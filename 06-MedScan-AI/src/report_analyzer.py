"""
Report Analyzer — Extraction + RAG Integration
=================================================
Takes a PDF, extracts biomarkers, queries RAG for each abnormal value,
and produces an enriched analysis with cited medical interpretations.
"""

import os
import json
from dataclasses import dataclass, field, asdict

from .pdf_extractor import extract_report, ExtractionResult
from .rag_pipeline import MedicalRAG


@dataclass
class BiomarkerAnalysis:
    canonical_name: str
    test_name: str
    value: float
    unit: str
    flag: str
    deviation_pct: float
    interpretation_band: str
    rag_interpretations: list[dict] = field(default_factory=list)  # [{title, content, source, similarity}]


@dataclass
class CombinedPatternAnalysis:
    pattern_title: str
    relevant_biomarkers: list[str]
    content: str
    source: str
    similarity: float


@dataclass
class EnrichedReport:
    patient_name: str
    patient_age: str
    patient_sex: str
    lab_name: str
    total_tests: int
    abnormal_count: int
    critical_count: int
    biomarker_analyses: list[BiomarkerAnalysis] = field(default_factory=list)
    combined_patterns: list[CombinedPatternAnalysis] = field(default_factory=list)
    normal_biomarkers: list[dict] = field(default_factory=list)
    source_file: str = ""


class ReportAnalyzer:
    """End-to-end: PDF → Extraction → RAG → Enriched Analysis."""

    def __init__(self):
        self.rag = MedicalRAG()
        if self.rag.collection.count() == 0:
            self.rag.build_index()

    def analyze(self, pdf_path: str) -> EnrichedReport:
        """Full pipeline: extract + RAG-enrich."""
        # Step 1: Extract
        extraction = extract_report(pdf_path)

        # Step 2: RAG-enrich each abnormal biomarker
        abnormal_analyses = []
        for b in extraction.biomarkers:
            if not b.is_abnormal:
                continue

            rag_results = self.rag.query_for_biomarker(
                biomarker_name=b.canonical_name or b.test_name,
                flag=b.flag,
                value=b.value,
                interpretation_band=b.interpretation_band,
                n_results=3,
            )

            interpretations = [
                {"title": r["title"], "content": r["content"][:500],
                 "source": r["source"], "similarity": r["similarity"]}
                for r in rag_results if r["similarity"] > 0.30
            ]

            abnormal_analyses.append(BiomarkerAnalysis(
                canonical_name=b.canonical_name,
                test_name=b.test_name,
                value=b.value,
                unit=b.unit,
                flag=b.flag,
                deviation_pct=b.deviation_pct,
                interpretation_band=b.interpretation_band,
                rag_interpretations=interpretations,
            ))

        # Step 3: Combined pattern analysis
        abnormal_dicts = [
            {"canonical_name": b.canonical_name, "flag": b.flag, "category": b.category}
            for b in extraction.biomarkers if b.is_abnormal and b.canonical_name
        ]
        pattern_results = self.rag.query_for_patterns(abnormal_dicts, n_results=5)
        combined_patterns = [
            CombinedPatternAnalysis(
                pattern_title=r["title"],
                relevant_biomarkers=[t for t in r["tags"] if t in {b["canonical_name"] for b in abnormal_dicts}],
                content=r["content"][:500],
                source=r["source"],
                similarity=r["similarity"],
            )
            for r in pattern_results if r["similarity"] > 0.25
        ]

        # Step 4: Normal biomarkers (brief)
        normals = [
            {"test_name": b.test_name, "value": b.value_raw, "unit": b.unit}
            for b in extraction.biomarkers if not b.is_abnormal
        ]

        return EnrichedReport(
            patient_name=extraction.patient.name,
            patient_age=extraction.patient.age,
            patient_sex=extraction.patient.sex,
            lab_name=extraction.patient.lab_name,
            total_tests=extraction.total_tests,
            abnormal_count=extraction.abnormal_count,
            critical_count=extraction.critical_count,
            biomarker_analyses=abnormal_analyses,
            combined_patterns=combined_patterns,
            normal_biomarkers=normals,
            source_file=extraction.source_file,
        )

    def print_enriched_report(self, report: EnrichedReport):
        """Print enriched report to console."""
        print("=" * 70)
        print("   MEDSCAN AI — Enriched Clinical Analysis (with RAG)")
        print("=" * 70)

        print(f"\n  Patient: {report.patient_name} | {report.patient_age} | {report.patient_sex}")
        print(f"  Lab: {report.lab_name}")
        print(f"  Tests: {report.total_tests} total | {report.abnormal_count} abnormal | {report.critical_count} critical")

        # Abnormal biomarkers with RAG interpretations
        print(f"\n{'─' * 70}")
        print(f"  ABNORMAL VALUES WITH CLINICAL INTERPRETATION")
        print(f"{'─' * 70}")

        for ba in report.biomarker_analyses:
            flag_icon = "🔺" if "HIGH" in ba.flag else "🔻"
            print(f"\n  {flag_icon} {ba.test_name}: {ba.value} {ba.unit} [{ba.flag}] (±{ba.deviation_pct}%)")
            if ba.interpretation_band:
                print(f"     Band: {ba.interpretation_band}")

            if ba.rag_interpretations:
                top = ba.rag_interpretations[0]
                # Truncate content for display
                snippet = top["content"][:200].replace("\n", " ")
                print(f"     📖 {top['title']}")
                print(f"        {snippet}...")
                print(f"        Source: {top['source']}")
            else:
                print(f"     (No RAG match found)")

        # Combined patterns
        if report.combined_patterns:
            print(f"\n{'─' * 70}")
            print(f"  COMBINED PATTERN ANALYSIS")
            print(f"{'─' * 70}")
            for cp in report.combined_patterns:
                snippet = cp.content[:180].replace("\n", " ")
                print(f"\n  🔗 {cp.pattern_title} (relevance: {cp.similarity:.2f})")
                print(f"     {snippet}...")
                print(f"     Source: {cp.source}")

        # Normal values
        print(f"\n{'─' * 70}")
        print(f"  NORMAL VALUES ({len(report.normal_biomarkers)})")
        print(f"{'─' * 70}")
        for n in report.normal_biomarkers:
            print(f"  ✓ {n['test_name']}: {n['value']} {n['unit']}")

        print(f"\n{'=' * 70}")

    def to_json(self, report: EnrichedReport) -> str:
        """Serialize enriched report to JSON."""
        return json.dumps(asdict(report), indent=2, ensure_ascii=False)


def main():
    import sys
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "sample_reports", "sample_report_01_cbc_lipid.pdf"
    )

    analyzer = ReportAnalyzer()
    report = analyzer.analyze(pdf_path)
    analyzer.print_enriched_report(report)

    # Save JSON
    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "processed")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "enriched_analysis.json")
    with open(out_path, "w") as f:
        f.write(analyzer.to_json(report))
    print(f"\n💾 JSON: {out_path}")


if __name__ == "__main__":
    main()

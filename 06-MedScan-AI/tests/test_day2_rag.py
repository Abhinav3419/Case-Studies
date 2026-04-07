"""Test Suite — Day 2: RAG Pipeline + Integrated Analyzer"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.rag_pipeline import MedicalRAG
from src.report_analyzer import ReportAnalyzer

REPORT_1 = os.path.join(os.path.dirname(__file__), "..", "data", "sample_reports", "sample_report_01_cbc_lipid.pdf")


def test_rag_index():
    print("TEST 1: RAG Index Build")
    rag = MedicalRAG()
    rag.build_index()
    count = rag.collection.count()
    assert count >= 25, f"Expected ≥25 chunks, got {count}"
    print(f"  ✅ {count} chunks indexed")
    return True


def test_rag_relevance():
    print("\nTEST 2: RAG Retrieval Relevance")
    rag = MedicalRAG()
    errors = []

    checks = [
        ("elevated TSH hypothyroidism", "Hypothyroidism"),
        ("low vitamin D deficiency", "Vitamin D"),
        ("high LDL cholesterol cardiovascular", "Cholesterol"),
        ("elevated ALT AST liver", "AST and ALT"),
        ("iron deficiency low ferritin", "Iron Deficiency"),
        ("HbA1c prediabetes elevated", "HbA1c"),
    ]

    for query, expected_keyword in checks:
        results = rag.query(query, n_results=1)
        top = results[0]
        if expected_keyword.lower() in top["title"].lower():
            print(f"  ✅ '{query[:30]}...' → {top['title'][:50]} ({top['similarity']:.2f})")
        else:
            print(f"  ❌ '{query[:30]}...' → {top['title'][:50]} (expected '{expected_keyword}')")
            errors.append(query)

    return len(errors) == 0


def test_integrated_analysis():
    print("\nTEST 3: Integrated PDF → RAG Analysis")
    analyzer = ReportAnalyzer()
    report = analyzer.analyze(REPORT_1)

    checks = []

    # Check enrichment happened
    enriched_count = sum(1 for ba in report.biomarker_analyses if ba.rag_interpretations)
    checks.append(("Enriched biomarkers ≥ 15", enriched_count >= 15))
    print(f"  {'✅' if enriched_count >= 15 else '❌'} Enriched: {enriched_count}/{len(report.biomarker_analyses)}")

    # Check combined patterns found
    checks.append(("Combined patterns ≥ 2", len(report.combined_patterns) >= 2))
    print(f"  {'✅' if len(report.combined_patterns) >= 2 else '❌'} Patterns: {len(report.combined_patterns)}")

    # Check specific match: TSH → Hypothyroidism
    tsh_match = any(
        "hypothyroidism" in ba.rag_interpretations[0]["title"].lower()
        for ba in report.biomarker_analyses
        if ba.canonical_name == "tsh" and ba.rag_interpretations
    )
    checks.append(("TSH → Hypothyroidism match", tsh_match))
    print(f"  {'✅' if tsh_match else '❌'} TSH → Hypothyroidism")

    # Check HbA1c → Prediabetes/Diabetes
    hba1c_match = any(
        "hba1c" in ba.rag_interpretations[0]["title"].lower()
        for ba in report.biomarker_analyses
        if ba.canonical_name == "hba1c" and ba.rag_interpretations
    )
    checks.append(("HbA1c → Diabetes knowledge", hba1c_match))
    print(f"  {'✅' if hba1c_match else '❌'} HbA1c → Glycemic interpretation")

    return all(c[1] for c in checks)


def main():
    print("=" * 50)
    print("  MEDSCAN AI — Day 2 Test Suite")
    print("=" * 50)

    results = {
        "RAG Index": test_rag_index(),
        "RAG Relevance": test_rag_relevance(),
        "Integrated Analysis": test_integrated_analysis(),
    }

    print("\n" + "=" * 50)
    passed = sum(v for v in results.values())
    for name, ok in results.items():
        print(f"  {'✅' if ok else '❌'} {name}")
    print(f"\n  {passed}/{len(results)} passed")
    print("=" * 50)


if __name__ == "__main__":
    main()

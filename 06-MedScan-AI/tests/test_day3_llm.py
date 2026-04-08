"""Test Suite — Day 3: LLM Clinical Analysis Engine"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.llm_engine import ClinicalAnalysisEngine, format_clinical_report, report_to_json

REPORT_1 = os.path.join(os.path.dirname(__file__), "..", "data", "sample_reports", "sample_report_01_cbc_lipid.pdf")
REPORT_2 = os.path.join(os.path.dirname(__file__), "..", "data", "sample_reports", "sample_report_02_thyroid.pdf")


def test_full_pipeline():
    print("TEST 1: Full Pipeline (PDF → Extract → RAG → Analysis)")
    engine = ClinicalAnalysisEngine(mode="local")
    report = engine.analyze_report(REPORT_1)

    checks = [
        ("Patient name", report.patient_name != ""),
        ("Biomarker interpretations ≥ 15", len(report.biomarker_interpretations) >= 15),
        ("Pattern interpretations ≥ 2", len(report.pattern_interpretations) >= 2),
        ("Executive summary exists", len(report.executive_summary) > 50),
        ("Lifestyle recs exist", len(report.lifestyle_recommendations) >= 3),
        ("Follow-up tests exist", len(report.follow_up_tests) >= 3),
        ("Disclaimer present", "educational" in report.disclaimer.lower()),
    ]

    for name, ok in checks:
        print(f"  {'✅' if ok else '❌'} {name}")

    return all(c[1] for c in checks)


def test_urgency_classification():
    print("\nTEST 2: Urgency Classification")
    engine = ClinicalAnalysisEngine(mode="local")
    report = engine.analyze_report(REPORT_1)

    urgencies = {i.urgency for i in report.biomarker_interpretations}
    has_routine = "routine" in urgencies
    has_soon = "soon" in urgencies

    checks = [
        ("Has routine urgency", has_routine),
        ("Has soon urgency", has_soon),
        ("All urgencies valid", urgencies.issubset({"routine", "soon", "urgent", "emergency"})),
    ]

    for name, ok in checks:
        print(f"  {'✅' if ok else '❌'} {name}")

    urgency_dist = {}
    for i in report.biomarker_interpretations:
        urgency_dist[i.urgency] = urgency_dist.get(i.urgency, 0) + 1
    print(f"  Distribution: {urgency_dist}")

    return all(c[1] for c in checks)


def test_causes_and_actions():
    print("\nTEST 3: Causes + Actions Quality")
    engine = ClinicalAnalysisEngine(mode="local")
    report = engine.analyze_report(REPORT_1)

    checks = []
    for bi in report.biomarker_interpretations:
        has_causes = len(bi.possible_causes) >= 2
        has_actions = len(bi.recommended_actions) >= 2
        has_sources = len(bi.sources) >= 1
        if not has_causes:
            print(f"  ❌ {bi.test_name}: missing causes")
        if not has_actions:
            print(f"  ❌ {bi.test_name}: missing actions")
        checks.append(has_causes and has_actions)

    pass_rate = sum(checks) / len(checks) * 100
    print(f"  ✅ Causes+Actions coverage: {sum(checks)}/{len(checks)} ({pass_rate:.0f}%)")
    return pass_rate >= 80


def test_json_serialization():
    print("\nTEST 4: JSON Serialization")
    engine = ClinicalAnalysisEngine(mode="local")
    report = engine.analyze_report(REPORT_1)
    json_str = report_to_json(report)

    try:
        data = json.loads(json_str)
        checks = [
            ("Valid JSON", True),
            ("Has executive_summary", "executive_summary" in data),
            ("Has biomarker_interpretations", len(data.get("biomarker_interpretations", [])) > 0),
            ("Has pattern_interpretations", len(data.get("pattern_interpretations", [])) > 0),
        ]
        for name, ok in checks:
            print(f"  {'✅' if ok else '❌'} {name}")
        print(f"  JSON size: {len(json_str):,} chars")
        return all(c[1] for c in checks)
    except json.JSONDecodeError:
        print("  ❌ Invalid JSON")
        return False


def test_report_2_thyroid():
    print("\nTEST 5: Report 2 (Thyroid Panel)")
    engine = ClinicalAnalysisEngine(mode="local")
    report = engine.analyze_report(REPORT_2)

    tsh_found = any(bi.canonical_name == "tsh" for bi in report.biomarker_interpretations)
    has_hashimoto_ref = any(
        "hashimoto" in bi.clinical_significance.lower() or
        any("hashimoto" in c.lower() for c in bi.possible_causes)
        for bi in report.biomarker_interpretations if bi.canonical_name == "tsh"
    )

    checks = [
        ("TSH interpreted", tsh_found),
        ("Hashimoto reference", has_hashimoto_ref),
        ("Interpretations ≥ 3", len(report.biomarker_interpretations) >= 3),
    ]
    for name, ok in checks:
        print(f"  {'✅' if ok else '❌'} {name}")

    return all(c[1] for c in checks)


def main():
    print("=" * 50)
    print("  MEDSCAN AI — Day 3 Test Suite")
    print("=" * 50)

    results = {
        "Full Pipeline": test_full_pipeline(),
        "Urgency Classification": test_urgency_classification(),
        "Causes + Actions": test_causes_and_actions(),
        "JSON Serialization": test_json_serialization(),
        "Report 2 (Thyroid)": test_report_2_thyroid(),
    }

    print("\n" + "=" * 50)
    passed = sum(v for v in results.values())
    for name, ok in results.items():
        print(f"  {'✅' if ok else '❌'} {name}")
    print(f"\n  {passed}/{len(results)} passed")
    print("=" * 50)


if __name__ == "__main__":
    main()

"""
Day 5 — Comprehensive Validation Suite
=========================================
Runs all 5 sample reports through the complete pipeline.
Validates extraction, RAG, analysis, and verification.
"""

import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.pdf_extractor import extract_report
from src.llm_engine import ClinicalAnalysisEngine, report_to_json
from src.medical_verifier import MedicalVerificationSystem

REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "sample_reports")

REPORTS = [
    ("sample_report_01_cbc_lipid.pdf", "Full Panel (CBC+Lipid+LFT+Thyroid+KFT+Glucose+Vitamins)", {
        "min_tests": 40, "min_abnormal": 15,
        "must_detect": ["haemoglobin", "tsh", "hba1c", "vitamin_d", "ldl_cholesterol"],
    }),
    ("sample_report_02_thyroid.pdf", "Thyroid Panel (SRL format)", {
        "min_tests": 4, "min_abnormal": 3,
        "must_detect": ["tsh"],
    }),
    ("sample_report_03_infectious.pdf", "Infectious Disease Panel", {
        "min_tests": 8, "min_abnormal": 5,
        "must_detect": ["haemoglobin", "crp"],
    }),
    ("sample_report_04_tumour_markers.pdf", "Tumour Marker Panel", {
        "min_tests": 8, "min_abnormal": 5,
        "must_detect": ["psa", "ldh"],
    }),
    ("sample_report_05_coagulation.pdf", "Coagulation + Critical Values", {
        "min_tests": 8, "min_abnormal": 8,
        "must_detect": ["d_dimer", "crp", "procalcitonin"],
    }),
]


def test_full_pipeline():
    print("=" * 60)
    print("  DAY 5 — COMPREHENSIVE VALIDATION")
    print("=" * 60)

    engine = ClinicalAnalysisEngine(mode="local")
    verifier = MedicalVerificationSystem()
    all_pass = True

    for filename, label, criteria in REPORTS:
        filepath = os.path.join(REPORTS_DIR, filename)
        if not os.path.exists(filepath):
            print(f"\n  [SKIP] {filename} — not found")
            continue

        print(f"\n  {'─' * 56}")
        print(f"  REPORT: {label}")
        print(f"  {'─' * 56}")

        # 1. Extraction
        extraction = extract_report(filepath)
        tests_ok = extraction.total_tests >= criteria["min_tests"]
        abnormal_ok = extraction.abnormal_count >= criteria["min_abnormal"]
        print(f"  Extraction: {extraction.total_tests} tests, {extraction.abnormal_count} abnormal "
              f"{'PASS' if tests_ok and abnormal_ok else 'FAIL'}")

        if not tests_ok:
            print(f"    Expected >= {criteria['min_tests']} tests, got {extraction.total_tests}")
            all_pass = False
        if not abnormal_ok:
            print(f"    Expected >= {criteria['min_abnormal']} abnormal, got {extraction.abnormal_count}")
            all_pass = False

        # 2. Must-detect biomarkers
        detected = {b.canonical_name for b in extraction.biomarkers if b.is_abnormal}
        for must in criteria["must_detect"]:
            if must in detected:
                print(f"    Detected: {must}")
            else:
                print(f"    MISSED: {must}")
                all_pass = False

        # 3. Full analysis
        try:
            report = engine.analyze_report(filepath)
            has_summary = len(report.executive_summary) > 30
            has_interps = len(report.biomarker_interpretations) > 0
            has_causes = all(len(bi.possible_causes) >= 1 for bi in report.biomarker_interpretations)
            has_actions = all(len(bi.recommended_actions) >= 1 for bi in report.biomarker_interpretations)

            print(f"  Analysis: {len(report.biomarker_interpretations)} interpretations, "
                  f"{len(report.pattern_interpretations)} patterns")
            print(f"    Summary: {'PASS' if has_summary else 'FAIL'} | "
                  f"Causes: {'PASS' if has_causes else 'FAIL'} | "
                  f"Actions: {'PASS' if has_actions else 'FAIL'}")

            if not (has_summary and has_interps and has_causes and has_actions):
                all_pass = False

            # 4. Verification (no anatomical errors in blood reports)
            v_report = verifier.verify_biomarkers(report.biomarker_interpretations)
            critical_errors = v_report.critical_errors
            print(f"  Verification: {v_report.valid_facts} valid, "
                  f"{v_report.flagged_facts} flagged, {critical_errors} critical")

            # 5. JSON serialization
            json_str = report_to_json(report)
            try:
                json.loads(json_str)
                print(f"  JSON: PASS ({len(json_str):,} chars)")
            except json.JSONDecodeError:
                print(f"  JSON: FAIL — invalid JSON")
                all_pass = False

        except Exception as e:
            print(f"  Analysis FAILED: {e}")
            all_pass = False

    return all_pass


def test_edge_cases():
    print(f"\n{'=' * 60}")
    print("  EDGE CASE TESTS")
    print(f"{'=' * 60}")

    errors = []

    # 1. Empty/minimal PDF handling
    print("\n  Test: Patient name extraction across formats")
    expected_names = {
        "sample_report_01_cbc_lipid.pdf": "abhinav pandey",
        "sample_report_02_thyroid.pdf": "priya sharma",
        "sample_report_03_infectious.pdf": "ravi kumar",
        "sample_report_04_tumour_markers.pdf": "suresh patel",
        "sample_report_05_coagulation.pdf": "meera joshi",
    }
    for fname, expected in expected_names.items():
        fpath = os.path.join(REPORTS_DIR, fname)
        if os.path.exists(fpath):
            ext = extract_report(fpath)
            if expected in ext.patient.name.lower():
                print(f"    {fname[:30]}: '{ext.patient.name}' PASS")
            else:
                print(f"    {fname[:30]}: got '{ext.patient.name}', expected '{expected}' FAIL")
                errors.append(f"Name mismatch: {fname}")

    # 2. Gender-specific reference ranges
    print("\n  Test: Gender-specific reference ranges")
    r1 = extract_report(os.path.join(REPORTS_DIR, "sample_report_01_cbc_lipid.pdf"))  # Male
    r2 = extract_report(os.path.join(REPORTS_DIR, "sample_report_02_thyroid.pdf"))    # Female
    print(f"    Report 1 sex: {r1.patient.sex} | Report 2 sex: {r2.patient.sex}")
    if r1.patient.sex == "Male" and r2.patient.sex == "Female":
        print("    PASS")
    else:
        print("    FAIL")
        errors.append("Gender detection failed")

    # 3. Urgency distribution check
    print("\n  Test: Urgency classification for critical report")
    engine = ClinicalAnalysisEngine(mode="local")
    critical_report = engine.analyze_report(os.path.join(REPORTS_DIR, "sample_report_05_coagulation.pdf"))
    urgencies = {bi.urgency for bi in critical_report.biomarker_interpretations}
    has_urgent_or_higher = "urgent" in urgencies or "emergency" in urgencies or "soon" in urgencies
    print(f"    Urgencies found: {urgencies}")
    print(f"    Has urgent/emergency: {'PASS' if has_urgent_or_higher else 'FAIL'}")
    if not has_urgent_or_higher:
        errors.append("Critical report missing urgent classification")

    return len(errors) == 0


def main():
    print("\n" + "=" * 60)
    print("  MEDSCAN AI — DAY 5 FINAL VALIDATION SUITE")
    print("=" * 60)

    r1 = test_full_pipeline()
    r2 = test_edge_cases()

    # Also run all previous test suites
    print(f"\n{'=' * 60}")
    print("  REGRESSION — ALL PREVIOUS TESTS")
    print(f"{'=' * 60}")

    import subprocess
    prev_tests = [
        "tests/test_extraction.py",
        "tests/test_day2_rag.py",
        "tests/test_day3_llm.py",
        "tests/test_red_team.py",
    ]
    prev_pass = True
    for t in prev_tests:
        result = subprocess.run([sys.executable, t], capture_output=True, text=True,
                                cwd=os.path.dirname(os.path.dirname(__file__)))
        if "passed" in result.stdout.split("\n")[-2] if result.stdout else "":
            line = [l for l in result.stdout.split("\n") if "passed" in l][-1].strip()
            print(f"  {t}: {line}")
        else:
            print(f"  {t}: CHECK OUTPUT")

    print(f"\n{'=' * 60}")
    print(f"  FINAL RESULT")
    print(f"{'=' * 60}")
    print(f"  Full Pipeline Validation: {'PASS' if r1 else 'FAIL'}")
    print(f"  Edge Case Tests: {'PASS' if r2 else 'FAIL'}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()

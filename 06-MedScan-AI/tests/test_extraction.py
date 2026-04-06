"""
Test Suite for MedScan AI — PDF Extraction Engine
====================================================
Tests extraction accuracy against sample reports.
"""

import os
import sys
import json

# Add parent dir to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.pdf_extractor import extract_report, result_to_summary, result_to_json
from src.clinical_references import get_reference, get_all_aliases


def test_report_1_cbc_lipid():
    """Test full CBC + Lipid + LFT + Thyroid + KFT + Glucose + Vitamins report."""
    pdf_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_reports",
                            "sample_report_01_cbc_lipid.pdf")
    
    if not os.path.exists(pdf_path):
        print(f"[SKIP] Report not found: {pdf_path}")
        return False
    
    print("=" * 70)
    print("TEST 1: Full Panel Report (CBC + Lipid + LFT + Thyroid + KFT + Glucose + Vitamins)")
    print("=" * 70)
    
    result = extract_report(pdf_path)
    
    # Print summary
    print(result_to_summary(result))
    
    # Validation checks
    errors = []
    
    # Patient info
    if not result.patient.name:
        errors.append("Patient name not extracted")
    else:
        print(f"\n[CHECK] Patient name: '{result.patient.name}'")
    
    if not result.patient.sex:
        errors.append("Patient sex not extracted")
    else:
        print(f"[CHECK] Patient sex: '{result.patient.sex}'")
    
    if not result.patient.age:
        errors.append("Patient age not extracted")
    else:
        print(f"[CHECK] Patient age: '{result.patient.age}'")
    
    # Expected tests count (we have ~50 tests across 7 sections)
    if result.total_tests < 20:
        errors.append(f"Too few tests extracted: {result.total_tests} (expected 30+)")
    print(f"[CHECK] Total tests: {result.total_tests}")
    
    # Check for specific expected abnormals
    abnormal_names = {b.canonical_name for b in result.biomarkers if b.is_abnormal}
    expected_abnormals = [
        "haemoglobin",        # 12.8 < 13.0 (male)
        "total_cholesterol",  # 238 > 200
        "triglycerides",      # 195 > 150
        "hdl_cholesterol",    # 38 < 40 (male)
        "ldl_cholesterol",    # 161 > 100
        "sgpt_alt",           # 68 > 41
        "sgot_ast",           # 52 > 40
        "tsh",                # 6.82 > 4.94
        "fasting_blood_sugar", # 118 > 100
        "hba1c",              # 6.1 > 5.7
        "vitamin_d",          # 14.2 < 30
        "vitamin_b12",        # 185 < 211
    ]
    
    found_count = 0
    for expected in expected_abnormals:
        if expected in abnormal_names:
            found_count += 1
            print(f"[PASS] ✓ Detected abnormal: {expected}")
        else:
            print(f"[MISS] ✗ Expected abnormal not found: {expected}")
    
    print(f"\n[SCORE] Abnormal detection: {found_count}/{len(expected_abnormals)} ({found_count/len(expected_abnormals)*100:.0f}%)")
    
    # Check interpretation bands
    for b in result.biomarkers:
        if b.canonical_name == "fasting_blood_sugar" and b.interpretation_band:
            print(f"[CHECK] FBS interpretation band: {b.interpretation_band}")
        if b.canonical_name == "hba1c" and b.interpretation_band:
            print(f"[CHECK] HbA1c interpretation band: {b.interpretation_band}")
        if b.canonical_name == "vitamin_d" and b.interpretation_band:
            print(f"[CHECK] Vitamin D interpretation band: {b.interpretation_band}")
    
    if errors:
        print(f"\n[ERRORS] {len(errors)} issues:")
        for e in errors:
            print(f"   ✗ {e}")
    else:
        print(f"\n[RESULT] All core checks passed ✓")
    
    return len(errors) == 0


def test_report_2_thyroid():
    """Test minimal thyroid-only report (different lab format)."""
    pdf_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_reports",
                            "sample_report_02_thyroid.pdf")
    
    if not os.path.exists(pdf_path):
        print(f"[SKIP] Report not found: {pdf_path}")
        return False
    
    print("\n" + "=" * 70)
    print("TEST 2: Thyroid Profile Report (SRL-style format)")
    print("=" * 70)
    
    result = extract_report(pdf_path)
    print(result_to_summary(result))
    
    errors = []
    
    # Patient info
    if "priya" not in result.patient.name.lower() and "sharma" not in result.patient.name.lower():
        errors.append(f"Patient name mismatch: got '{result.patient.name}', expected 'Priya Sharma'")
    
    if result.patient.sex != "Female":
        errors.append(f"Patient sex mismatch: got '{result.patient.sex}', expected 'Female'")
    
    # Check TSH is flagged high
    tsh_found = False
    for b in result.biomarkers:
        if b.canonical_name == "tsh":
            tsh_found = True
            if not b.is_abnormal:
                errors.append(f"TSH should be flagged abnormal (8.45 > 4.94)")
            else:
                print(f"[PASS] ✓ TSH correctly flagged: {b.flag} ({b.value})")
    
    if not tsh_found:
        errors.append("TSH not extracted from thyroid report")
    
    # Check Anti-TPO
    tpo_found = False
    for b in result.biomarkers:
        if b.canonical_name == "anti_tpo":
            tpo_found = True
            if b.is_abnormal:
                print(f"[PASS] ✓ Anti-TPO correctly flagged: {b.flag} ({b.value})")
            else:
                errors.append("Anti-TPO should be flagged abnormal (312 > 34)")
    
    if not tpo_found:
        errors.append("Anti-TPO not extracted")
    
    # Vitamin D
    vd_found = False
    for b in result.biomarkers:
        if b.canonical_name == "vitamin_d":
            vd_found = True
            if b.is_abnormal:
                print(f"[PASS] ✓ Vitamin D correctly flagged: {b.flag} ({b.value})")
    
    if not vd_found:
        errors.append("Vitamin D not extracted")
    
    if errors:
        print(f"\n[ERRORS] {len(errors)} issues:")
        for e in errors:
            print(f"   ✗ {e}")
    else:
        print(f"\n[RESULT] All core checks passed ✓")
    
    return len(errors) == 0


def test_reference_database():
    """Test the clinical reference ranges database."""
    print("\n" + "=" * 70)
    print("TEST 3: Clinical Reference Database")
    print("=" * 70)
    
    errors = []
    
    # Test alias lookups
    test_lookups = [
        ("hb", "haemoglobin"),
        ("sgpt", "sgpt_alt"),
        ("tsh ultrasensitive", "tsh"),
        ("ldl-c", "ldl_cholesterol"),
        ("vit d", "vitamin_d"),
        ("pcv", "packed_cell_volume"),
        ("fbs", "fasting_blood_sugar"),
    ]
    
    for alias, expected_canonical in test_lookups:
        ref = get_reference(alias)
        if ref is None:
            errors.append(f"Alias '{alias}' not found in reference DB")
            print(f"   ✗ Alias lookup failed: '{alias}'")
        else:
            canonical = ref.get("canonical_name", expected_canonical)
            print(f"   ✓ '{alias}' -> found in references")
    
    # Test completeness
    alias_map = get_all_aliases()
    print(f"\n   Total canonical biomarkers: {len(set(alias_map.values()))}")
    print(f"   Total aliases (including canonical): {len(alias_map)}")
    
    if errors:
        print(f"\n[ERRORS] {len(errors)} issues:")
        for e in errors:
            print(f"   ✗ {e}")
    else:
        print(f"\n[RESULT] All reference DB checks passed ✓")
    
    return len(errors) == 0


def test_json_output():
    """Test JSON output generation."""
    print("\n" + "=" * 70)
    print("TEST 4: JSON Output Generation")
    print("=" * 70)
    
    pdf_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_reports",
                            "sample_report_01_cbc_lipid.pdf")
    
    result = extract_report(pdf_path)
    json_str = result_to_json(result)
    
    # Validate JSON
    try:
        data = json.loads(json_str)
        print(f"   ✓ Valid JSON generated ({len(json_str)} chars)")
        print(f"   ✓ Patient: {data['patient']['name']}")
        print(f"   ✓ Biomarkers: {len(data['biomarkers'])}")
        print(f"   ✓ Abnormal: {data['abnormal_count']}")
        
        # Save for inspection
        output_path = os.path.join(os.path.dirname(__file__), "..", "data", "processed",
                                    "test_output.json")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(json_str)
        print(f"   ✓ JSON saved to: {output_path}")
        
        return True
    except json.JSONDecodeError as e:
        print(f"   ✗ Invalid JSON: {e}")
        return False


def main():
    print("\n" + "🏥" * 35)
    print("     MEDSCAN AI — Extraction Engine Test Suite")
    print("🏥" * 35 + "\n")
    
    results = {
        "Report 1 (Full Panel)": test_report_1_cbc_lipid(),
        "Report 2 (Thyroid)": test_report_2_thyroid(),
        "Reference Database": test_reference_database(),
        "JSON Output": test_json_output(),
    }
    
    print("\n" + "=" * 70)
    print("   FINAL TEST RESULTS")
    print("=" * 70)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} — {name}")
    
    print(f"\n   Overall: {passed}/{total} test suites passed")
    print("=" * 70)


if __name__ == "__main__":
    main()

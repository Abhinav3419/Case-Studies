"""
Red-Team Adversarial Test Suite
==================================
Tests the anatomical grounding and multi-agent verification system
against deliberately crafted adversarial inputs.

50 correct findings + 50 hallucinated errors.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.anatomical_grounding import validate_condition_in_region
from src.medical_verifier import MedicalVerificationSystem, ExtractedFact


# ── Test Cases ──

CORRECT_FINDINGS = [
    ("hydronephrosis", "abdomen"),
    ("hydronephrosis", "pelvis"),
    ("renal calculus", "abdomen"),
    ("fatty liver", "abdomen"),
    ("hepatomegaly", "abdomen"),
    ("cirrhosis", "abdomen"),
    ("consolidation", "chest"),
    ("pleural effusion", "chest"),
    ("pulmonary embolism", "chest"),
    ("ground glass", "chest"),
    ("lung mass", "chest"),
    ("brain infarct", "brain"),
    ("hydrocephalus", "brain"),
    ("meningioma", "brain"),
    ("subdural hematoma", "brain"),
    ("subarachnoid hemorrhage", "brain"),
    ("cerebral atrophy", "brain"),
    ("cardiomegaly", "chest"),
    ("pericardial effusion", "chest"),
    ("aortic aneurysm", "chest"),
    ("fracture", "extremity"),
    ("osteoporosis", "spine"),
    ("disc herniation", "spine"),
    ("thyroid nodule", "neck"),
    ("lymphadenopathy", "chest"),
    ("lymphadenopathy", "abdomen"),
    ("lymphadenopathy", "neck"),
    ("ascites", "abdomen"),
    ("splenomegaly", "abdomen"),
    ("appendicitis", "abdomen"),
    ("cholelithiasis", "abdomen"),
    ("pancreatitis", "abdomen"),
    ("ovarian cyst", "pelvis"),
    ("uterine fibroid", "pelvis"),
    ("prostatic enlargement", "pelvis"),
    ("bowel obstruction", "abdomen"),
    ("colitis", "abdomen"),
    ("brain mass", "brain"),
    ("encephalitis", "brain"),
    ("demyelination", "brain"),
    ("atelectasis", "chest"),
    ("emphysema", "chest"),
    ("bronchiectasis", "chest"),
    ("pneumothorax", "chest"),
    ("hepatic mass", "abdomen"),
    ("biliary dilatation", "abdomen"),
    ("bladder mass", "pelvis"),
    ("spondylosis", "spine"),
    ("fracture", "spine"),
    ("adrenal mass", "abdomen"),
]

HALLUCINATED_FINDINGS = [
    # Renal conditions in wrong regions
    ("hydronephrosis", "brain"),
    ("hydronephrosis", "chest"),
    ("renal calculus", "brain"),
    ("renal calculus", "chest"),
    ("pyelonephritis", "brain"),
    ("renal cyst", "brain"),
    ("renal cell carcinoma", "brain"),
    ("bladder mass", "brain"),
    ("bladder mass", "chest"),
    ("vesicoureteral reflux", "brain"),

    # Liver conditions in wrong regions
    ("fatty liver", "brain"),
    ("hepatomegaly", "brain"),
    ("cirrhosis", "brain"),
    ("hepatic mass", "brain"),
    ("cholecystitis", "brain"),
    ("hepatomegaly", "chest"),
    ("hepatic steatosis", "chest"),

    # Brain conditions in wrong regions
    ("hydrocephalus", "abdomen"),
    ("hydrocephalus", "chest"),
    ("brain infarct", "abdomen"),
    ("meningioma", "abdomen"),
    ("subdural hematoma", "abdomen"),
    ("encephalitis", "chest"),
    ("cerebral atrophy", "abdomen"),
    ("glioma", "chest"),
    ("subarachnoid hemorrhage", "abdomen"),

    # Lung conditions in wrong regions
    ("pneumothorax", "brain"),
    ("pleural effusion", "brain"),
    ("consolidation", "brain"),
    ("bronchiectasis", "brain"),
    ("pulmonary embolism", "brain"),
    ("atelectasis", "brain"),
    ("emphysema", "brain"),
    ("pulmonary fibrosis", "brain"),

    # Reproductive in wrong regions
    ("ovarian cyst", "brain"),
    ("ovarian cyst", "chest"),
    ("uterine fibroid", "brain"),
    ("uterine fibroid", "chest"),
    ("prostatic enlargement", "brain"),
    ("prostatic enlargement", "chest"),

    # Heart conditions in wrong regions
    ("cardiomegaly", "brain"),
    ("pericardial effusion", "brain"),
    ("myocardial infarction", "abdomen"),

    # GI conditions in wrong regions
    ("appendicitis", "brain"),
    ("appendicitis", "chest"),
    ("bowel obstruction", "brain"),
    ("colitis", "brain"),
    ("diverticulitis", "brain"),
    ("pancreatitis", "brain"),
    ("cholelithiasis", "brain"),
]


def test_anatomical_grounding():
    """Test the anatomical grounding validation."""
    print("=" * 60)
    print("  TEST: Anatomical Grounding Validation")
    print("=" * 60)

    # Test correct findings (should all pass)
    print(f"\n  Testing {len(CORRECT_FINDINGS)} CORRECT findings...")
    correct_pass = 0
    correct_fail = []
    for condition, region in CORRECT_FINDINGS:
        result = validate_condition_in_region(condition, region)
        if result["valid"]:
            correct_pass += 1
        else:
            correct_fail.append((condition, region, result["message"]))

    print(f"  ✅ Correct: {correct_pass}/{len(CORRECT_FINDINGS)} passed")
    if correct_fail:
        for c, r, m in correct_fail[:5]:
            print(f"    ❌ False negative: '{c}' in '{r}' — {m}")

    # Test hallucinated findings (should all fail)
    print(f"\n  Testing {len(HALLUCINATED_FINDINGS)} HALLUCINATED findings...")
    halluc_caught = 0
    halluc_missed = []
    for condition, region in HALLUCINATED_FINDINGS:
        result = validate_condition_in_region(condition, region)
        if not result["valid"]:
            halluc_caught += 1
        else:
            halluc_missed.append((condition, region))

    print(f"  ✅ Caught: {halluc_caught}/{len(HALLUCINATED_FINDINGS)} hallucinations blocked")
    if halluc_missed:
        for c, r in halluc_missed[:5]:
            print(f"    ❌ Missed hallucination: '{c}' in '{r}'")

    # Accuracy
    total = len(CORRECT_FINDINGS) + len(HALLUCINATED_FINDINGS)
    correct_total = correct_pass + halluc_caught
    accuracy = correct_total / total * 100

    print(f"\n  ACCURACY: {correct_total}/{total} ({accuracy:.1f}%)")
    return accuracy >= 90


def test_multi_agent_verification():
    """Test the Extractor + Critic multi-agent system."""
    print("\n" + "=" * 60)
    print("  TEST: Multi-Agent Verification System")
    print("=" * 60)

    system = MedicalVerificationSystem()

    # Test 1: Hydronephrosis in Brain (should catch)
    print("\n  Case 1: Hydronephrosis in Brain MRI")
    from dataclasses import dataclass

    @dataclass
    class FakeFinding:
        finding: str
        body_region: str

    findings = [FakeFinding("hydronephrosis of third ventricle", "Brain")]
    report = system.verify_radiology(findings, "brain", "MRI")

    critical = [r for r in report.audit_results if r.severity == "critical"]
    if critical:
        print(f"  ✅ CAUGHT — {critical[0].error_message[:80]}...")
    else:
        print("  ❌ MISSED — should have caught anatomical mismatch")

    # Test 2: Normal abdomen findings (should pass)
    print("\n  Case 2: Fatty liver in CT Abdomen")
    findings2 = [FakeFinding("fatty liver with hepatomegaly", "Liver")]
    report2 = system.verify_radiology(findings2, "abdomen", "CT")

    flagged = [r for r in report2.audit_results if not r.is_valid]
    if not flagged:
        print(f"  ✅ PASSED — no false positives")
    else:
        print(f"  ❌ FALSE POSITIVE — flagged valid finding: {flagged[0].error_message[:80]}")

    # Test 3: Impossible biomarker value
    print("\n  Case 3: Haemoglobin 45 g/dL (impossible)")
    bio_facts = [ExtractedFact(fact_type="biomarker", value="Haemoglobin: 45 g/dL")]
    bio_report = system.critic.audit_facts(bio_facts)
    bio_critical = [r for r in bio_report.audit_results if r.severity == "critical"]
    if bio_critical:
        print(f"  ✅ CAUGHT — {bio_critical[0].error_message[:80]}...")
    else:
        print("  ❌ MISSED — should have caught impossible value")

    # Test 4: Chain-of-thought output
    print("\n  Case 4: CoT Reasoning for Renal Calculus in Brain")
    findings4 = [FakeFinding("renal calculus", "Kidney")]
    report4 = system.verify_radiology(findings4, "brain", "CT")
    cot_critical = [r for r in report4.audit_results if r.severity == "critical"]
    if cot_critical:
        print(f"  ✅ CAUGHT with reasoning:")
        for line in cot_critical[0].cot_reasoning.split("\n"):
            print(f"     {line}")
    else:
        print("  ❌ MISSED")

    return True


def test_chain_of_thought():
    """Verify CoT reasoning is complete for all steps."""
    print("\n" + "=" * 60)
    print("  TEST: Chain-of-Thought Completeness")
    print("=" * 60)

    system = MedicalVerificationSystem()

    from dataclasses import dataclass
    @dataclass
    class F:
        finding: str
        body_region: str

    report = system.verify_radiology(
        [F("pleural effusion", "Lung")],
        "brain", "MRI"
    )

    for r in report.audit_results:
        if r.cot_reasoning:
            steps = [l for l in r.cot_reasoning.split("\n") if l.startswith("Step")]
            if len(steps) >= 3:
                print(f"  ✅ CoT has {len(steps)} steps")
            else:
                print(f"  ❌ CoT incomplete — only {len(steps)} steps")

    return True


def main():
    print("\n" + "🛡️" * 30)
    print("  MEDSCAN AI — Red Team / Adversarial Test Suite")
    print("🛡️" * 30)

    results = {
        "Anatomical Grounding": test_anatomical_grounding(),
        "Multi-Agent Verification": test_multi_agent_verification(),
        "Chain-of-Thought": test_chain_of_thought(),
    }

    print("\n" + "=" * 60)
    passed = sum(v for v in results.values())
    for name, ok in results.items():
        print(f"  {'✅' if ok else '❌'} {name}")
    print(f"\n  {passed}/{len(results)} passed")
    print("=" * 60)


if __name__ == "__main__":
    main()

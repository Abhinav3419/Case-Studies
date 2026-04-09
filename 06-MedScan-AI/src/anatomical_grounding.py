"""
Anatomical Grounding Engine
==============================
Validates that pathology findings are biologically possible in the stated
anatomical region. Prevents hallucinations like "Hydronephrosis in Brain."

Implements:
1. Anatomy-Pathology Property Matrix
2. Organ-System hierarchy
3. Scan-region → allowed organs mapping
4. Condition → required organ mapping
"""

# ── Organ System Hierarchy ──
# Maps every organ to its parent system

ORGAN_TO_SYSTEM = {
    # Central Nervous System
    "brain": "cns", "cerebrum": "cns", "cerebellum": "cns", "brainstem": "cns",
    "ventricle": "cns", "third ventricle": "cns", "lateral ventricle": "cns",
    "fourth ventricle": "cns", "thalamus": "cns", "hypothalamus": "cns",
    "pituitary": "cns", "meninges": "cns", "spinal cord": "cns",
    "corpus callosum": "cns", "basal ganglia": "cns", "hippocampus": "cns",

    # Cardiovascular
    "heart": "cardiovascular", "aorta": "cardiovascular", "coronary": "cardiovascular",
    "pericardium": "cardiovascular", "myocardium": "cardiovascular",
    "left ventricle": "cardiovascular", "right ventricle": "cardiovascular",
    "atrium": "cardiovascular", "valve": "cardiovascular",

    # Respiratory
    "lung": "respiratory", "lungs": "respiratory", "bronchus": "respiratory",
    "trachea": "respiratory", "pleura": "respiratory", "mediastinum": "respiratory",
    "diaphragm": "respiratory", "alveoli": "respiratory",

    # Gastrointestinal
    "liver": "gi", "gallbladder": "gi", "pancreas": "gi", "spleen": "gi",
    "stomach": "gi", "duodenum": "gi", "jejunum": "gi", "ileum": "gi",
    "colon": "gi", "rectum": "gi", "appendix": "gi", "esophagus": "gi",
    "small bowel": "gi", "large bowel": "gi", "mesentery": "gi",
    "peritoneum": "gi", "omentum": "gi",

    # Urinary / Renal
    "kidney": "renal", "kidneys": "renal", "ureter": "renal",
    "bladder": "renal", "urethra": "renal", "renal pelvis": "renal",
    "collecting system": "renal", "calyx": "renal", "calyces": "renal",

    # Reproductive
    "uterus": "reproductive", "ovary": "reproductive", "ovaries": "reproductive",
    "fallopian tube": "reproductive", "cervix": "reproductive",
    "prostate": "reproductive", "testis": "reproductive", "testes": "reproductive",
    "seminal vesicle": "reproductive", "epididymis": "reproductive",

    # Musculoskeletal
    "bone": "msk", "spine": "msk", "vertebra": "msk", "disc": "msk",
    "femur": "msk", "tibia": "msk", "humerus": "msk", "pelvis": "msk",
    "rib": "msk", "skull": "msk", "joint": "msk", "muscle": "msk",
    "tendon": "msk", "ligament": "msk", "cartilage": "msk",

    # Endocrine
    "thyroid": "endocrine", "adrenal": "endocrine", "parathyroid": "endocrine",
    "pineal": "endocrine",

    # Lymphatic / Haematological
    "lymph node": "lymphatic", "lymph nodes": "lymphatic", "spleen": "lymphatic",
    "bone marrow": "lymphatic",

    # Skin / Soft tissue
    "skin": "integumentary", "subcutaneous": "integumentary",
    "soft tissue": "integumentary",
}

# ── Scan Region → Allowed Systems ──
# When a scan says "MRI Brain", only these systems can have pathology

SCAN_REGION_SYSTEMS = {
    "brain": {"cns"},
    "head": {"cns", "msk", "endocrine"},
    "neck": {"endocrine", "lymphatic", "respiratory", "cardiovascular", "msk"},
    "chest": {"respiratory", "cardiovascular", "msk", "lymphatic"},
    "thorax": {"respiratory", "cardiovascular", "msk", "lymphatic"},
    "abdomen": {"gi", "renal", "lymphatic", "endocrine", "cardiovascular", "msk"},
    "pelvis": {"renal", "reproductive", "gi", "msk", "lymphatic"},
    "spine": {"cns", "msk"},
    "extremity": {"msk", "cardiovascular", "integumentary"},
    "whole body": {"cns", "cardiovascular", "respiratory", "gi", "renal",
                   "reproductive", "msk", "endocrine", "lymphatic", "integumentary"},
    "unknown": {"cns", "cardiovascular", "respiratory", "gi", "renal",
                "reproductive", "msk", "endocrine", "lymphatic", "integumentary"},
}

# ── Condition → Required System ──
# Each pathological condition belongs to specific organ system(s)

CONDITION_REQUIRED_SYSTEM = {
    # Renal-specific
    "hydronephrosis": {"renal"},
    "renal calculus": {"renal"},
    "nephrolithiasis": {"renal"},
    "renal cyst": {"renal"},
    "polycystic kidney": {"renal"},
    "renal cell carcinoma": {"renal"},
    "pyelonephritis": {"renal"},
    "renal artery stenosis": {"renal", "cardiovascular"},
    "ureteric calculus": {"renal"},
    "vesicoureteral reflux": {"renal"},
    "bladder mass": {"renal"},

    # Liver-specific
    "fatty liver": {"gi"},
    "hepatomegaly": {"gi"},
    "cirrhosis": {"gi"},
    "hepatic mass": {"gi"},
    "portal hypertension": {"gi", "cardiovascular"},
    "hepatic steatosis": {"gi"},
    "hepatocellular carcinoma": {"gi"},
    "cholecystitis": {"gi"},
    "cholelithiasis": {"gi"},
    "biliary dilatation": {"gi"},
    "pancreatitis": {"gi"},

    # Lung-specific
    "consolidation": {"respiratory"},
    "pleural effusion": {"respiratory"},
    "pneumothorax": {"respiratory"},
    "pulmonary embolism": {"respiratory", "cardiovascular"},
    "ground glass": {"respiratory"},
    "lung mass": {"respiratory"},
    "bronchiectasis": {"respiratory"},
    "atelectasis": {"respiratory"},
    "emphysema": {"respiratory"},
    "pulmonary fibrosis": {"respiratory"},

    # Brain-specific
    "brain infarct": {"cns"},
    "cerebral infarct": {"cns"},
    "intracranial hemorrhage": {"cns"},
    "brain mass": {"cns"},
    "glioma": {"cns"},
    "meningioma": {"cns"},
    "hydrocephalus": {"cns"},
    "cerebral atrophy": {"cns"},
    "demyelination": {"cns"},
    "encephalitis": {"cns"},
    "subdural hematoma": {"cns"},
    "epidural hematoma": {"cns"},
    "subarachnoid hemorrhage": {"cns"},

    # Heart-specific
    "cardiomegaly": {"cardiovascular"},
    "pericardial effusion": {"cardiovascular"},
    "myocardial infarction": {"cardiovascular"},
    "aortic aneurysm": {"cardiovascular"},
    "valve calcification": {"cardiovascular"},

    # MSK-specific
    "fracture": {"msk"},
    "osteoporosis": {"msk"},
    "disc herniation": {"msk"},
    "spondylosis": {"msk"},
    "osteomyelitis": {"msk"},
    "bone mass": {"msk"},

    # Endocrine
    "thyroid nodule": {"endocrine"},
    "adrenal mass": {"endocrine"},

    # Lymphatic
    "lymphadenopathy": {"lymphatic", "cns", "respiratory", "gi", "renal",
                         "reproductive", "msk"},  # can occur anywhere

    # GI
    "ascites": {"gi", "cardiovascular"},
    "splenomegaly": {"gi", "lymphatic"},
    "appendicitis": {"gi"},
    "bowel obstruction": {"gi"},
    "colitis": {"gi"},
    "diverticulitis": {"gi"},

    # Reproductive
    "ovarian cyst": {"reproductive"},
    "uterine fibroid": {"reproductive"},
    "prostatic enlargement": {"reproductive"},
}

# ── Biomarker → System ──
# Which organ system each biomarker belongs to

BIOMARKER_SYSTEM = {
    "haemoglobin": "haematological", "total_wbc_count": "haematological",
    "esr": "haematological", "platelet_count": "haematological",
    "rdw": "haematological", "mcv": "haematological",
    "total_cholesterol": "cardiovascular", "ldl_cholesterol": "cardiovascular",
    "hdl_cholesterol": "cardiovascular", "triglycerides": "cardiovascular",
    "sgot_ast": "gi", "sgpt_alt": "gi", "ggt": "gi",
    "total_bilirubin": "gi", "direct_bilirubin": "gi",
    "alkaline_phosphatase": "gi", "albumin": "gi",
    "tsh": "endocrine", "free_t3": "endocrine", "free_t4": "endocrine",
    "serum_creatinine": "renal", "bun": "renal", "egfr": "renal",
    "uric_acid": "renal", "sodium": "renal", "potassium": "renal",
    "fasting_blood_sugar": "endocrine", "hba1c": "endocrine",
    "vitamin_d": "msk", "vitamin_b12": "haematological",
    "iron_serum": "haematological", "ferritin": "haematological",
    "crp": "inflammatory", "procalcitonin": "inflammatory",
    "cd4_count": "immunological", "d_dimer": "cardiovascular",
    "psa": "reproductive", "ca125": "reproductive",
    "cea": "gi", "afp": "gi", "ca199": "gi",
    "pt": "haematological", "inr": "haematological",
    "aptt": "haematological", "fibrinogen": "haematological",
    "ldh": "general",  # non-specific
}


# ── Validation Functions ──

def validate_condition_in_region(condition: str, scan_region: str) -> dict:
    """
    Check if a pathological condition is anatomically valid for the scan region.

    Returns:
        {
            "valid": bool,
            "condition": str,
            "scan_region": str,
            "required_systems": set,
            "allowed_systems": set,
            "error_type": str or None,  # "anatomical_mismatch" / None
            "message": str
        }
    """
    condition_lower = condition.lower().strip()
    region_lower = scan_region.lower().strip()

    # Get required systems for this condition
    required = None
    for cond_key, systems in CONDITION_REQUIRED_SYSTEM.items():
        if cond_key in condition_lower or condition_lower in cond_key:
            required = systems
            break

    if required is None:
        return {
            "valid": True,
            "condition": condition,
            "scan_region": scan_region,
            "required_systems": set(),
            "allowed_systems": set(),
            "error_type": None,
            "message": "Condition not in validation database — manual review recommended"
        }

    # Get allowed systems for scan region
    allowed = None
    for region_key, systems in SCAN_REGION_SYSTEMS.items():
        if region_key in region_lower or region_lower in region_key:
            allowed = systems
            break

    if allowed is None:
        allowed = SCAN_REGION_SYSTEMS["unknown"]

    # Check overlap
    overlap = required & allowed
    if overlap:
        return {
            "valid": True,
            "condition": condition,
            "scan_region": scan_region,
            "required_systems": required,
            "allowed_systems": allowed,
            "error_type": None,
            "message": f"Anatomically valid: {condition} can occur in {scan_region} region"
        }
    else:
        return {
            "valid": False,
            "condition": condition,
            "scan_region": scan_region,
            "required_systems": required,
            "allowed_systems": allowed,
            "error_type": "anatomical_mismatch",
            "message": (
                f"ANATOMICAL INCONSISTENCY: '{condition}' requires {required} system(s), "
                f"but '{scan_region}' scan covers {allowed}. "
                f"This finding is NOT biologically possible in this region."
            )
        }


def validate_radiology_findings(findings: list[dict], scan_region: str) -> list[dict]:
    """
    Validate a list of radiology findings against the scan region.

    Args:
        findings: list of {"finding": str, "body_region": str, ...}
        scan_region: str (e.g., "Brain", "Abdomen")

    Returns:
        List of validation results with "valid", "error_type", "message"
    """
    results = []
    for f in findings:
        finding_text = f.get("finding", "") or f.get("body_region", "")
        result = validate_condition_in_region(finding_text, scan_region)
        result["original_finding"] = f
        results.append(result)
    return results


def get_valid_conditions_for_region(scan_region: str) -> list[str]:
    """Return all conditions that are anatomically valid for a given scan region."""
    region_lower = scan_region.lower()
    allowed_systems = None
    for region_key, systems in SCAN_REGION_SYSTEMS.items():
        if region_key in region_lower or region_lower in region_key:
            allowed_systems = systems
            break
    if not allowed_systems:
        return []

    valid = []
    for condition, required_systems in CONDITION_REQUIRED_SYSTEM.items():
        if required_systems & allowed_systems:
            valid.append(condition)
    return sorted(valid)


def get_system_for_organ(organ: str) -> str:
    """Look up which system an organ belongs to."""
    organ_lower = organ.lower().strip()
    return ORGAN_TO_SYSTEM.get(organ_lower, "unknown")

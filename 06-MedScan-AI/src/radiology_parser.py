"""
Radiology Text Report Parser
===============================
Parses written findings from CT/MRI/X-ray reports (radiologist's text).
Extracts structured findings and cross-references with blood biomarkers.
"""

import re
from dataclasses import dataclass, field


@dataclass
class RadiologyFinding:
    body_region: str
    finding: str
    severity: str
    category: str
    related_biomarkers: list[str] = field(default_factory=list)
    recommended_correlation: str = ""


@dataclass
class RadiologyReport:
    modality: str
    body_part: str
    findings: list[RadiologyFinding] = field(default_factory=list)
    impression: str = ""
    raw_text: str = ""


FINDING_PATTERNS = {
    "fatty liver": {
        "region": "Liver", "severity": "mild", "category": "structural",
        "biomarkers": ["sgpt_alt", "sgot_ast", "ggt", "triglycerides", "hba1c"],
        "correlation": "Check ALT, AST, GGT, lipid panel, HbA1c for NAFLD confirmation"
    },
    "hepatomegaly": {
        "region": "Liver", "severity": "moderate", "category": "structural",
        "biomarkers": ["sgpt_alt", "sgot_ast", "ggt", "alkaline_phosphatase", "total_bilirubin"],
        "correlation": "Full LFT panel + hepatitis serology + liver ultrasound"
    },
    "cirrhosis": {
        "region": "Liver", "severity": "severe", "category": "structural",
        "biomarkers": ["albumin", "total_bilirubin", "pt", "inr", "platelet_count", "afp"],
        "correlation": "Child-Pugh score (albumin, bilirubin, INR, ascites, encephalopathy) + AFP for HCC screening"
    },
    "hepatic mass": {
        "region": "Liver", "severity": "severe", "category": "neoplastic",
        "biomarkers": ["afp", "sgpt_alt", "total_bilirubin", "ldh"],
        "correlation": "AFP + triphasic CT/MRI + biopsy if needed"
    },
    "pleural effusion": {
        "region": "Lungs", "severity": "moderate", "category": "inflammatory",
        "biomarkers": ["total_protein", "albumin", "ldh", "ada"],
        "correlation": "Pleural fluid analysis (Light's criteria: protein, LDH) + ADA for TB"
    },
    "consolidation": {
        "region": "Lungs", "severity": "moderate", "category": "inflammatory",
        "biomarkers": ["total_wbc_count", "crp", "procalcitonin"],
        "correlation": "CBC + CRP + Procalcitonin + sputum culture"
    },
    "ground glass": {
        "region": "Lungs", "severity": "moderate", "category": "inflammatory",
        "biomarkers": ["crp", "d_dimer", "il6", "ferritin", "ldh"],
        "correlation": "COVID-19 markers (CRP, D-dimer, IL-6, ferritin, LDH) if clinical suspicion"
    },
    "pulmonary embolism": {
        "region": "Lungs", "severity": "severe", "category": "vascular",
        "biomarkers": ["d_dimer", "pt", "inr"],
        "correlation": "D-dimer + CT pulmonary angiography + coagulation panel"
    },
    "lung mass": {
        "region": "Lungs", "severity": "severe", "category": "neoplastic",
        "biomarkers": ["cea", "ldh", "crp"],
        "correlation": "CEA + LDH + biopsy + PET-CT staging"
    },
    "lymphadenopathy": {
        "region": "Lymph Nodes", "severity": "moderate", "category": "neoplastic",
        "biomarkers": ["ldh", "crp", "esr", "total_wbc_count"],
        "correlation": "LDH (lymphoma marker) + CBC + ESR + CRP + biopsy if persistent >6 weeks"
    },
    "splenomegaly": {
        "region": "Spleen", "severity": "moderate", "category": "structural",
        "biomarkers": ["platelet_count", "total_wbc_count", "ldh", "total_bilirubin"],
        "correlation": "CBC (cytopenias) + LFT + peripheral smear + infection workup"
    },
    "renal calculus": {
        "region": "Kidney", "severity": "mild", "category": "structural",
        "biomarkers": ["serum_creatinine", "uric_acid", "calcium", "phosphorus"],
        "correlation": "Renal function panel + uric acid + calcium + 24-hr urine stone analysis"
    },
    "hydronephrosis": {
        "region": "Kidney", "severity": "moderate", "category": "structural",
        "biomarkers": ["serum_creatinine", "bun", "egfr", "potassium"],
        "correlation": "Renal function panel + electrolytes + urology referral"
    },
    "brain infarct": {
        "region": "Brain", "severity": "severe", "category": "vascular",
        "biomarkers": ["total_cholesterol", "ldl_cholesterol", "hba1c", "pt", "inr"],
        "correlation": "Lipid panel + HbA1c + coagulation + echocardiography"
    },
    "brain mass": {
        "region": "Brain", "severity": "severe", "category": "neoplastic",
        "biomarkers": ["ldh", "cea", "sodium"],
        "correlation": "Systemic tumour markers if metastasis suspected + neurosurgery referral"
    },
    "osteoporosis": {
        "region": "Bone", "severity": "moderate", "category": "degenerative",
        "biomarkers": ["vitamin_d", "calcium", "phosphorus", "alkaline_phosphatase", "tsh"],
        "correlation": "Vitamin D + calcium + ALP + thyroid panel + DEXA scan"
    },
    "fracture": {
        "region": "Bone", "severity": "moderate", "category": "structural",
        "biomarkers": ["calcium", "vitamin_d", "alkaline_phosphatase"],
        "correlation": "Calcium + Vitamin D + ALP if pathological fracture suspected"
    },
    "thyroid nodule": {
        "region": "Thyroid", "severity": "mild", "category": "neoplastic",
        "biomarkers": ["tsh", "free_t3", "free_t4"],
        "correlation": "TSH + thyroid function + FNAC (fine needle aspiration cytology) per TIRADS"
    },
    "ascites": {
        "region": "Abdomen", "severity": "moderate", "category": "structural",
        "biomarkers": ["albumin", "total_protein", "total_bilirubin", "crp", "ca125"],
        "correlation": "SAAG (serum-ascites albumin gradient) + ascitic fluid analysis + LFT"
    },
    "cardiomegaly": {
        "region": "Heart", "severity": "moderate", "category": "structural",
        "biomarkers": ["crp", "tsh"],
        "correlation": "Echocardiography + BNP/NT-proBNP + thyroid function"
    },
}

MODALITY_KEYWORDS = {
    "ct": ["ct scan", "computed tomography", "hrct", "cect", "ncct", "ct angiography", "ctpa"],
    "mri": ["mri", "magnetic resonance", "mr imaging", "flair", "dwi", "t1w", "t2w"],
    "xray": ["x-ray", "x ray", "xray", "radiograph", "chest pa", "ap view"],
    "ultrasound": ["ultrasound", "usg", "sonography", "doppler"],
}

BODY_PART_KEYWORDS = {
    "chest": ["chest", "thorax", "lung", "pulmonary", "mediastinum"],
    "abdomen": ["abdomen", "abdominal", "liver", "spleen", "kidney", "pancreas", "gallbladder"],
    "brain": ["brain", "head", "cranial", "intracranial", "cerebral"],
    "spine": ["spine", "spinal", "lumbar", "cervical", "thoracic", "vertebr"],
    "pelvis": ["pelvis", "pelvic", "uterus", "ovary", "prostate", "bladder"],
    "extremity": ["extremity", "femur", "tibia", "humerus", "wrist", "ankle", "knee", "shoulder"],
}


def detect_modality(text: str) -> str:
    text_lower = text.lower()
    for modality, keywords in MODALITY_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            return modality.upper()
    return "Unknown"


def detect_body_part(text: str) -> str:
    text_lower = text.lower()
    for part, keywords in BODY_PART_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            return part.capitalize()
    return "Unknown"


def extract_impression(text: str) -> str:
    patterns = [
        r"(?:IMPRESSION|CONCLUSION|OPINION|SUMMARY)\s*[:\-]?\s*(.*?)(?:\n\n|\Z)",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE | re.DOTALL)
        if m:
            return m.group(1).strip()[:500]
    return ""


def parse_radiology_report(text: str) -> RadiologyReport:
    """Parse a radiology text report into structured findings."""
    text_lower = text.lower()

    modality = detect_modality(text)
    body_part = detect_body_part(text)
    impression = extract_impression(text)

    findings = []
    for pattern_key, pattern_data in FINDING_PATTERNS.items():
        if pattern_key in text_lower:
            # Extract the sentence containing the finding
            sentences = re.split(r'[.;]\s', text)
            relevant = [s.strip() for s in sentences if pattern_key in s.lower()]
            finding_text = relevant[0] if relevant else f"{pattern_key} noted"

            # Detect severity modifiers
            severity = pattern_data["severity"]
            if any(w in text_lower for w in ["mild", "minimal", "subtle", "trace"]):
                if pattern_key in text_lower.split("mild")[0][-50:] if "mild" in text_lower else False:
                    severity = "mild"
            if any(w in text_lower for w in ["moderate", "significant"]):
                severity = "moderate"
            if any(w in text_lower for w in ["severe", "extensive", "massive", "large"]):
                severity = "severe"

            findings.append(RadiologyFinding(
                body_region=pattern_data["region"],
                finding=finding_text[:200],
                severity=severity,
                category=pattern_data["category"],
                related_biomarkers=pattern_data["biomarkers"],
                recommended_correlation=pattern_data["correlation"],
            ))

    return RadiologyReport(
        modality=modality,
        body_part=body_part,
        findings=findings,
        impression=impression,
        raw_text=text,
    )


def correlate_with_bloodwork(rad_report: RadiologyReport, abnormal_biomarkers: set[str]) -> list[dict]:
    """Cross-reference radiology findings with abnormal blood biomarkers."""
    correlations = []
    for finding in rad_report.findings:
        matched = [b for b in finding.related_biomarkers if b in abnormal_biomarkers]
        if matched:
            correlations.append({
                "finding": finding.finding,
                "region": finding.body_region,
                "matching_biomarkers": matched,
                "correlation_note": finding.recommended_correlation,
                "confidence": "high" if len(matched) >= 2 else "moderate",
            })
    return correlations

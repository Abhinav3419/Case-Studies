"""
PDF Clinical Report Extraction Engine
=======================================
Extracts structured biomarker data from clinical laboratory report PDFs.

Strategy:
1. Extract raw text using pdfplumber (layout-aware)
2. Extract tables using pdfplumber table detection
3. Parse extracted content into structured biomarker records
4. Validate against clinical reference ranges
5. Output clean JSON with flags and metadata

Handles multiple Indian lab formats: Thyrocare, Dr. Lal PathLabs, SRL, Metropolis, etc.
"""

import re
import json
import os
from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime

import pdfplumber

from .clinical_references import REFERENCE_RANGES, get_reference, get_all_aliases


# ============================================================
# DATA MODELS
# ============================================================

@dataclass
class PatientInfo:
    name: str = ""
    age: str = ""
    sex: str = ""
    patient_id: str = ""
    sample_id: str = ""
    referred_by: str = ""
    collection_date: str = ""
    report_date: str = ""
    sample_type: str = ""
    lab_name: str = ""


@dataclass
class BiomarkerResult:
    test_name: str                     # As printed on report
    canonical_name: str = ""           # Standardized name from our reference DB
    value: Optional[float] = None      # Numeric value
    value_raw: str = ""                # Raw string as extracted
    unit: str = ""
    reference_range_reported: str = "" # Range as printed on report
    reference_range_standard: str = "" # Our validated standard range
    flag: str = ""                     # HIGH / LOW / NORMAL / CRITICAL
    category: str = ""                 # CBC, Lipid, Liver, etc.
    is_abnormal: bool = False
    is_critical: bool = False
    deviation_pct: float = 0.0         # How far from normal (% deviation)
    interpretation_band: str = ""       # e.g., "prediabetes", "deficient"
    description: str = ""              # What this test measures


@dataclass
class ExtractionResult:
    patient: PatientInfo
    biomarkers: list[BiomarkerResult] = field(default_factory=list)
    sections_found: list[str] = field(default_factory=list)
    total_tests: int = 0
    abnormal_count: int = 0
    critical_count: int = 0
    extraction_method: str = ""
    raw_text: str = ""
    extraction_timestamp: str = ""
    source_file: str = ""
    warnings: list[str] = field(default_factory=list)


# ============================================================
# TEXT EXTRACTION
# ============================================================

def extract_text_from_pdf(pdf_path: str) -> tuple[str, list[list[list[str]]]]:
    """
    Extract both raw text and tables from a PDF.
    Returns (full_text, list_of_tables_per_page).
    """
    full_text = ""
    all_tables = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract text
            text = page.extract_text() or ""
            full_text += text + "\n\n"

            # Extract tables
            tables = page.extract_tables() or []
            all_tables.extend(tables)

    return full_text.strip(), all_tables


# ============================================================
# PATIENT INFO PARSING
# ============================================================

def parse_patient_info(text: str) -> PatientInfo:
    """Extract patient demographic information from report text."""
    patient = PatientInfo()

    # Name patterns
    name_patterns = [
        r"(?:Patient\s*Name|Name)\s*[:\-]\s*(.+?)(?:\n|$|Age|Sex|Patient\s*ID)",
        r"Name:\s*(.+?)(?:\s{2,}|\n|$)",
    ]
    for pat in name_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            patient.name = m.group(1).strip().rstrip(',').strip()
            break

    # Age
    age_patterns = [
        r"(?:Age)\s*[:/\-]\s*(\d+\s*(?:Yrs?|Years?|Y))",
        r"Age/Sex\s*[:\-]\s*(\d+\s*(?:Yrs?|Years?|Y))",
        r"(\d+)\s*(?:Yrs?|Years?)\s*/",
    ]
    for pat in age_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            patient.age = m.group(1).strip()
            break

    # Sex/Gender
    sex_patterns = [
        r"(?:Sex|Gender)\s*[:\-]\s*(Male|Female|M|F)",
        r"Age/Sex\s*[:\-]\s*\d+\s*(?:Yrs?|Years?|Y)\s*/\s*(Male|Female|M|F)",
        r"/\s*(Male|Female|M|F)\b",
    ]
    for pat in sex_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            sex = m.group(1).strip().upper()
            patient.sex = "Male" if sex in ("M", "MALE") else "Female"
            break

    # Patient ID
    id_patterns = [
        r"(?:Patient\s*ID|PID|Reg\.?\s*No|Registration)\s*[:\-]\s*([A-Za-z0-9\-/]+)",
        r"Barcode\s*[:\-]\s*(\d+)",
    ]
    for pat in id_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            patient.patient_id = m.group(1).strip()
            break

    # Sample ID
    m = re.search(r"(?:Sample\s*ID|Specimen\s*ID)\s*[:\-]\s*([A-Za-z0-9\-/]+)", text, re.IGNORECASE)
    if m:
        patient.sample_id = m.group(1).strip()

    # Referred By
    m = re.search(r"(?:Ref\.?\s*(?:By|Doctor|Dr)|Referred\s*By|Doctor)\s*[:\-]\s*(.+?)(?:\n|$|\s{2,})", text, re.IGNORECASE)
    if m:
        patient.referred_by = m.group(1).strip()

    # Collection Date
    date_patterns = [
        r"(?:Collection\s*Date|Sample\s*Date|Collected\s*On)\s*[:\-]\s*(.+?)(?:\n|$|\s{2,})",
    ]
    for pat in date_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            patient.collection_date = m.group(1).strip()
            break

    # Report Date
    m = re.search(r"(?:Report\s*Date|Reported\s*On|Date\s*of\s*Report)\s*[:\-]\s*(.+?)(?:\n|$|\s{2,})", text, re.IGNORECASE)
    if m:
        patient.report_date = m.group(1).strip()

    # Sample Type
    m = re.search(r"(?:Sample\s*Type|Specimen)\s*[:\-]\s*(.+?)(?:\n|$)", text, re.IGNORECASE)
    if m:
        patient.sample_type = m.group(1).strip()

    # Lab Name (usually the first or second line)
    lines = text.strip().split('\n')
    for line in lines[:5]:
        line = line.strip()
        if len(line) > 5 and line.upper() == line and not any(kw in line.lower() for kw in ['test', 'result', 'reference', 'unit']):
            patient.lab_name = line.title()
            break

    return patient


# ============================================================
# BIOMARKER EXTRACTION FROM TABLES
# ============================================================

def _clean_cell(cell: str | None) -> str:
    """Clean a table cell value."""
    if cell is None:
        return ""
    return str(cell).strip().replace('\n', ' ').strip()


def _parse_numeric(value_str: str) -> Optional[float]:
    """Parse a numeric value from a string, handling commas and spaces."""
    if not value_str:
        return None
    # Remove commas, spaces
    cleaned = value_str.replace(',', '').replace(' ', '').strip()
    # Handle ranges like "< 200" or "> 40"
    cleaned = re.sub(r'^[<>≤≥]\s*', '', cleaned)
    try:
        return float(cleaned)
    except ValueError:
        return None


def _match_to_reference(test_name: str) -> tuple[str, dict | None]:
    """Match an extracted test name to our reference database."""
    name_lower = test_name.lower().strip()

    # Remove parenthetical content for matching, but keep it for secondary checks
    name_clean = re.sub(r'\([^)]*\)', '', name_lower).strip()
    # Also extract parenthetical content as secondary match target
    parens = re.findall(r'\(([^)]*)\)', name_lower)
    paren_text = ' '.join(p.lower() for p in parens)

    alias_map = get_all_aliases()

    # Try exact match on full name first
    if name_lower in alias_map:
        canonical = alias_map[name_lower]
        return canonical, REFERENCE_RANGES[canonical]

    # Try exact match on cleaned name
    if name_clean in alias_map:
        canonical = alias_map[name_clean]
        return canonical, REFERENCE_RANGES[canonical]

    # Try exact match on parenthetical content (e.g., "AST", "ALT", "PCV")
    if paren_text and paren_text in alias_map:
        canonical = alias_map[paren_text]
        return canonical, REFERENCE_RANGES[canonical]

    # Try partial match — but require the alias to be a substantial match
    best_partial = None
    best_partial_len = 0
    for alias, canonical in alias_map.items():
        # Alias contained in the test name
        if len(alias) >= 3 and alias in name_clean:
            if len(alias) > best_partial_len:
                best_partial_len = len(alias)
                best_partial = (canonical, REFERENCE_RANGES[canonical])
        # Test name contained in alias
        elif len(name_clean) >= 3 and name_clean in alias:
            if len(name_clean) > best_partial_len:
                best_partial_len = len(name_clean)
                best_partial = (canonical, REFERENCE_RANGES[canonical])
        # Check paren text too
        if paren_text and len(paren_text) >= 2 and paren_text in alias:
            if len(paren_text) > best_partial_len:
                best_partial_len = len(paren_text)
                best_partial = (canonical, REFERENCE_RANGES[canonical])

    if best_partial:
        return best_partial

    # Try word-level matching with stricter threshold
    name_words = set(name_clean.split())
    best_match = None
    best_score = 0
    best_alias_len = 0
    for alias, canonical in alias_map.items():
        alias_words = set(alias.split())
        overlap = len(name_words & alias_words)
        # Require at least all alias words to match if alias is short
        min_required = len(alias_words) if len(alias_words) <= 2 else len(alias_words) - 1
        if overlap >= min_required and overlap > 0:
            # Prefer longer alias matches (more specific)
            if overlap > best_score or (overlap == best_score and len(alias) > best_alias_len):
                best_score = overlap
                best_alias_len = len(alias)
                best_match = (canonical, REFERENCE_RANGES[canonical])

    if best_match:
        return best_match

    return "", None


def _determine_flag(value: float, ref_data: dict, sex: str = "male") -> tuple[str, bool, bool, float, str]:
    """
    Determine if a biomarker value is normal, high, low, or critical.
    Returns (flag, is_abnormal, is_critical, deviation_pct, interpretation_band).
    """
    sex_key = sex.lower() if sex.lower() in ("male", "female") else "all"

    # Get reference range
    ref_range = ref_data.get("ref_range", {})
    if sex_key in ref_range:
        low, high = ref_range[sex_key]
    elif "all" in ref_range:
        low, high = ref_range["all"]
    else:
        return "UNKNOWN", False, False, 0.0, ""

    # Determine flag
    flag = "NORMAL"
    is_abnormal = False
    is_critical = False
    deviation_pct = 0.0

    if value < low:
        flag = "LOW"
        is_abnormal = True
        deviation_pct = round(((low - value) / low) * 100, 1) if low > 0 else 0.0
        critical_low = ref_data.get("critical_low")
        if critical_low is not None and value <= critical_low:
            flag = "CRITICAL_LOW"
            is_critical = True
    elif value > high:
        flag = "HIGH"
        is_abnormal = True
        deviation_pct = round(((value - high) / high) * 100, 1) if high > 0 else 0.0
        critical_high = ref_data.get("critical_high")
        if critical_high is not None and value >= critical_high:
            flag = "CRITICAL_HIGH"
            is_critical = True

    # Interpretation band
    band = ""
    if "interpretation_bands" in ref_data:
        for band_name, (band_low, band_high) in ref_data["interpretation_bands"].items():
            if band_low <= value <= band_high:
                band = band_name
                break

    return flag, is_abnormal, is_critical, deviation_pct, band


def extract_biomarkers_from_tables(tables: list[list[list[str]]], sex: str = "male") -> list[BiomarkerResult]:
    """
    Parse structured tables into BiomarkerResult objects.
    Handles various table formats from different Indian labs.
    """
    results = []

    for table in tables:
        if not table or len(table) < 2:
            continue

        # Identify header row
        header = [_clean_cell(c).lower() for c in table[0]]

        # Find column indices
        name_col = None
        value_col = None
        unit_col = None
        ref_col = None
        flag_col = None

        for i, h in enumerate(header):
            if any(kw in h for kw in ['test', 'investigation', 'parameter', 'analyte', 'name']):
                name_col = i
            elif any(kw in h for kw in ['result', 'value', 'observed']):
                value_col = i
            elif any(kw in h for kw in ['unit']):
                unit_col = i
            elif any(kw in h for kw in ['reference', 'ref', 'range', 'biological', 'normal', 'desirable']):
                ref_col = i
            elif any(kw in h for kw in ['flag', 'remark', 'status', 'interpretation']):
                flag_col = i

        # If we couldn't identify columns, try positional heuristic
        if name_col is None and len(header) >= 3:
            name_col = 0
            value_col = 1
            if len(header) >= 4:
                unit_col = 2
                ref_col = 3
            else:
                ref_col = 2

        if name_col is None or value_col is None:
            continue

        # Parse data rows
        for row in table[1:]:
            if len(row) <= max(name_col, value_col):
                continue

            test_name = _clean_cell(row[name_col])
            value_raw = _clean_cell(row[value_col]) if value_col < len(row) else ""
            unit = _clean_cell(row[unit_col]) if unit_col is not None and unit_col < len(row) else ""
            ref_range_str = _clean_cell(row[ref_col]) if ref_col is not None and ref_col < len(row) else ""
            flag_reported = _clean_cell(row[flag_col]) if flag_col is not None and flag_col < len(row) else ""

            # Skip if no valid test name or value
            if not test_name or not value_raw:
                continue
            if test_name.lower() in ['test name', 'investigation', 'parameter', '']:
                continue

            value = _parse_numeric(value_raw)

            # Match to reference database
            canonical, ref_data = _match_to_reference(test_name)

            # Determine flag
            flag = ""
            is_abnormal = False
            is_critical = False
            deviation_pct = 0.0
            interp_band = ""
            ref_range_standard = ""
            description = ""
            category = ""

            if ref_data and value is not None:
                flag, is_abnormal, is_critical, deviation_pct, interp_band = _determine_flag(
                    value, ref_data, sex
                )
                sex_key = sex.lower() if sex.lower() in ("male", "female") else "all"
                rr = ref_data.get("ref_range", {})
                if sex_key in rr:
                    ref_range_standard = f"{rr[sex_key][0]} - {rr[sex_key][1]}"
                elif "all" in rr:
                    ref_range_standard = f"{rr['all'][0]} - {rr['all'][1]}"
                description = ref_data.get("description", "")
                category = ref_data.get("category", "")
            elif flag_reported:
                flag = flag_reported.upper()
                is_abnormal = flag in ("HIGH", "LOW", "ABNORMAL")

            results.append(BiomarkerResult(
                test_name=test_name,
                canonical_name=canonical,
                value=value,
                value_raw=value_raw,
                unit=unit,
                reference_range_reported=ref_range_str,
                reference_range_standard=ref_range_standard,
                flag=flag,
                category=category,
                is_abnormal=is_abnormal,
                is_critical=is_critical,
                deviation_pct=deviation_pct,
                interpretation_band=interp_band,
                description=description,
            ))

    return results


# ============================================================
# FALLBACK: REGEX-BASED EXTRACTION FROM RAW TEXT
# ============================================================

def extract_biomarkers_from_text(text: str, sex: str = "male") -> list[BiomarkerResult]:
    """
    Fallback extraction using regex patterns on raw text.
    Used when table extraction fails or misses entries.
    """
    results = []
    alias_map = get_all_aliases()

    # Pattern: Test Name ... numeric_value ... unit ... ref_range
    # Handles various separators: spaces, tabs, colons, dashes
    line_pattern = re.compile(
        r'^(.+?)\s+'                     # Test name
        r'(\d+[\d,]*\.?\d*)\s+'          # Result value
        r'([a-zA-Zµ/%°·²³]+(?:/[a-zA-Zµ/%°·²³]+)*)\s+'  # Unit
        r'(.+?)$',                        # Reference range
        re.MULTILINE
    )

    for match in line_pattern.finditer(text):
        test_name = match.group(1).strip().rstrip(':').strip()
        value_raw = match.group(2).strip()
        unit = match.group(3).strip()
        ref_range_str = match.group(4).strip()

        value = _parse_numeric(value_raw)
        canonical, ref_data = _match_to_reference(test_name)

        if not canonical:
            continue  # Skip unrecognized tests in fallback mode

        flag = ""
        is_abnormal = False
        is_critical = False
        deviation_pct = 0.0
        interp_band = ""
        ref_range_standard = ""
        description = ""
        category = ""

        if ref_data and value is not None:
            flag, is_abnormal, is_critical, deviation_pct, interp_band = _determine_flag(
                value, ref_data, sex
            )
            sex_key = sex.lower() if sex.lower() in ("male", "female") else "all"
            rr = ref_data.get("ref_range", {})
            if sex_key in rr:
                ref_range_standard = f"{rr[sex_key][0]} - {rr[sex_key][1]}"
            elif "all" in rr:
                ref_range_standard = f"{rr['all'][0]} - {rr['all'][1]}"
            description = ref_data.get("description", "")
            category = ref_data.get("category", "")

        results.append(BiomarkerResult(
            test_name=test_name,
            canonical_name=canonical,
            value=value,
            value_raw=value_raw,
            unit=unit,
            reference_range_reported=ref_range_str,
            reference_range_standard=ref_range_standard,
            flag=flag,
            category=category,
            is_abnormal=is_abnormal,
            is_critical=is_critical,
            deviation_pct=deviation_pct,
            interpretation_band=interp_band,
            description=description,
        ))

    return results


# ============================================================
# SECTION DETECTION
# ============================================================

def detect_sections(text: str) -> list[str]:
    """Detect clinical test section headers in the report."""
    section_keywords = [
        "complete blood count", "cbc", "haemogram",
        "lipid profile", "lipid panel",
        "liver function", "lft", "hepatic",
        "thyroid", "thyroid function", "thyroid profile",
        "kidney function", "kft", "rft", "renal",
        "blood glucose", "blood sugar", "diabetes",
        "vitamin", "mineral", "iron studies",
        "urine", "urinalysis",
        "electrolyte",
        "coagulation",
        "cardiac markers",
        "hormone",
    ]

    found = []
    text_lower = text.lower()
    for kw in section_keywords:
        if kw in text_lower:
            found.append(kw.upper())

    return list(set(found))


# ============================================================
# MAIN EXTRACTION PIPELINE
# ============================================================

def extract_report(pdf_path: str) -> ExtractionResult:
    """
    Main extraction pipeline.
    
    Args:
        pdf_path: Path to the clinical lab report PDF.
    
    Returns:
        ExtractionResult with structured biomarker data.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    # Step 1: Extract raw text and tables
    raw_text, tables = extract_text_from_pdf(pdf_path)

    # Step 2: Parse patient info
    patient = parse_patient_info(raw_text)

    # Determine sex for reference ranges
    sex = patient.sex.lower() if patient.sex else "male"

    # Step 3: Extract biomarkers from tables (primary method)
    biomarkers = extract_biomarkers_from_tables(tables, sex)

    # Step 4: If table extraction found fewer than expected, try text fallback
    warnings = []
    extraction_method = "table"

    if len(biomarkers) < 3:
        text_biomarkers = extract_biomarkers_from_text(raw_text, sex)
        if len(text_biomarkers) > len(biomarkers):
            biomarkers = text_biomarkers
            extraction_method = "text_regex"
            warnings.append("Table extraction yielded few results; fell back to text-based extraction.")
        elif text_biomarkers:
            # Merge: add any text-extracted markers not already found
            existing_names = {b.canonical_name for b in biomarkers}
            for tb in text_biomarkers:
                if tb.canonical_name and tb.canonical_name not in existing_names:
                    biomarkers.append(tb)
                    existing_names.add(tb.canonical_name)
            extraction_method = "table+text"

    # Step 5: Detect sections
    sections = detect_sections(raw_text)

    # Step 6: Deduplicate (keep first occurrence if duplicate canonical names)
    seen = set()
    deduped = []
    for b in biomarkers:
        key = b.canonical_name or b.test_name.lower()
        if key not in seen:
            seen.add(key)
            deduped.append(b)
    biomarkers = deduped

    # Step 7: Compile result
    abnormal_count = sum(1 for b in biomarkers if b.is_abnormal)
    critical_count = sum(1 for b in biomarkers if b.is_critical)

    return ExtractionResult(
        patient=patient,
        biomarkers=biomarkers,
        sections_found=sections,
        total_tests=len(biomarkers),
        abnormal_count=abnormal_count,
        critical_count=critical_count,
        extraction_method=extraction_method,
        raw_text=raw_text,
        extraction_timestamp=datetime.now().isoformat(),
        source_file=os.path.basename(pdf_path),
        warnings=warnings,
    )


# ============================================================
# OUTPUT FORMATTING
# ============================================================

def result_to_json(result: ExtractionResult, include_raw_text: bool = False) -> str:
    """Convert ExtractionResult to formatted JSON string."""
    data = asdict(result)
    if not include_raw_text:
        data.pop("raw_text", None)
    return json.dumps(data, indent=2, ensure_ascii=False)


def result_to_summary(result: ExtractionResult) -> str:
    """Generate a human-readable summary of the extraction."""
    lines = []
    lines.append("=" * 70)
    lines.append("   MEDSCAN AI — Clinical Report Extraction Summary")
    lines.append("=" * 70)

    # Patient Info
    p = result.patient
    lines.append(f"\n📋 PATIENT: {p.name or 'N/A'}")
    lines.append(f"   Age: {p.age or 'N/A'} | Sex: {p.sex or 'N/A'}")
    lines.append(f"   Lab: {p.lab_name or 'N/A'}")
    lines.append(f"   Collection: {p.collection_date or 'N/A'} | Report: {p.report_date or 'N/A'}")
    lines.append(f"   Patient ID: {p.patient_id or 'N/A'} | Ref: {p.referred_by or 'N/A'}")

    # Stats
    lines.append(f"\n📊 EXTRACTION STATS:")
    lines.append(f"   Total Tests Extracted: {result.total_tests}")
    lines.append(f"   Abnormal Values: {result.abnormal_count}")
    lines.append(f"   Critical Values: {result.critical_count}")
    lines.append(f"   Extraction Method: {result.extraction_method}")
    lines.append(f"   Sections Found: {', '.join(result.sections_found) if result.sections_found else 'N/A'}")

    if result.warnings:
        lines.append(f"\n⚠️  WARNINGS:")
        for w in result.warnings:
            lines.append(f"   - {w}")

    # Abnormal biomarkers
    abnormals = [b for b in result.biomarkers if b.is_abnormal]
    if abnormals:
        lines.append(f"\n🔴 ABNORMAL VALUES ({len(abnormals)}):")
        lines.append(f"   {'Test':<35} {'Value':<12} {'Flag':<12} {'Deviation':<10} {'Ref Range'}")
        lines.append(f"   {'─' * 35} {'─' * 12} {'─' * 12} {'─' * 10} {'─' * 20}")
        for b in abnormals:
            flag_symbol = "🔺" if "HIGH" in b.flag else "🔻"
            if b.is_critical:
                flag_symbol = "🚨"
            name = b.test_name[:35]
            val = f"{b.value_raw} {b.unit}"[:12]
            dev = f"{b.deviation_pct}%"
            ref = b.reference_range_standard or b.reference_range_reported
            band = f" [{b.interpretation_band}]" if b.interpretation_band else ""
            lines.append(f"   {flag_symbol} {name:<33} {val:<12} {b.flag:<12} {dev:<10} {ref}{band}")

    # Normal biomarkers
    normals = [b for b in result.biomarkers if not b.is_abnormal]
    if normals:
        lines.append(f"\n🟢 NORMAL VALUES ({len(normals)}):")
        for b in normals:
            lines.append(f"   ✓ {b.test_name:<35} {b.value_raw} {b.unit}")

    lines.append(f"\n{'=' * 70}")
    lines.append(f"Source: {result.source_file} | Extracted: {result.extraction_timestamp}")
    lines.append(f"{'=' * 70}")

    return "\n".join(lines)


# ============================================================
# CLI ENTRY POINT
# ============================================================

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m src.pdf_extractor <path_to_report.pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    print(f"Extracting: {pdf_path}")
    print()

    result = extract_report(pdf_path)

    # Print summary
    print(result_to_summary(result))

    # Save JSON output
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "processed")
    os.makedirs(output_dir, exist_ok=True)
    json_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(pdf_path))[0]}_extracted.json")
    with open(json_path, 'w') as f:
        f.write(result_to_json(result))
    print(f"\n💾 JSON saved: {json_path}")


if __name__ == "__main__":
    main()

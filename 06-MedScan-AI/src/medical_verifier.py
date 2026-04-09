"""
Multi-Agent Medical Verification System
==========================================
Implements a two-agent architecture:
  1. EXTRACTOR — pulls facts from reports (conditions, locations, values)
  2. CRITIC (AUDITOR) — validates the Extractor's output for logical consistency

The Critic never sees raw text. It only validates structured facts.
This prevents the LLM from "explaining away" contradictions.

Also implements:
  - Chain-of-Thought (CoT) reasoning with anatomical validation at each step
  - Red-team adversarial detection for nonsensical findings
"""

import re
from dataclasses import dataclass, field
from typing import Optional

from .anatomical_grounding import (
    validate_condition_in_region,
    validate_radiology_findings,
    CONDITION_REQUIRED_SYSTEM,
    SCAN_REGION_SYSTEMS,
    BIOMARKER_SYSTEM,
)


# ── Data Models ──

@dataclass
class ExtractedFact:
    """A single fact extracted by the Extractor agent."""
    fact_type: str          # "condition" / "location" / "biomarker" / "measurement"
    value: str              # The extracted value
    context: str = ""       # Surrounding context
    confidence: float = 1.0 # 0-1 confidence score
    source_region: str = "" # Which body region this came from


@dataclass
class AuditResult:
    """Result from the Critic/Auditor agent."""
    fact: ExtractedFact
    is_valid: bool
    error_type: Optional[str] = None   # anatomical_mismatch / unit_error / value_impossible / logical_contradiction
    error_message: str = ""
    severity: str = "info"             # info / warning / error / critical
    cot_reasoning: str = ""            # Chain-of-thought reasoning steps


@dataclass
class VerificationReport:
    """Complete verification output from the multi-agent system."""
    total_facts: int = 0
    valid_facts: int = 0
    flagged_facts: int = 0
    critical_errors: int = 0
    audit_results: list[AuditResult] = field(default_factory=list)
    cot_summary: str = ""
    overall_confidence: float = 1.0


# ── Extractor Agent ──

class ExtractorAgent:
    """Extracts structured facts from clinical/radiology data."""

    def extract_from_radiology(self, findings: list, scan_region: str, modality: str) -> list[ExtractedFact]:
        """Extract facts from parsed radiology findings."""
        facts = []

        # Fact: scan type
        facts.append(ExtractedFact(
            fact_type="scan_info",
            value=f"{modality} {scan_region}",
            context=f"Imaging modality: {modality}, Region: {scan_region}",
            source_region=scan_region,
        ))

        for f in findings:
            # Condition fact
            facts.append(ExtractedFact(
                fact_type="condition",
                value=f.finding if hasattr(f, 'finding') else str(f.get("finding", "")),
                context=f"Found in {f.body_region if hasattr(f, 'body_region') else f.get('body_region', '')}",
                source_region=scan_region,
            ))

            # Location fact
            region = f.body_region if hasattr(f, 'body_region') else f.get("body_region", "")
            facts.append(ExtractedFact(
                fact_type="location",
                value=region,
                context=f"Anatomical region of finding",
                source_region=scan_region,
            ))

        return facts

    def extract_from_biomarkers(self, biomarker_interpretations: list) -> list[ExtractedFact]:
        """Extract facts from biomarker analysis."""
        facts = []
        for bi in biomarker_interpretations:
            facts.append(ExtractedFact(
                fact_type="biomarker",
                value=f"{bi.test_name}: {bi.value} {bi.unit}",
                context=f"Flag: {bi.flag}, Deviation: {bi.deviation_pct}%",
                confidence=1.0,
            ))

            # Extract causes as facts
            for cause in getattr(bi, 'possible_causes', []):
                facts.append(ExtractedFact(
                    fact_type="suggested_cause",
                    value=cause,
                    context=f"Suggested for {bi.test_name} ({bi.flag})",
                    confidence=0.8,
                ))

        return facts


# ── Critic / Auditor Agent ──

class CriticAgent:
    """
    Validates extracted facts for logical consistency.
    NEVER sees raw text — only structured facts from the Extractor.
    """

    # Impossible value ranges (red-team detection)
    IMPOSSIBLE_VALUES = {
        "height_meters": (0.3, 2.5),     # Humans aren't 4 meters tall
        "weight_kg": (0.5, 500),
        "temperature_c": (25, 45),
        "heart_rate": (20, 300),
        "blood_pressure_sys": (40, 300),
        "blood_pressure_dia": (20, 200),
        "age_years": (0, 130),
    }

    # Biomarker sanity bounds (beyond critical — these are "impossible in living human")
    BIOMARKER_SANITY = {
        "haemoglobin": (1, 25),          # g/dL
        "total_wbc_count": (100, 500000), # cells/µL
        "platelet_count": (1000, 2000000),
        "sodium": (100, 180),             # mEq/L
        "potassium": (1.0, 10.0),
        "calcium": (3.0, 18.0),
        "fasting_blood_sugar": (10, 1000), # mg/dL
        "hba1c": (2, 20),                # %
        "serum_creatinine": (0.1, 30),
        "total_bilirubin": (0, 50),
        "tsh": (0.001, 500),
        "psa": (0, 10000),
    }

    def audit_facts(self, facts: list[ExtractedFact], scan_region: str = "") -> VerificationReport:
        """
        Audit all extracted facts for consistency.
        Returns a VerificationReport with per-fact results.
        """
        results = []
        cot_steps = []

        for fact in facts:
            if fact.fact_type == "condition" and scan_region:
                result = self._audit_anatomical_consistency(fact, scan_region)
                cot_steps.append(result.cot_reasoning)
            elif fact.fact_type == "biomarker":
                result = self._audit_biomarker_sanity(fact)
                cot_steps.append(result.cot_reasoning)
            elif fact.fact_type == "suggested_cause":
                result = self._audit_cause_plausibility(fact, scan_region)
                cot_steps.append(result.cot_reasoning)
            else:
                result = AuditResult(
                    fact=fact, is_valid=True,
                    cot_reasoning=f"Step: '{fact.value}' — informational fact, no validation needed."
                )

            results.append(result)

        # Compile report
        valid = sum(1 for r in results if r.is_valid)
        flagged = sum(1 for r in results if not r.is_valid)
        critical = sum(1 for r in results if r.severity == "critical")

        overall_confidence = valid / len(results) if results else 1.0

        return VerificationReport(
            total_facts=len(results),
            valid_facts=valid,
            flagged_facts=flagged,
            critical_errors=critical,
            audit_results=results,
            cot_summary="\n".join(cot_steps),
            overall_confidence=round(overall_confidence, 3),
        )

    def _audit_anatomical_consistency(self, fact: ExtractedFact, scan_region: str) -> AuditResult:
        """
        Chain-of-Thought anatomical validation.

        Step 1: Identify the scan type
        Step 2: List organs/structures in that region
        Step 3: Check if the pathology is biologically possible there
        Step 4: Flag if impossible
        """
        condition = fact.value.lower()

        # CoT Step 1
        cot = f"Step 1: Scan region is '{scan_region}'.\n"

        # CoT Step 2
        allowed_systems = set()
        for region_key, systems in SCAN_REGION_SYSTEMS.items():
            if region_key in scan_region.lower():
                allowed_systems = systems
                break
        if not allowed_systems:
            allowed_systems = SCAN_REGION_SYSTEMS.get("unknown", set())
        cot += f"Step 2: Allowed organ systems for '{scan_region}': {allowed_systems}.\n"

        # CoT Step 3
        required_systems = None
        matched_condition = ""
        for cond_key, systems in CONDITION_REQUIRED_SYSTEM.items():
            if cond_key in condition or condition in cond_key:
                required_systems = systems
                matched_condition = cond_key
                break

        if required_systems is None:
            cot += f"Step 3: Condition '{fact.value}' not in validation DB — manual review.\n"
            cot += "Step 4: PASS (unrecognized condition — no automatic rejection)."
            return AuditResult(
                fact=fact, is_valid=True, severity="info",
                cot_reasoning=cot,
                error_message="Condition not in validation database"
            )

        cot += f"Step 3: '{matched_condition}' requires systems: {required_systems}.\n"

        # CoT Step 4
        overlap = required_systems & allowed_systems
        if overlap:
            cot += f"Step 4: PASS — {required_systems} overlaps with {allowed_systems}. Anatomically valid."
            return AuditResult(
                fact=fact, is_valid=True, severity="info",
                cot_reasoning=cot,
            )
        else:
            cot += (
                f"Step 4: FAIL — '{matched_condition}' requires {required_systems} but "
                f"'{scan_region}' only covers {allowed_systems}. "
                f"THIS IS AN ANATOMICAL IMPOSSIBILITY."
            )
            return AuditResult(
                fact=fact, is_valid=False,
                error_type="anatomical_mismatch",
                error_message=(
                    f"DOCUMENT INCONSISTENCY: '{matched_condition}' cannot occur in '{scan_region}'. "
                    f"Required: {required_systems}, Available: {allowed_systems}."
                ),
                severity="critical",
                cot_reasoning=cot,
            )

    def _audit_biomarker_sanity(self, fact: ExtractedFact) -> AuditResult:
        """Check if biomarker values are within physiologically possible ranges."""
        cot = f"Checking: {fact.value}\n"

        # Extract numeric value and biomarker name
        match = re.match(r'(.+?):\s*([\d.]+)', fact.value)
        if not match:
            cot += "Cannot parse numeric value — skipping sanity check."
            return AuditResult(fact=fact, is_valid=True, cot_reasoning=cot)

        name_part = match.group(1).lower().strip()
        try:
            value = float(match.group(2))
        except ValueError:
            return AuditResult(fact=fact, is_valid=True, cot_reasoning=cot + "Non-numeric value.")

        # Check against sanity bounds
        for biomarker_key, (low, high) in self.BIOMARKER_SANITY.items():
            if biomarker_key.replace("_", " ") in name_part or biomarker_key in name_part:
                cot += f"Sanity range for {biomarker_key}: {low}-{high}. Value: {value}.\n"
                if value < low or value > high:
                    cot += f"FAIL — value {value} is outside physiologically possible range."
                    return AuditResult(
                        fact=fact, is_valid=False,
                        error_type="value_impossible",
                        error_message=f"Value {value} for {name_part} is physiologically impossible (range: {low}-{high})",
                        severity="critical",
                        cot_reasoning=cot,
                    )
                else:
                    cot += "PASS — within physiological range."
                    return AuditResult(fact=fact, is_valid=True, cot_reasoning=cot)

        cot += "No sanity bounds defined for this biomarker — PASS."
        return AuditResult(fact=fact, is_valid=True, cot_reasoning=cot)

    def _audit_cause_plausibility(self, fact: ExtractedFact, scan_region: str) -> AuditResult:
        """Check if a suggested cause makes sense for the context."""
        cause_lower = fact.value.lower()
        cot = f"Checking cause plausibility: '{fact.value}'\n"

        # Check if cause mentions an organ system that doesn't match
        if scan_region:
            # If we're looking at a brain scan and the cause mentions "renal failure", flag it
            region_lower = scan_region.lower()
            mismatches = {
                "brain": ["renal", "kidney", "hepatic", "liver", "pancreatic", "ovarian", "prostate"],
                "abdomen": [],  # abdomen is broad, most causes are plausible
                "chest": ["renal", "kidney", "prostate", "ovarian", "uterine"],
            }

            blocked_terms = mismatches.get(region_lower, [])
            for term in blocked_terms:
                if term in cause_lower:
                    cot += f"FAIL — cause mentions '{term}' which is irrelevant to '{scan_region}' scan."
                    return AuditResult(
                        fact=fact, is_valid=False,
                        error_type="logical_contradiction",
                        error_message=f"Cause '{fact.value}' mentions '{term}' — irrelevant to {scan_region} region",
                        severity="warning",
                        cot_reasoning=cot,
                    )

        cot += "PASS — no obvious logical contradiction."
        return AuditResult(fact=fact, is_valid=True, cot_reasoning=cot)


# ── Orchestrator ──

class MedicalVerificationSystem:
    """
    Orchestrates Extractor + Critic for complete verification.
    """

    def __init__(self):
        self.extractor = ExtractorAgent()
        self.critic = CriticAgent()

    def verify_radiology(self, findings: list, scan_region: str, modality: str) -> VerificationReport:
        """Full verification pipeline for radiology findings."""
        facts = self.extractor.extract_from_radiology(findings, scan_region, modality)
        return self.critic.audit_facts(facts, scan_region)

    def verify_biomarkers(self, biomarker_interpretations: list) -> VerificationReport:
        """Full verification pipeline for biomarker interpretations."""
        facts = self.extractor.extract_from_biomarkers(biomarker_interpretations)
        return self.critic.audit_facts(facts)

    def verify_combined(self, biomarker_interpretations: list,
                         radiology_findings: list = None,
                         scan_region: str = "", modality: str = "") -> VerificationReport:
        """Verify both biomarkers and radiology together."""
        all_facts = self.extractor.extract_from_biomarkers(biomarker_interpretations)

        if radiology_findings:
            rad_facts = self.extractor.extract_from_radiology(radiology_findings, scan_region, modality)
            all_facts.extend(rad_facts)

        return self.critic.audit_facts(all_facts, scan_region)

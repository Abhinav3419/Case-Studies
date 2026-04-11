"""
Additional sample reports for edge case validation.
Report 3: Infectious disease panel (dengue + typhoid + malaria)
Report 4: Tumour marker panel
Report 5: Coagulation + critically abnormal values
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "sample_reports")
os.makedirs(OUTPUT_DIR, exist_ok=True)

HDR_COLOR = colors.HexColor('#1a5276')

def _make_table(header, data, col_widths):
    rows = [header] + data
    t = Table(rows, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HDR_COLOR),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ]))
    return t


def create_infectious_report():
    filepath = os.path.join(OUTPUT_DIR, "sample_report_03_infectious.pdf")
    doc = SimpleDocTemplate(filepath, pagesize=A4, topMargin=1.5*cm, bottomMargin=1.5*cm,
                            leftMargin=1.5*cm, rightMargin=1.5*cm)
    styles = getSampleStyleSheet()
    sec = ParagraphStyle('Sec', parent=styles['Heading2'], fontSize=11, textColor=HDR_COLOR, spaceBefore=4*mm, spaceAfter=2*mm)
    elements = []

    elements.append(Paragraph("APOLLO DIAGNOSTICS — FEVER PANEL", styles['Title']))
    elements.append(Paragraph("NABL Accredited | Ref: Dr. Anita Gupta", ParagraphStyle('s', fontSize=8, alignment=TA_CENTER, textColor=colors.grey)))
    elements.append(Spacer(1, 3*mm))

    info = [
        ["Patient Name:", "RAVI KUMAR", "Age/Sex:", "45 Yrs / Male"],
        ["Patient ID:", "AP-2026-55123", "Sample Date:", "08-Apr-2026"],
        ["Report Date:", "09-Apr-2026", "Sample Type:", "Whole Blood / Serum"],
    ]
    it = Table(info, colWidths=[3*cm, 5.5*cm, 3*cm, 5.5*cm])
    it.setStyle(TableStyle([('FONTSIZE', (0,0), (-1,-1), 8), ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
                             ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold')]))
    elements.append(it)
    elements.append(Spacer(1, 3*mm))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))

    # CBC
    elements.append(Paragraph("COMPLETE BLOOD COUNT", sec))
    elements.append(_make_table(
        ["Test Name", "Result", "Unit", "Reference Range", "Flag"],
        [
            ["Haemoglobin", "10.2", "g/dL", "13.0 - 17.0", "LOW"],
            ["Total WBC Count", "3200", "cells/µL", "4000 - 10000", "LOW"],
            ["Platelet Count", "62000", "/µL", "150000 - 410000", "LOW"],
            ["Neutrophils", "35", "%", "40 - 70", "LOW"],
            ["Lymphocytes", "55", "%", "20 - 40", "HIGH"],
            ["Haematocrit (PCV)", "31.5", "%", "40 - 50", "LOW"],
            ["ESR", "45", "mm/hr", "0 - 15", "HIGH"],
        ],
        [6.5*cm, 2.5*cm, 2.5*cm, 3.5*cm, 2*cm]
    ))

    # Inflammatory
    elements.append(Paragraph("INFLAMMATORY MARKERS", sec))
    elements.append(_make_table(
        ["Test Name", "Result", "Unit", "Reference Range", "Flag"],
        [
            ["C-Reactive Protein (CRP)", "85.4", "mg/L", "0 - 5", "HIGH"],
            ["Procalcitonin (PCT)", "0.38", "ng/mL", "0 - 0.05", "HIGH"],
        ],
        [6.5*cm, 2.5*cm, 2.5*cm, 3.5*cm, 2*cm]
    ))

    # Dengue
    elements.append(Paragraph("DENGUE PANEL", sec))
    elements.append(_make_table(
        ["Test Name", "Result", "Unit", "Reference Range", "Flag"],
        [
            ["Dengue NS1 Antigen", "Positive", "", "Negative", "POSITIVE"],
            ["Dengue IgM Antibody", "Negative", "", "Negative", ""],
            ["Dengue IgG Antibody", "Negative", "", "Negative", ""],
        ],
        [6.5*cm, 2.5*cm, 2.5*cm, 3.5*cm, 2*cm]
    ))

    # Typhoid
    elements.append(Paragraph("WIDAL TEST", sec))
    elements.append(_make_table(
        ["Test Name", "Result", "Unit", "Reference Range", "Flag"],
        [
            ["Widal O (S. typhi)", "1:160", "titre", "< 1:80", "HIGH"],
            ["Widal H (S. typhi)", "1:80", "titre", "< 1:80", ""],
        ],
        [6.5*cm, 2.5*cm, 2.5*cm, 3.5*cm, 2*cm]
    ))

    # Malaria
    elements.append(Paragraph("MALARIA SCREENING", sec))
    elements.append(_make_table(
        ["Test Name", "Result", "Unit", "Reference Range", "Flag"],
        [
            ["Malaria Antigen (Rapid)", "Negative", "", "Negative", ""],
            ["Peripheral Smear for MP", "No parasites seen", "", "Negative", ""],
        ],
        [6.5*cm, 2.5*cm, 2.5*cm, 3.5*cm, 2*cm]
    ))

    # LFT (to cross-correlate with dengue)
    elements.append(Paragraph("LIVER FUNCTION TEST", sec))
    elements.append(_make_table(
        ["Test Name", "Result", "Unit", "Reference Range", "Flag"],
        [
            ["SGOT (AST)", "156", "U/L", "0 - 40", "HIGH"],
            ["SGPT (ALT)", "198", "U/L", "0 - 41", "HIGH"],
            ["Total Bilirubin", "2.1", "mg/dL", "0.1 - 1.2", "HIGH"],
        ],
        [6.5*cm, 2.5*cm, 2.5*cm, 3.5*cm, 2*cm]
    ))

    elements.append(Spacer(1, 5*mm))
    elements.append(Paragraph("*** Kindly correlate clinically. ***",
                               ParagraphStyle('d', fontSize=7, textColor=colors.grey, alignment=TA_CENTER)))

    doc.build(elements)
    print(f"[OK] {filepath}")
    return filepath


def create_tumour_marker_report():
    filepath = os.path.join(OUTPUT_DIR, "sample_report_04_tumour_markers.pdf")
    doc = SimpleDocTemplate(filepath, pagesize=A4, topMargin=1.5*cm, bottomMargin=1.5*cm,
                            leftMargin=1.5*cm, rightMargin=1.5*cm)
    styles = getSampleStyleSheet()
    sec = ParagraphStyle('Sec', parent=styles['Heading2'], fontSize=11, textColor=HDR_COLOR, spaceBefore=4*mm, spaceAfter=2*mm)
    elements = []

    elements.append(Paragraph("ONCQUEST LABS — TUMOUR MARKER PANEL", styles['Title']))
    elements.append(Spacer(1, 3*mm))

    info = [
        ["Patient Name:", "SURESH PATEL", "Age/Sex:", "62 Yrs / Male"],
        ["Patient ID:", "OQ-2026-99201", "Ref. By:", "Dr. Vikram Shah (Oncology)"],
        ["Report Date:", "07-Apr-2026", "Sample Type:", "Serum"],
    ]
    it = Table(info, colWidths=[3*cm, 5.5*cm, 3*cm, 5.5*cm])
    it.setStyle(TableStyle([('FONTSIZE', (0,0), (-1,-1), 8), ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
                             ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold')]))
    elements.append(it)
    elements.append(Spacer(1, 3*mm))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))

    elements.append(Paragraph("TUMOUR MARKERS", sec))
    elements.append(_make_table(
        ["Test Name", "Result", "Unit", "Reference Range", "Flag"],
        [
            ["PSA (Total)", "18.5", "ng/mL", "0 - 4.0", "HIGH"],
            ["CEA (Carcinoembryonic Antigen)", "12.8", "ng/mL", "0 - 5.0", "HIGH"],
            ["AFP (Alpha Fetoprotein)", "8.2", "ng/mL", "0 - 10", ""],
            ["CA 19-9", "42", "U/mL", "0 - 37", "HIGH"],
            ["LDH (Lactate Dehydrogenase)", "385", "U/L", "140 - 280", "HIGH"],
        ],
        [6.5*cm, 2.5*cm, 2.5*cm, 3.5*cm, 2*cm]
    ))

    elements.append(Paragraph("RENAL FUNCTION", sec))
    elements.append(_make_table(
        ["Test Name", "Result", "Unit", "Reference Range", "Flag"],
        [
            ["Serum Creatinine", "1.8", "mg/dL", "0.7 - 1.3", "HIGH"],
            ["eGFR (CKD-EPI)", "42", "mL/min/1.73m²", "> 90", "LOW"],
            ["Calcium", "11.8", "mg/dL", "8.5 - 10.5", "HIGH"],
        ],
        [6.5*cm, 2.5*cm, 2.5*cm, 3.5*cm, 2*cm]
    ))

    elements.append(Paragraph("COMPLETE BLOOD COUNT", sec))
    elements.append(_make_table(
        ["Test Name", "Result", "Unit", "Reference Range", "Flag"],
        [
            ["Haemoglobin", "9.8", "g/dL", "13.0 - 17.0", "LOW"],
            ["Total WBC Count", "14500", "cells/µL", "4000 - 10000", "HIGH"],
            ["Platelet Count", "310000", "/µL", "150000 - 410000", ""],
            ["ESR", "68", "mm/hr", "0 - 15", "HIGH"],
        ],
        [6.5*cm, 2.5*cm, 2.5*cm, 3.5*cm, 2*cm]
    ))

    elements.append(Spacer(1, 5*mm))
    elements.append(Paragraph("*** For professional use only. Correlate with clinical findings and imaging. ***",
                               ParagraphStyle('d', fontSize=7, textColor=colors.grey, alignment=TA_CENTER)))

    doc.build(elements)
    print(f"[OK] {filepath}")
    return filepath


def create_coagulation_critical_report():
    filepath = os.path.join(OUTPUT_DIR, "sample_report_05_coagulation.pdf")
    doc = SimpleDocTemplate(filepath, pagesize=A4, topMargin=1.5*cm, bottomMargin=1.5*cm,
                            leftMargin=1.5*cm, rightMargin=1.5*cm)
    styles = getSampleStyleSheet()
    sec = ParagraphStyle('Sec', parent=styles['Heading2'], fontSize=11, textColor=HDR_COLOR, spaceBefore=4*mm, spaceAfter=2*mm)
    elements = []

    elements.append(Paragraph("MAX LAB — COAGULATION & CRITICAL PANEL", styles['Title']))
    elements.append(Spacer(1, 3*mm))

    info = [
        ["Patient Name:", "MEERA JOSHI", "Age/Sex:", "38 Yrs / Female"],
        ["Patient ID:", "MAX-2026-41022", "Ref. By:", "Dr. Arun Kapoor (ICU)"],
        ["Report Date:", "09-Apr-2026", "Sample Type:", "Citrated Plasma / Serum"],
    ]
    it = Table(info, colWidths=[3*cm, 5.5*cm, 3*cm, 5.5*cm])
    it.setStyle(TableStyle([('FONTSIZE', (0,0), (-1,-1), 8), ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
                             ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold')]))
    elements.append(it)
    elements.append(Spacer(1, 3*mm))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))

    elements.append(Paragraph("COAGULATION PROFILE", sec))
    elements.append(_make_table(
        ["Test Name", "Result", "Unit", "Reference Range", "Flag"],
        [
            ["Prothrombin Time (PT)", "22.5", "seconds", "11.0 - 13.5", "HIGH"],
            ["INR", "2.1", "", "0.8 - 1.2", "HIGH"],
            ["aPTT", "52", "seconds", "25 - 35", "HIGH"],
            ["Fibrinogen", "95", "mg/dL", "200 - 400", "LOW"],
            ["D-Dimer", "4800", "ng/mL", "0 - 500", "HIGH"],
        ],
        [6.5*cm, 2.5*cm, 2.5*cm, 3.5*cm, 2*cm]
    ))

    elements.append(Paragraph("CBC — CRITICAL VALUES", sec))
    elements.append(_make_table(
        ["Test Name", "Result", "Unit", "Reference Range", "Flag"],
        [
            ["Haemoglobin", "6.8", "g/dL", "12.0 - 15.5", "CRITICAL LOW"],
            ["Platelet Count", "38000", "/µL", "150000 - 410000", "CRITICAL LOW"],
            ["Total WBC Count", "22000", "cells/µL", "4000 - 10000", "HIGH"],
        ],
        [6.5*cm, 2.5*cm, 2.5*cm, 3.5*cm, 2*cm]
    ))

    elements.append(Paragraph("INFLAMMATORY / SEPSIS MARKERS", sec))
    elements.append(_make_table(
        ["Test Name", "Result", "Unit", "Reference Range", "Flag"],
        [
            ["CRP", "245", "mg/L", "0 - 5", "HIGH"],
            ["Procalcitonin", "8.5", "ng/mL", "0 - 0.05", "HIGH"],
            ["LDH", "520", "U/L", "140 - 280", "HIGH"],
        ],
        [6.5*cm, 2.5*cm, 2.5*cm, 3.5*cm, 2*cm]
    ))

    elements.append(Paragraph("RENAL & LIVER", sec))
    elements.append(_make_table(
        ["Test Name", "Result", "Unit", "Reference Range", "Flag"],
        [
            ["Serum Creatinine", "2.8", "mg/dL", "0.6 - 1.1", "HIGH"],
            ["Total Bilirubin", "4.5", "mg/dL", "0.1 - 1.2", "HIGH"],
            ["SGPT (ALT)", "210", "U/L", "0 - 41", "HIGH"],
            ["Potassium", "5.8", "mEq/L", "3.5 - 5.1", "HIGH"],
        ],
        [6.5*cm, 2.5*cm, 2.5*cm, 3.5*cm, 2*cm]
    ))

    elements.append(Spacer(1, 5*mm))
    elements.append(Paragraph("*** CRITICAL VALUES — PHYSICIAN NOTIFIED ***",
                               ParagraphStyle('d', fontSize=9, textColor=colors.red, alignment=TA_CENTER)))

    doc.build(elements)
    print(f"[OK] {filepath}")
    return filepath


if __name__ == "__main__":
    create_infectious_report()
    create_tumour_marker_report()
    create_coagulation_critical_report()
    print("Done — 3 edge-case reports generated.")

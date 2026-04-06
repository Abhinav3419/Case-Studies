"""
Generate realistic sample clinical lab report PDFs for testing MedScan AI.
Creates reports mimicking Indian lab formats (Thyrocare, Dr. Lal PathLabs style).
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "sample_reports")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_cbc_lipid_report():
    """Generate a Complete Blood Count + Lipid Profile report (Indian lab style)."""
    filepath = os.path.join(OUTPUT_DIR, "sample_report_01_cbc_lipid.pdf")
    doc = SimpleDocTemplate(filepath, pagesize=A4,
                            topMargin=1.5*cm, bottomMargin=1.5*cm,
                            leftMargin=1.5*cm, rightMargin=1.5*cm)
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle('LabTitle', parent=styles['Title'],
                                  fontSize=16, textColor=colors.HexColor('#1a5276'),
                                  spaceAfter=2*mm)
    header_style = ParagraphStyle('Header', parent=styles['Normal'],
                                   fontSize=9, textColor=colors.grey)
    section_style = ParagraphStyle('Section', parent=styles['Heading2'],
                                    fontSize=12, textColor=colors.HexColor('#2c3e50'),
                                    spaceBefore=4*mm, spaceAfter=2*mm)
    disclaimer_style = ParagraphStyle('Disclaimer', parent=styles['Normal'],
                                       fontSize=7, textColor=colors.grey,
                                       spaceBefore=5*mm)

    elements = []

    # --- Lab Header ---
    elements.append(Paragraph("PRECISION DIAGNOSTICS & PATHOLOGY LAB", title_style))
    elements.append(Paragraph("NABL Accredited | ISO 15189:2012 Certified", header_style))
    elements.append(Paragraph("Sector 18, Noida, Uttar Pradesh - 201301 | Ph: 0120-4567890", header_style))
    elements.append(Spacer(1, 3*mm))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#1a5276')))
    elements.append(Spacer(1, 3*mm))

    # --- Patient Info ---
    patient_data = [
        ["Patient Name:", "ABHINAV PANDEY", "Age/Sex:", "33 Yrs / Male"],
        ["Patient ID:", "PD-2026-04-78231", "Sample ID:", "BLD-260405-1142"],
        ["Ref. By:", "Dr. Sanjay Mehta", "Collection Date:", "04-Apr-2026, 07:45 AM"],
        ["Report Date:", "05-Apr-2026, 02:30 PM", "Sample Type:", "Whole Blood (EDTA) / Serum"],
    ]
    patient_table = Table(patient_data, colWidths=[3*cm, 5.5*cm, 3*cm, 5.5*cm])
    patient_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (2, 0), (2, -1), colors.HexColor('#2c3e50')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
    ]))
    elements.append(patient_table)
    elements.append(Spacer(1, 3*mm))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))

    # --- SECTION 1: COMPLETE BLOOD COUNT ---
    elements.append(Paragraph("COMPLETE BLOOD COUNT (CBC)", section_style))

    cbc_header = ["Test Name", "Result", "Unit", "Reference Range", "Flag"]
    cbc_data = [
        cbc_header,
        ["Haemoglobin (Hb)", "12.8", "g/dL", "13.0 - 17.0", "LOW"],
        ["Total RBC Count", "4.52", "million/µL", "4.5 - 5.5", ""],
        ["Packed Cell Volume (PCV)", "38.2", "%", "40.0 - 50.0", "LOW"],
        ["Mean Corpuscular Volume (MCV)", "84.5", "fL", "80.0 - 100.0", ""],
        ["MCH", "28.3", "pg", "27.0 - 31.0", ""],
        ["MCHC", "33.5", "g/dL", "32.0 - 36.0", ""],
        ["Red Cell Distribution Width (RDW)", "14.8", "%", "11.5 - 14.5", "HIGH"],
        ["Total WBC Count", "11200", "cells/µL", "4000 - 10000", "HIGH"],
        ["Neutrophils", "72", "%", "40 - 70", "HIGH"],
        ["Lymphocytes", "20", "%", "20 - 40", ""],
        ["Monocytes", "5", "%", "2 - 8", ""],
        ["Eosinophils", "2", "%", "1 - 6", ""],
        ["Basophils", "1", "%", "0 - 2", ""],
        ["Platelet Count", "245000", "/µL", "150000 - 410000", ""],
        ["Mean Platelet Volume (MPV)", "10.2", "fL", "7.5 - 11.5", ""],
        ["ESR (Westergren)", "22", "mm/hr", "0 - 15", "HIGH"],
    ]

    cbc_table = Table(cbc_data, colWidths=[6.5*cm, 2.5*cm, 2.5*cm, 3.5*cm, 2*cm])
    cbc_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5276')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        # Flag column coloring
        ('TEXTCOLOR', (4, 1), (4, 1), colors.red),   # Hb LOW
        ('TEXTCOLOR', (4, 3), (4, 3), colors.red),    # PCV LOW
        ('TEXTCOLOR', (4, 7), (4, 7), colors.red),    # RDW HIGH
        ('TEXTCOLOR', (4, 8), (4, 8), colors.red),    # WBC HIGH
        ('TEXTCOLOR', (4, 9), (4, 9), colors.red),    # Neutrophils HIGH
        ('TEXTCOLOR', (4, 16), (4, 16), colors.red),  # ESR HIGH
        ('FONTNAME', (4, 1), (4, -1), 'Helvetica-Bold'),
    ]))
    elements.append(cbc_table)

    # --- SECTION 2: LIPID PROFILE ---
    elements.append(Paragraph("LIPID PROFILE (FASTING)", section_style))

    lipid_header = ["Test Name", "Result", "Unit", "Desirable Range", "Flag"]
    lipid_data = [
        lipid_header,
        ["Total Cholesterol", "238", "mg/dL", "< 200 (Desirable)", "HIGH"],
        ["Triglycerides", "195", "mg/dL", "< 150 (Normal)", "HIGH"],
        ["HDL Cholesterol", "38", "mg/dL", "> 40 (Desirable)", "LOW"],
        ["LDL Cholesterol (Calculated)", "161", "mg/dL", "< 100 (Optimal)", "HIGH"],
        ["VLDL Cholesterol", "39", "mg/dL", "< 30", "HIGH"],
        ["Total Cholesterol / HDL Ratio", "6.26", "", "< 4.5 (Ideal)", "HIGH"],
        ["LDL / HDL Ratio", "4.24", "", "< 3.0 (Ideal)", "HIGH"],
        ["Non-HDL Cholesterol", "200", "mg/dL", "< 130", "HIGH"],
    ]

    lipid_table = Table(lipid_data, colWidths=[6.5*cm, 2.5*cm, 2*cm, 4*cm, 2*cm])
    lipid_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5276')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('TEXTCOLOR', (4, 1), (4, -1), colors.red),
        ('FONTNAME', (4, 1), (4, -1), 'Helvetica-Bold'),
    ]))
    elements.append(lipid_table)

    # --- SECTION 3: LIVER FUNCTION TEST ---
    elements.append(Paragraph("LIVER FUNCTION TEST (LFT)", section_style))

    lft_header = ["Test Name", "Result", "Unit", "Reference Range", "Flag"]
    lft_data = [
        lft_header,
        ["Total Bilirubin", "1.4", "mg/dL", "0.1 - 1.2", "HIGH"],
        ["Direct Bilirubin", "0.4", "mg/dL", "0.0 - 0.3", "HIGH"],
        ["Indirect Bilirubin", "1.0", "mg/dL", "0.1 - 1.0", ""],
        ["SGOT (AST)", "52", "U/L", "0 - 40", "HIGH"],
        ["SGPT (ALT)", "68", "U/L", "0 - 41", "HIGH"],
        ["Alkaline Phosphatase (ALP)", "95", "U/L", "44 - 147", ""],
        ["Total Protein", "7.2", "g/dL", "6.0 - 8.3", ""],
        ["Albumin", "4.1", "g/dL", "3.5 - 5.5", ""],
        ["Globulin", "3.1", "g/dL", "2.0 - 3.5", ""],
        ["A/G Ratio", "1.32", "", "1.0 - 2.0", ""],
        ["GGT (Gamma GT)", "78", "U/L", "0 - 55", "HIGH"],
    ]

    lft_table = Table(lft_data, colWidths=[6.5*cm, 2.5*cm, 2*cm, 3.5*cm, 2.5*cm])
    lft_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5276')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('TEXTCOLOR', (4, 1), (4, -1), colors.red),
        ('FONTNAME', (4, 1), (4, -1), 'Helvetica-Bold'),
    ]))
    elements.append(lft_table)

    # --- SECTION 4: THYROID PROFILE ---
    elements.append(Paragraph("THYROID FUNCTION TEST", section_style))

    thyroid_header = ["Test Name", "Result", "Unit", "Reference Range", "Flag"]
    thyroid_data = [
        thyroid_header,
        ["TSH (Ultrasensitive)", "6.82", "µIU/mL", "0.35 - 4.94", "HIGH"],
        ["Free T3", "2.45", "pg/mL", "1.71 - 3.71", ""],
        ["Free T4", "0.78", "ng/dL", "0.70 - 1.48", ""],
        ["Total T3", "95", "ng/dL", "60 - 200", ""],
        ["Total T4", "5.8", "µg/dL", "4.5 - 12.0", ""],
    ]

    thyroid_table = Table(thyroid_data, colWidths=[6.5*cm, 2.5*cm, 2.5*cm, 3.5*cm, 2*cm])
    thyroid_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5276')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('TEXTCOLOR', (4, 1), (4, 1), colors.red),
        ('FONTNAME', (4, 1), (4, -1), 'Helvetica-Bold'),
    ]))
    elements.append(thyroid_table)

    # --- SECTION 5: KIDNEY / RENAL FUNCTION ---
    elements.append(Paragraph("KIDNEY FUNCTION TEST (KFT / RFT)", section_style))

    kft_header = ["Test Name", "Result", "Unit", "Reference Range", "Flag"]
    kft_data = [
        kft_header,
        ["Blood Urea", "32", "mg/dL", "17 - 43", ""],
        ["Blood Urea Nitrogen (BUN)", "14.9", "mg/dL", "7 - 20", ""],
        ["Serum Creatinine", "1.0", "mg/dL", "0.7 - 1.3", ""],
        ["Uric Acid", "7.8", "mg/dL", "3.5 - 7.2", "HIGH"],
        ["BUN / Creatinine Ratio", "14.9", "", "10 - 20", ""],
        ["Sodium (Na+)", "141", "mEq/L", "136 - 145", ""],
        ["Potassium (K+)", "4.3", "mEq/L", "3.5 - 5.1", ""],
        ["Chloride (Cl-)", "102", "mEq/L", "98 - 106", ""],
        ["Calcium", "9.2", "mg/dL", "8.5 - 10.5", ""],
        ["Phosphorus", "3.8", "mg/dL", "2.5 - 4.5", ""],
        ["eGFR (CKD-EPI)", "92", "mL/min/1.73m²", "> 90 (Normal)", ""],
    ]

    kft_table = Table(kft_data, colWidths=[6.5*cm, 2.5*cm, 2.5*cm, 3.5*cm, 2*cm])
    kft_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5276')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('TEXTCOLOR', (4, 4), (4, 4), colors.red),
        ('FONTNAME', (4, 1), (4, -1), 'Helvetica-Bold'),
    ]))
    elements.append(kft_table)

    # --- SECTION 6: BLOOD SUGAR ---
    elements.append(Paragraph("BLOOD GLUCOSE", section_style))

    sugar_header = ["Test Name", "Result", "Unit", "Reference Range", "Flag"]
    sugar_data = [
        sugar_header,
        ["Fasting Blood Sugar (FBS)", "118", "mg/dL", "70 - 100 (Normal)", "HIGH"],
        ["HbA1c (Glycated Haemoglobin)", "6.1", "%", "< 5.7 (Normal)", "HIGH"],
        ["Average Blood Glucose (est.)", "128", "mg/dL", "< 117 (Normal)", "HIGH"],
    ]

    sugar_table = Table(sugar_data, colWidths=[6.5*cm, 2.5*cm, 2.5*cm, 3.5*cm, 2*cm])
    sugar_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5276')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('TEXTCOLOR', (4, 1), (4, -1), colors.red),
        ('FONTNAME', (4, 1), (4, -1), 'Helvetica-Bold'),
    ]))
    elements.append(sugar_table)

    # --- Vitamin Panel ---
    elements.append(Paragraph("VITAMIN & MINERAL PANEL", section_style))

    vit_header = ["Test Name", "Result", "Unit", "Reference Range", "Flag"]
    vit_data = [
        vit_header,
        ["Vitamin D (25-OH)", "14.2", "ng/mL", "30 - 100 (Sufficient)", "LOW"],
        ["Vitamin B12", "185", "pg/mL", "211 - 946", "LOW"],
        ["Iron (Serum)", "55", "µg/dL", "65 - 175", "LOW"],
        ["Ferritin", "18", "ng/mL", "20 - 250", "LOW"],
        ["TIBC", "410", "µg/dL", "250 - 370", "HIGH"],
        ["Transferrin Saturation", "13.4", "%", "20 - 50", "LOW"],
        ["Folate (Folic Acid)", "4.8", "ng/mL", "3.0 - 17.0", ""],
    ]

    vit_table = Table(vit_data, colWidths=[6.5*cm, 2.5*cm, 2.5*cm, 3.5*cm, 2*cm])
    vit_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5276')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('TEXTCOLOR', (4, 1), (4, -1), colors.red),
        ('FONTNAME', (4, 1), (4, -1), 'Helvetica-Bold'),
    ]))
    elements.append(vit_table)

    # --- Footer ---
    elements.append(Spacer(1, 8*mm))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))
    elements.append(Paragraph(
        "<b>Pathologist:</b> Dr. Meera Sharma, MD (Pathology) | Reg. No: UP-MCI-34521",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, spaceBefore=2*mm)
    ))
    elements.append(Paragraph(
        "<b>Lab Director:</b> Dr. Rajesh Kumar, MBBS, DCP | Lab Reg: UP/NOI/2019/00234",
        ParagraphStyle('Footer2', parent=styles['Normal'], fontSize=8)
    ))
    elements.append(Paragraph(
        "*** This is a computer-generated report. Kindly correlate clinically. ***",
        disclaimer_style
    ))
    elements.append(Paragraph(
        "Disclaimer: The results reported are specific to the sample received. "
        "Results may vary with time, medication, and physiological conditions. "
        "Please consult your physician for interpretation.",
        disclaimer_style
    ))

    doc.build(elements)
    print(f"[OK] Generated: {filepath}")
    return filepath


def create_minimal_thyroid_report():
    """Generate a minimal thyroid-only report (different lab format)."""
    filepath = os.path.join(OUTPUT_DIR, "sample_report_02_thyroid.pdf")
    doc = SimpleDocTemplate(filepath, pagesize=A4,
                            topMargin=2*cm, bottomMargin=2*cm,
                            leftMargin=2*cm, rightMargin=2*cm)
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph("SRL DIAGNOSTICS", styles['Title']))
    elements.append(Paragraph("An SRL Group Laboratory | CIN: L74899DL2004PLC123456", 
                               ParagraphStyle('Sub', fontSize=8, alignment=TA_CENTER, textColor=colors.grey)))
    elements.append(Spacer(1, 5*mm))

    # Patient info as simple text
    info_text = """
    <b>Name:</b> Priya Sharma &nbsp;&nbsp; <b>Age:</b> 28 Years &nbsp;&nbsp; <b>Sex:</b> Female<br/>
    <b>Ref. Doctor:</b> Self &nbsp;&nbsp; <b>Sample Date:</b> 03-Apr-2026 &nbsp;&nbsp; <b>Report Date:</b> 04-Apr-2026<br/>
    <b>Patient ID:</b> SRL-2026-88342 &nbsp;&nbsp; <b>Barcode:</b> 826041592
    """
    elements.append(Paragraph(info_text, ParagraphStyle('Info', fontSize=9, leading=14)))
    elements.append(Spacer(1, 5*mm))

    elements.append(Paragraph("THYROID PROFILE", styles['Heading2']))

    data = [
        ["Investigation", "Result", "Unit", "Biological Ref. Interval"],
        ["T3, Total", "1.12", "ng/mL", "0.58 - 1.59"],
        ["T4, Total", "6.8", "µg/dL", "4.87 - 11.72"],
        ["TSH, Ultrasensitive", "8.45", "µIU/mL", "0.35 - 4.94"],
        ["Free T3 (FT3)", "2.1", "pg/mL", "1.71 - 3.71"],
        ["Free T4 (FT4)", "0.65", "ng/dL", "0.70 - 1.48"],
        ["Anti-TPO Antibodies", "312", "IU/mL", "< 34"],
    ]

    t = Table(data, colWidths=[5.5*cm, 2.5*cm, 2.5*cm, 5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 5*mm))

    elements.append(Paragraph("VITAMIN D (25-HYDROXY)", styles['Heading2']))
    vit_data = [
        ["Investigation", "Result", "Unit", "Biological Ref. Interval"],
        ["25-OH Vitamin D (Total)", "11.5", "ng/mL",
         "Deficient: <20 | Insufficient: 20-29 | Sufficient: 30-100"],
    ]
    vt = Table(vit_data, colWidths=[5.5*cm, 2.5*cm, 2.5*cm, 5*cm])
    vt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(vt)

    elements.append(Spacer(1, 10*mm))
    elements.append(Paragraph(
        "*** End of Report. Please consult your physician for clinical correlation. ***",
        ParagraphStyle('Disc', fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
    ))

    doc.build(elements)
    print(f"[OK] Generated: {filepath}")
    return filepath


if __name__ == "__main__":
    print("Generating sample clinical lab reports...")
    create_cbc_lipid_report()
    create_minimal_thyroid_report()
    print("\nDone! Reports saved to:", OUTPUT_DIR)

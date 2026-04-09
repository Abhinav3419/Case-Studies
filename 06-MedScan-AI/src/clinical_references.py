"""
Clinical Reference Ranges Database
===================================
Standardized reference ranges for common biomarkers based on:
- Harrison's Principles of Internal Medicine (21st Ed.)
- WHO Clinical Guidelines
- ICMR (Indian Council of Medical Research) standards
- Tietz Clinical Guide to Laboratory Tests (6th Ed.)

This module serves as the ground-truth for biomarker validation
when the PDF itself doesn't provide clear reference ranges.
"""

# Each entry: canonical_name -> {aliases, unit, ref_range, category, critical_low, critical_high}
# ref_range is for adult males by default; gender-specific noted where relevant

REFERENCE_RANGES = {
    # ============================================================
    # COMPLETE BLOOD COUNT (CBC)
    # ============================================================
    "haemoglobin": {
        "aliases": ["hemoglobin", "hb", "hgb"],
        "unit": "g/dL",
        "ref_range": {"male": (13.0, 17.0), "female": (12.0, 15.5)},
        "critical_low": 7.0,
        "critical_high": 20.0,
        "category": "CBC",
        "description": "Oxygen-carrying protein in red blood cells"
    },
    "total_rbc_count": {
        "aliases": ["rbc count", "rbc", "red blood cell count", "total rbc"],
        "unit": "million/µL",
        "ref_range": {"male": (4.5, 5.5), "female": (4.0, 5.0)},
        "critical_low": 2.0,
        "critical_high": 7.0,
        "category": "CBC",
        "description": "Total number of red blood cells"
    },
    "packed_cell_volume": {
        "aliases": ["pcv", "hematocrit", "hct"],
        "unit": "%",
        "ref_range": {"male": (40.0, 50.0), "female": (36.0, 44.0)},
        "critical_low": 20.0,
        "critical_high": 60.0,
        "category": "CBC",
        "description": "Percentage of blood volume occupied by red blood cells"
    },
    "mcv": {
        "aliases": ["mean corpuscular volume"],
        "unit": "fL",
        "ref_range": {"all": (80.0, 100.0)},
        "critical_low": 50.0,
        "critical_high": 130.0,
        "category": "CBC",
        "description": "Average volume of a single red blood cell"
    },
    "mch": {
        "aliases": ["mean corpuscular haemoglobin", "mean corpuscular hemoglobin"],
        "unit": "pg",
        "ref_range": {"all": (27.0, 31.0)},
        "category": "CBC",
        "description": "Average weight of hemoglobin per red blood cell"
    },
    "mchc": {
        "aliases": ["mean corpuscular haemoglobin concentration",
                     "mean corpuscular hemoglobin concentration"],
        "unit": "g/dL",
        "ref_range": {"all": (32.0, 36.0)},
        "category": "CBC",
        "description": "Average concentration of hemoglobin in red blood cells"
    },
    "rdw": {
        "aliases": ["red cell distribution width", "rdw-cv"],
        "unit": "%",
        "ref_range": {"all": (11.5, 14.5)},
        "category": "CBC",
        "description": "Variation in red blood cell size"
    },
    "total_wbc_count": {
        "aliases": ["wbc count", "wbc", "white blood cell count", "total wbc",
                     "total leucocyte count", "tlc"],
        "unit": "cells/µL",
        "ref_range": {"all": (4000, 10000)},
        "critical_low": 2000,
        "critical_high": 30000,
        "category": "CBC",
        "description": "Total number of white blood cells"
    },
    "neutrophils": {
        "aliases": ["neutrophil", "neutrophils %", "segmented neutrophils"],
        "unit": "%",
        "ref_range": {"all": (40, 70)},
        "category": "CBC - Differential",
        "description": "First-line immune defense cells"
    },
    "lymphocytes": {
        "aliases": ["lymphocyte", "lymphocytes %"],
        "unit": "%",
        "ref_range": {"all": (20, 40)},
        "category": "CBC - Differential",
        "description": "Adaptive immune cells (B cells and T cells)"
    },
    "monocytes": {
        "aliases": ["monocyte", "monocytes %"],
        "unit": "%",
        "ref_range": {"all": (2, 8)},
        "category": "CBC - Differential",
        "description": "Phagocytic cells that fight infection"
    },
    "eosinophils": {
        "aliases": ["eosinophil", "eosinophils %"],
        "unit": "%",
        "ref_range": {"all": (1, 6)},
        "category": "CBC - Differential",
        "description": "Cells involved in allergic responses and parasitic defense"
    },
    "basophils": {
        "aliases": ["basophil", "basophils %"],
        "unit": "%",
        "ref_range": {"all": (0, 2)},
        "category": "CBC - Differential",
        "description": "Least common WBC, involved in allergic reactions"
    },
    "platelet_count": {
        "aliases": ["platelets", "plt", "thrombocyte count"],
        "unit": "/µL",
        "ref_range": {"all": (150000, 410000)},
        "critical_low": 50000,
        "critical_high": 1000000,
        "category": "CBC",
        "description": "Blood cells essential for clotting"
    },
    "mpv": {
        "aliases": ["mean platelet volume"],
        "unit": "fL",
        "ref_range": {"all": (7.5, 11.5)},
        "category": "CBC",
        "description": "Average size of platelets"
    },
    "esr": {
        "aliases": ["erythrocyte sedimentation rate", "esr westergren"],
        "unit": "mm/hr",
        "ref_range": {"male": (0, 15), "female": (0, 20)},
        "category": "CBC",
        "description": "Non-specific marker of inflammation"
    },

    # ============================================================
    # LIPID PROFILE
    # ============================================================
    "total_cholesterol": {
        "aliases": ["cholesterol", "serum cholesterol", "tc"],
        "unit": "mg/dL",
        "ref_range": {"all": (0, 200)},
        "category": "Lipid Profile",
        "description": "Total cholesterol in blood",
        "interpretation_bands": {
            "desirable": (0, 200),
            "borderline_high": (200, 239),
            "high": (240, 9999)
        }
    },
    "triglycerides": {
        "aliases": ["tg", "trigs", "serum triglycerides"],
        "unit": "mg/dL",
        "ref_range": {"all": (0, 150)},
        "category": "Lipid Profile",
        "description": "Fat molecules in blood",
        "interpretation_bands": {
            "normal": (0, 150),
            "borderline_high": (150, 199),
            "high": (200, 499),
            "very_high": (500, 9999)
        }
    },
    "hdl_cholesterol": {
        "aliases": ["hdl", "hdl-c", "good cholesterol"],
        "unit": "mg/dL",
        "ref_range": {"male": (40, 999), "female": (50, 999)},
        "category": "Lipid Profile",
        "description": "High-density lipoprotein — protective cholesterol"
    },
    "ldl_cholesterol": {
        "aliases": ["ldl", "ldl-c", "ldl cholesterol calculated", "ldl cholesterol (calculated)",
                     "bad cholesterol", "low density lipoprotein"],
        "unit": "mg/dL",
        "ref_range": {"all": (0, 100)},
        "category": "Lipid Profile",
        "description": "Low-density lipoprotein — atherogenic cholesterol",
        "interpretation_bands": {
            "optimal": (0, 100),
            "near_optimal": (100, 129),
            "borderline_high": (130, 159),
            "high": (160, 189),
            "very_high": (190, 9999)
        }
    },
    "vldl_cholesterol": {
        "aliases": ["vldl", "vldl-c"],
        "unit": "mg/dL",
        "ref_range": {"all": (0, 30)},
        "category": "Lipid Profile",
        "description": "Very low-density lipoprotein cholesterol"
    },

    # ============================================================
    # LIVER FUNCTION TEST (LFT)
    # ============================================================
    "total_bilirubin": {
        "aliases": ["bilirubin total", "serum bilirubin", "t. bilirubin"],
        "unit": "mg/dL",
        "ref_range": {"all": (0.1, 1.2)},
        "critical_high": 15.0,
        "category": "Liver Function",
        "description": "Breakdown product of hemoglobin processed by liver"
    },
    "direct_bilirubin": {
        "aliases": ["conjugated bilirubin", "d. bilirubin"],
        "unit": "mg/dL",
        "ref_range": {"all": (0.0, 0.3)},
        "category": "Liver Function",
        "description": "Bilirubin conjugated by the liver"
    },
    "indirect_bilirubin": {
        "aliases": ["unconjugated bilirubin"],
        "unit": "mg/dL",
        "ref_range": {"all": (0.1, 1.0)},
        "category": "Liver Function",
        "description": "Unconjugated bilirubin before liver processing"
    },
    "sgot_ast": {
        "aliases": ["sgot", "ast", "aspartate aminotransferase", "aspartate transaminase"],
        "unit": "U/L",
        "ref_range": {"all": (0, 40)},
        "critical_high": 1000,
        "category": "Liver Function",
        "description": "Enzyme found in liver, heart, muscle — marker of liver injury"
    },
    "sgpt_alt": {
        "aliases": ["sgpt", "alt", "alanine aminotransferase", "alanine transaminase"],
        "unit": "U/L",
        "ref_range": {"all": (0, 41)},
        "critical_high": 1000,
        "category": "Liver Function",
        "description": "Liver-specific enzyme — most sensitive marker of hepatocellular injury"
    },
    "alkaline_phosphatase": {
        "aliases": ["alp", "alk phos", "alkaline phosphatase alp"],
        "unit": "U/L",
        "ref_range": {"all": (44, 147)},
        "category": "Liver Function",
        "description": "Enzyme from liver and bones — elevated in cholestasis"
    },
    "total_protein": {
        "aliases": ["serum total protein", "tp"],
        "unit": "g/dL",
        "ref_range": {"all": (6.0, 8.3)},
        "category": "Liver Function",
        "description": "Total albumin + globulin in serum"
    },
    "albumin": {
        "aliases": ["serum albumin", "alb"],
        "unit": "g/dL",
        "ref_range": {"all": (3.5, 5.5)},
        "category": "Liver Function",
        "description": "Major serum protein synthesized by liver"
    },
    "globulin": {
        "aliases": ["serum globulin"],
        "unit": "g/dL",
        "ref_range": {"all": (2.0, 3.5)},
        "category": "Liver Function",
        "description": "Immune-related proteins in blood"
    },
    "ggt": {
        "aliases": ["gamma gt", "gamma glutamyl transferase", "gamma-glutamyl transpeptidase",
                     "ggt gamma gt"],
        "unit": "U/L",
        "ref_range": {"male": (0, 55), "female": (0, 38)},
        "category": "Liver Function",
        "description": "Enzyme sensitive to alcohol and cholestasis"
    },

    # ============================================================
    # THYROID FUNCTION
    # ============================================================
    "tsh": {
        "aliases": ["thyroid stimulating hormone", "tsh ultrasensitive", "tsh 3rd gen",
                     "tsh ultra sensitive"],
        "unit": "µIU/mL",
        "ref_range": {"all": (0.35, 4.94)},
        "critical_low": 0.01,
        "critical_high": 50.0,
        "category": "Thyroid",
        "description": "Pituitary hormone controlling thyroid function"
    },
    "free_t3": {
        "aliases": ["ft3", "free triiodothyronine"],
        "unit": "pg/mL",
        "ref_range": {"all": (1.71, 3.71)},
        "category": "Thyroid",
        "description": "Active thyroid hormone (unbound)"
    },
    "free_t4": {
        "aliases": ["ft4", "free thyroxine"],
        "unit": "ng/dL",
        "ref_range": {"all": (0.70, 1.48)},
        "category": "Thyroid",
        "description": "Major thyroid hormone (unbound)"
    },
    "total_t3": {
        "aliases": ["t3 total", "t3", "triiodothyronine"],
        "unit": "ng/dL",
        "ref_range": {"all": (60, 200)},
        "category": "Thyroid",
        "description": "Total T3 (bound + unbound)"
    },
    "total_t4": {
        "aliases": ["t4 total", "t4", "thyroxine"],
        "unit": "µg/dL",
        "ref_range": {"all": (4.5, 12.0)},
        "category": "Thyroid",
        "description": "Total T4 (bound + unbound)"
    },
    "anti_tpo": {
        "aliases": ["anti-tpo antibodies", "anti tpo", "tpo antibodies",
                     "thyroid peroxidase antibody"],
        "unit": "IU/mL",
        "ref_range": {"all": (0, 34)},
        "category": "Thyroid",
        "description": "Autoimmune marker for Hashimoto's thyroiditis"
    },

    # ============================================================
    # KIDNEY / RENAL FUNCTION
    # ============================================================
    "blood_urea": {
        "aliases": ["urea", "serum urea"],
        "unit": "mg/dL",
        "ref_range": {"all": (17, 43)},
        "category": "Kidney Function",
        "description": "Waste product from protein metabolism filtered by kidneys"
    },
    "bun": {
        "aliases": ["blood urea nitrogen"],
        "unit": "mg/dL",
        "ref_range": {"all": (7, 20)},
        "critical_high": 100,
        "category": "Kidney Function",
        "description": "Nitrogen component of urea — reflects kidney filtration"
    },
    "serum_creatinine": {
        "aliases": ["creatinine", "s. creatinine"],
        "unit": "mg/dL",
        "ref_range": {"male": (0.7, 1.3), "female": (0.6, 1.1)},
        "critical_high": 10.0,
        "category": "Kidney Function",
        "description": "Muscle metabolism waste product — gold standard for kidney function"
    },
    "uric_acid": {
        "aliases": ["serum uric acid"],
        "unit": "mg/dL",
        "ref_range": {"male": (3.5, 7.2), "female": (2.6, 6.0)},
        "category": "Kidney Function",
        "description": "Purine metabolism end product — elevated in gout"
    },
    "egfr": {
        "aliases": ["estimated gfr", "gfr", "egfr ckd-epi", "glomerular filtration rate"],
        "unit": "mL/min/1.73m²",
        "ref_range": {"all": (90, 999)},
        "category": "Kidney Function",
        "description": "Estimated glomerular filtration rate — overall kidney function score",
        "interpretation_bands": {
            "normal": (90, 999),
            "mildly_decreased": (60, 89),
            "moderately_decreased": (30, 59),
            "severely_decreased": (15, 29),
            "kidney_failure": (0, 14)
        }
    },
    "sodium": {
        "aliases": ["na+", "na", "serum sodium"],
        "unit": "mEq/L",
        "ref_range": {"all": (136, 145)},
        "critical_low": 120,
        "critical_high": 160,
        "category": "Electrolytes",
        "description": "Major extracellular cation"
    },
    "potassium": {
        "aliases": ["k+", "k", "serum potassium"],
        "unit": "mEq/L",
        "ref_range": {"all": (3.5, 5.1)},
        "critical_low": 2.5,
        "critical_high": 6.5,
        "category": "Electrolytes",
        "description": "Major intracellular cation — critical for cardiac function"
    },
    "chloride": {
        "aliases": ["cl-", "cl", "serum chloride"],
        "unit": "mEq/L",
        "ref_range": {"all": (98, 106)},
        "category": "Electrolytes",
        "description": "Major extracellular anion"
    },
    "calcium": {
        "aliases": ["ca", "serum calcium", "total calcium"],
        "unit": "mg/dL",
        "ref_range": {"all": (8.5, 10.5)},
        "critical_low": 6.0,
        "critical_high": 13.0,
        "category": "Electrolytes",
        "description": "Essential for bones, muscles, and nerve function"
    },
    "phosphorus": {
        "aliases": ["phosphate", "serum phosphorus", "inorganic phosphorus"],
        "unit": "mg/dL",
        "ref_range": {"all": (2.5, 4.5)},
        "category": "Electrolytes",
        "description": "Essential for bones and energy metabolism"
    },

    # ============================================================
    # BLOOD GLUCOSE / DIABETES
    # ============================================================
    "fasting_blood_sugar": {
        "aliases": ["fbs", "fasting glucose", "fasting blood glucose", "fbg"],
        "unit": "mg/dL",
        "ref_range": {"all": (70, 100)},
        "critical_low": 40,
        "critical_high": 500,
        "category": "Blood Glucose",
        "description": "Blood sugar level after 8-12 hours fasting",
        "interpretation_bands": {
            "normal": (70, 100),
            "prediabetes": (100, 125),
            "diabetes": (126, 9999)
        }
    },
    "hba1c": {
        "aliases": ["glycated haemoglobin", "glycated hemoglobin", "a1c",
                     "hba1c glycated haemoglobin"],
        "unit": "%",
        "ref_range": {"all": (0, 5.7)},
        "category": "Blood Glucose",
        "description": "3-month average blood sugar indicator",
        "interpretation_bands": {
            "normal": (0, 5.7),
            "prediabetes": (5.7, 6.4),
            "diabetes": (6.5, 9999)
        }
    },

    # ============================================================
    # VITAMINS & MINERALS
    # ============================================================
    "vitamin_d": {
        "aliases": ["vit d", "vitamin d3", "25-oh vitamin d", "25 hydroxy vitamin d",
                     "25-oh vit d", "cholecalciferol"],
        "unit": "ng/mL",
        "ref_range": {"all": (30, 100)},
        "category": "Vitamins",
        "description": "Fat-soluble vitamin essential for bone health and immunity",
        "interpretation_bands": {
            "deficient": (0, 20),
            "insufficient": (20, 29),
            "sufficient": (30, 100),
            "potentially_toxic": (100, 9999)
        }
    },
    "vitamin_b12": {
        "aliases": ["vit b12", "cobalamin", "cyanocobalamin", "serum b12",
                     "b12", "vitamin b 12"],
        "unit": "pg/mL",
        "ref_range": {"all": (211, 946)},
        "category": "Vitamins",
        "description": "Essential for nerve function and DNA synthesis"
    },
    "iron_serum": {
        "aliases": ["iron", "serum iron", "fe"],
        "unit": "µg/dL",
        "ref_range": {"male": (65, 175), "female": (50, 170)},
        "category": "Iron Studies",
        "description": "Iron level in blood serum"
    },
    "ferritin": {
        "aliases": ["serum ferritin"],
        "unit": "ng/mL",
        "ref_range": {"male": (20, 250), "female": (10, 120)},
        "category": "Iron Studies",
        "description": "Iron storage protein — reflects total body iron stores"
    },
    "tibc": {
        "aliases": ["total iron binding capacity"],
        "unit": "µg/dL",
        "ref_range": {"all": (250, 370)},
        "category": "Iron Studies",
        "description": "Measures transferrin's capacity to bind iron"
    },
    "transferrin_saturation": {
        "aliases": ["tsat", "transferrin sat", "iron saturation"],
        "unit": "%",
        "ref_range": {"all": (20, 50)},
        "category": "Iron Studies",
        "description": "Percentage of transferrin bound with iron"
    },
    "folate": {
        "aliases": ["folic acid", "serum folate", "vitamin b9"],
        "unit": "ng/mL",
        "ref_range": {"all": (3.0, 17.0)},
        "category": "Vitamins",
        "description": "Essential for DNA synthesis and cell division"
    },

    # ============================================================
    # INFECTIOUS DISEASE MARKERS
    # ============================================================
    "crp": {
        "aliases": ["c-reactive protein", "c reactive protein", "hs-crp", "high sensitivity crp",
                     "hs crp", "cardio crp"],
        "unit": "mg/L",
        "ref_range": {"all": (0, 5)},
        "critical_high": 200,
        "category": "Inflammatory Markers",
        "description": "Acute-phase protein — rises rapidly in infection and inflammation",
        "interpretation_bands": {
            "normal": (0, 5),
            "mild_inflammation": (5, 10),
            "moderate_inflammation": (10, 50),
            "severe_infection_or_autoimmune": (50, 200),
            "critical_sepsis_or_trauma": (200, 9999)
        }
    },
    "procalcitonin": {
        "aliases": ["pct", "pro-calcitonin"],
        "unit": "ng/mL",
        "ref_range": {"all": (0, 0.05)},
        "critical_high": 10.0,
        "category": "Inflammatory Markers",
        "description": "Specific marker for bacterial infection — helps differentiate from viral",
        "interpretation_bands": {
            "normal": (0, 0.05),
            "possible_local_infection": (0.05, 0.5),
            "likely_bacterial_sepsis": (0.5, 2.0),
            "severe_sepsis": (2.0, 10.0),
            "septic_shock": (10.0, 9999)
        }
    },
    "cd4_count": {
        "aliases": ["cd4", "cd4 cell count", "cd4+ t cells", "t helper cells",
                     "cd4 absolute count"],
        "unit": "cells/µL",
        "ref_range": {"all": (500, 1500)},
        "critical_low": 200,
        "category": "Immunology / HIV",
        "description": "T-helper lymphocyte count — key marker for HIV staging and immune status",
        "interpretation_bands": {
            "normal": (500, 1500),
            "mild_immunosuppression": (350, 499),
            "advanced_immunosuppression": (200, 349),
            "severe_immunodeficiency_aids": (0, 199)
        }
    },
    "hiv_viral_load": {
        "aliases": ["hiv rna", "hiv-1 rna", "viral load hiv", "hiv pcr"],
        "unit": "copies/mL",
        "ref_range": {"all": (0, 20)},
        "category": "Immunology / HIV",
        "description": "HIV RNA level — undetectable (<20) is the treatment goal",
        "interpretation_bands": {
            "undetectable": (0, 20),
            "low_level_viremia": (20, 200),
            "virological_failure": (200, 1000),
            "high_viral_load": (1000, 9999999)
        }
    },
    "hbsag": {
        "aliases": ["hepatitis b surface antigen", "hbs ag", "hep b surface antigen"],
        "unit": "",
        "ref_range": {"all": (0, 0.99)},
        "category": "Hepatitis",
        "description": "Hepatitis B surface antigen — positive indicates active HBV infection"
    },
    "anti_hcv": {
        "aliases": ["hepatitis c antibody", "hcv antibody", "anti-hcv", "hep c antibody"],
        "unit": "",
        "ref_range": {"all": (0, 0.99)},
        "category": "Hepatitis",
        "description": "Hepatitis C antibody — positive indicates exposure/infection, confirm with HCV RNA"
    },
    "dengue_ns1": {
        "aliases": ["ns1 antigen", "dengue ns1 antigen", "ns1 ag"],
        "unit": "",
        "ref_range": {"all": (0, 0.99)},
        "category": "Infectious Disease",
        "description": "Dengue NS1 antigen — positive in first 5 days of fever indicates acute dengue"
    },
    "dengue_igm": {
        "aliases": ["dengue igm antibody", "dengue igm"],
        "unit": "",
        "ref_range": {"all": (0, 0.99)},
        "category": "Infectious Disease",
        "description": "Dengue IgM — positive after day 5 indicates recent dengue infection"
    },
    "malaria_antigen": {
        "aliases": ["malaria rapid test", "malaria antigen test", "mp antigen",
                     "plasmodium antigen", "malaria rdt"],
        "unit": "",
        "ref_range": {"all": (0, 0.99)},
        "category": "Infectious Disease",
        "description": "Malaria rapid diagnostic test — detects Plasmodium antigens"
    },
    "widal_o": {
        "aliases": ["widal test o", "typhoid o", "salmonella typhi o"],
        "unit": "titre",
        "ref_range": {"all": (0, 80)},
        "category": "Infectious Disease",
        "description": "Widal O titre — ≥1:160 suggestive of typhoid in endemic areas"
    },
    "widal_h": {
        "aliases": ["widal test h", "typhoid h", "salmonella typhi h"],
        "unit": "titre",
        "ref_range": {"all": (0, 80)},
        "category": "Infectious Disease",
        "description": "Widal H titre — supports typhoid diagnosis when rising titres demonstrated"
    },
    "ada": {
        "aliases": ["adenosine deaminase", "ada level", "pleural ada", "csf ada"],
        "unit": "U/L",
        "ref_range": {"all": (0, 40)},
        "category": "Infectious Disease",
        "description": "Adenosine Deaminase — elevated in tuberculous effusions (pleural/CSF)"
    },
    "quantiferon": {
        "aliases": ["quantiferon tb gold", "igra", "interferon gamma release assay",
                     "tb gold", "qft"],
        "unit": "IU/mL",
        "ref_range": {"all": (0, 0.35)},
        "category": "Infectious Disease",
        "description": "Interferon-gamma release assay — detects latent and active TB infection"
    },
    "d_dimer": {
        "aliases": ["d-dimer", "ddimer", "fibrin degradation"],
        "unit": "ng/mL",
        "ref_range": {"all": (0, 500)},
        "critical_high": 5000,
        "category": "Coagulation / COVID Markers",
        "description": "Fibrin degradation product — elevated in DVT, PE, DIC, and COVID-19 coagulopathy"
    },
    "il6": {
        "aliases": ["interleukin 6", "interleukin-6", "il-6"],
        "unit": "pg/mL",
        "ref_range": {"all": (0, 7)},
        "critical_high": 100,
        "category": "Inflammatory Markers",
        "description": "Pro-inflammatory cytokine — markedly elevated in cytokine storm and severe sepsis"
    },
    "ldh": {
        "aliases": ["lactate dehydrogenase", "lactic dehydrogenase", "serum ldh"],
        "unit": "U/L",
        "ref_range": {"all": (140, 280)},
        "category": "Tumour Markers / General",
        "description": "Non-specific marker — elevated in tissue damage, haemolysis, lymphoma, and many malignancies"
    },

    # ============================================================
    # TUMOUR MARKERS
    # ============================================================
    "psa": {
        "aliases": ["prostate specific antigen", "total psa", "serum psa", "psa total"],
        "unit": "ng/mL",
        "ref_range": {"male": (0, 4.0)},
        "category": "Tumour Markers",
        "description": "Prostate-specific antigen — screening marker for prostate cancer",
        "interpretation_bands": {
            "normal": (0, 4.0),
            "grey_zone": (4.0, 10.0),
            "suspicious": (10.0, 20.0),
            "highly_suspicious": (20.0, 9999)
        }
    },
    "ca125": {
        "aliases": ["ca-125", "cancer antigen 125", "ovarian cancer marker"],
        "unit": "U/mL",
        "ref_range": {"female": (0, 35)},
        "category": "Tumour Markers",
        "description": "Ovarian cancer marker — also elevated in endometriosis, PID, liver cirrhosis"
    },
    "cea": {
        "aliases": ["carcinoembryonic antigen", "carcino embryonic antigen"],
        "unit": "ng/mL",
        "ref_range": {"all": (0, 5.0)},
        "category": "Tumour Markers",
        "description": "Colorectal, lung, breast cancer marker — used for monitoring, not primary diagnosis"
    },
    "afp": {
        "aliases": ["alpha fetoprotein", "alpha-fetoprotein", "serum afp", "alfa fetoprotein"],
        "unit": "ng/mL",
        "ref_range": {"all": (0, 10)},
        "category": "Tumour Markers",
        "description": "Hepatocellular carcinoma and testicular cancer marker"
    },
    "ca199": {
        "aliases": ["ca 19-9", "ca19-9", "cancer antigen 19-9", "ca-19-9"],
        "unit": "U/mL",
        "ref_range": {"all": (0, 37)},
        "category": "Tumour Markers",
        "description": "Pancreatic and biliary cancer marker — also elevated in cholestasis and pancreatitis"
    },
    "beta_hcg": {
        "aliases": ["hcg", "beta hcg", "human chorionic gonadotropin", "b-hcg",
                     "serum hcg", "bhcg"],
        "unit": "mIU/mL",
        "ref_range": {"male": (0, 5), "female": (0, 5)},
        "category": "Tumour Markers",
        "description": "Pregnancy marker; in males/non-pregnant females, elevated suggests testicular or gestational trophoblastic tumour"
    },
    "spep": {
        "aliases": ["serum protein electrophoresis", "protein electrophoresis",
                     "spep pattern", "m spike", "m band"],
        "unit": "",
        "ref_range": {"all": (0, 0)},
        "category": "Tumour Markers",
        "description": "Detects monoclonal protein bands (M-spike) — key screening for multiple myeloma and MGUS"
    },

    # ============================================================
    # GENETIC / HAEMATOLOGICAL MARKERS
    # ============================================================
    "hba_electrophoresis": {
        "aliases": ["hb electrophoresis", "haemoglobin electrophoresis", "hemoglobin electrophoresis",
                     "hplc haemoglobin", "hb hplc", "hba2", "hb a2"],
        "unit": "%",
        "ref_range": {"all": (95, 98)},
        "category": "Genetic / Haematology",
        "description": "Separates haemoglobin variants — screens for sickle cell disease, thalassemia major/trait"
    },
    "hbs_percentage": {
        "aliases": ["hb s", "hbs", "sickle haemoglobin", "sickle hemoglobin"],
        "unit": "%",
        "ref_range": {"all": (0, 0)},
        "category": "Genetic / Haematology",
        "description": "HbS percentage — >50% indicates sickle cell disease, 20-40% indicates sickle trait"
    },
    "hba2_percentage": {
        "aliases": ["hb a2 level", "hba2 level"],
        "unit": "%",
        "ref_range": {"all": (2.0, 3.3)},
        "category": "Genetic / Haematology",
        "description": "HbA2 — elevated (3.5-8%) in beta-thalassemia trait; key diagnostic test"
    },
    "hbf_percentage": {
        "aliases": ["hb f", "fetal haemoglobin", "fetal hemoglobin", "hbf"],
        "unit": "%",
        "ref_range": {"all": (0, 2)},
        "category": "Genetic / Haematology",
        "description": "Fetal haemoglobin — elevated in thalassemia major, sickle cell disease, HPFH"
    },
    "g6pd": {
        "aliases": ["glucose-6-phosphate dehydrogenase", "g6pd level", "g6pd activity",
                     "g6pd quantitative"],
        "unit": "U/g Hb",
        "ref_range": {"male": (4.6, 13.5), "female": (4.6, 13.5)},
        "category": "Genetic / Haematology",
        "description": "G6PD enzyme activity — deficiency causes drug/food-induced haemolytic anaemia"
    },

    # ============================================================
    # COAGULATION PANEL
    # ============================================================
    "pt": {
        "aliases": ["prothrombin time", "pro time", "pt seconds"],
        "unit": "seconds",
        "ref_range": {"all": (11.0, 13.5)},
        "critical_high": 30.0,
        "category": "Coagulation",
        "description": "Prothrombin time — measures extrinsic pathway; prolonged in warfarin use, liver disease, DIC"
    },
    "inr": {
        "aliases": ["international normalized ratio", "pt/inr"],
        "unit": "",
        "ref_range": {"all": (0.8, 1.2)},
        "critical_high": 5.0,
        "category": "Coagulation",
        "description": "Standardized PT ratio — therapeutic range 2.0-3.0 on warfarin; >5.0 = bleeding risk"
    },
    "aptt": {
        "aliases": ["activated partial thromboplastin time", "ptt", "partial thromboplastin time"],
        "unit": "seconds",
        "ref_range": {"all": (25, 35)},
        "critical_high": 100,
        "category": "Coagulation",
        "description": "Measures intrinsic pathway — prolonged in haemophilia A/B, heparin use, DIC, lupus anticoagulant"
    },
    "fibrinogen": {
        "aliases": ["serum fibrinogen", "plasma fibrinogen", "factor i"],
        "unit": "mg/dL",
        "ref_range": {"all": (200, 400)},
        "critical_low": 100,
        "category": "Coagulation",
        "description": "Clotting factor — low in DIC, liver failure; elevated as acute-phase reactant in infection"
    },
}


def get_reference(test_name: str) -> dict | None:
    """Look up reference range by canonical name or any alias."""
    key = test_name.lower().strip()

    # Direct match
    if key in REFERENCE_RANGES:
        return REFERENCE_RANGES[key]

    # Alias match
    for canonical, data in REFERENCE_RANGES.items():
        if key in [a.lower() for a in data["aliases"]]:
            return {**data, "canonical_name": canonical}

    return None


def get_all_aliases() -> dict[str, str]:
    """Return a flat mapping of every alias -> canonical name."""
    alias_map = {}
    for canonical, data in REFERENCE_RANGES.items():
        alias_map[canonical] = canonical
        for alias in data["aliases"]:
            alias_map[alias.lower()] = canonical
    return alias_map

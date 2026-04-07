"""
Medical Knowledge Base — Curated Clinical Knowledge for RAG
=============================================================
Structured medical knowledge from open-access sources:
- MSD Manuals (Merck Manual — open access)
- WHO Clinical Guidelines
- Harrison's Principles (summarized interpretations)
- Standard clinical practice guidelines (ADA, AHA, KDIGO, ATA, etc.)

Each entry is a self-contained "knowledge chunk" designed for embedding + retrieval.
Format: {id, category, title, content, source, tags}
"""

MEDICAL_KNOWLEDGE = [

    # ================================================================
    # COMPLETE BLOOD COUNT — INTERPRETATIONS
    # ================================================================
    {
        "id": "cbc_001",
        "category": "CBC",
        "title": "Low Haemoglobin — Anaemia Classification",
        "content": (
            "Haemoglobin below the reference range indicates anaemia. Classification by severity: "
            "Mild anaemia (Hb 10-12.9 g/dL males, 10-11.9 females), Moderate (7-9.9 g/dL), Severe (<7 g/dL). "
            "Classification by MCV: Microcytic (MCV<80 fL) suggests iron deficiency or thalassemia; "
            "Normocytic (MCV 80-100 fL) suggests chronic disease, acute blood loss, or renal failure; "
            "Macrocytic (MCV>100 fL) suggests B12/folate deficiency or liver disease. "
            "Iron deficiency is the most common cause globally, affecting ~25% of the world population per WHO. "
            "Key confirmatory tests: serum ferritin (<30 ng/mL confirms iron deficiency), iron studies (low serum iron + high TIBC), "
            "peripheral blood smear, reticulocyte count. In Indian adults, dietary iron deficiency and vegetarian diets are leading causes."
        ),
        "source": "WHO Global Anaemia Guidelines 2023; Harrison's Principles Ch. 93",
        "tags": ["haemoglobin", "anaemia", "iron deficiency", "mcv", "cbc"]
    },
    {
        "id": "cbc_002",
        "category": "CBC",
        "title": "Elevated WBC Count — Leukocytosis",
        "content": (
            "WBC count above 10,000 cells/µL is leukocytosis. Common causes: bacterial infection (most common), "
            "inflammation, stress response, corticosteroid use, smoking, post-exercise. "
            "Neutrophilia (neutrophils >70%): bacterial infection, tissue necrosis, inflammatory disorders. "
            "Lymphocytosis (lymphocytes >40%): viral infections (EBV, CMV, hepatitis), chronic lymphocytic leukemia. "
            "Eosinophilia (eosinophils >6%): allergic conditions, parasitic infections, drug reactions. "
            "WBC >30,000 with blast cells warrants urgent haematology referral to exclude leukaemia. "
            "Mild leukocytosis (10,000-15,000) with neutrophilia in an otherwise well patient often reflects "
            "acute infection and resolves with treatment."
        ),
        "source": "Harrison's Principles Ch. 60; MSD Manual — Leukocytosis",
        "tags": ["wbc", "leukocytosis", "neutrophilia", "infection", "cbc"]
    },
    {
        "id": "cbc_003",
        "category": "CBC",
        "title": "Elevated ESR — Non-Specific Inflammation Marker",
        "content": (
            "ESR (Erythrocyte Sedimentation Rate) is a non-specific marker of inflammation. "
            "Elevated ESR indicates: infection, autoimmune disease (RA, SLE, PMR), malignancy, chronic kidney disease, "
            "anaemia itself (low Hb increases ESR). ESR >100 mm/hr strongly suggests: multiple myeloma, "
            "temporal arteritis, severe infection, or metastatic malignancy. "
            "ESR rises slowly (days) and falls slowly — not useful for acute monitoring. "
            "CRP is preferred for acute-phase tracking as it rises and falls faster. "
            "Age-adjusted upper limit: Age/2 for males, (Age+10)/2 for females."
        ),
        "source": "Harrison's Principles Ch. 60; Tietz Clinical Guide",
        "tags": ["esr", "inflammation", "infection", "autoimmune", "cbc"]
    },
    {
        "id": "cbc_004",
        "category": "CBC",
        "title": "Elevated RDW — Red Cell Size Variation",
        "content": (
            "RDW (Red Cell Distribution Width) >14.5% indicates anisocytosis — variation in red blood cell size. "
            "High RDW with low MCV: iron deficiency anaemia (most common), thalassemia trait (RDW usually normal in thalassemia — "
            "this distinction helps differentiate the two). High RDW with high MCV: B12/folate deficiency, mixed deficiency. "
            "High RDW with normal MCV: early iron deficiency, combined iron + B12 deficiency, chronic disease. "
            "RDW is increasingly studied as an independent predictor of cardiovascular mortality and all-cause mortality."
        ),
        "source": "Tietz Clinical Guide to Laboratory Tests; Harrison's Principles Ch. 93",
        "tags": ["rdw", "anisocytosis", "iron deficiency", "thalassemia", "cbc"]
    },

    # ================================================================
    # LIPID PROFILE — INTERPRETATIONS
    # ================================================================
    {
        "id": "lipid_001",
        "category": "Lipid Profile",
        "title": "Elevated Total Cholesterol and LDL — Cardiovascular Risk",
        "content": (
            "Total cholesterol >200 mg/dL and LDL >100 mg/dL indicate dyslipidemia with increased cardiovascular risk. "
            "LDL classification: Optimal <100, Near-optimal 100-129, Borderline-high 130-159, High 160-189, Very high ≥190 mg/dL. "
            "LDL is the primary therapeutic target per AHA/ACC guidelines. Every 1 mmol/L (39 mg/dL) reduction in LDL "
            "reduces major cardiovascular events by ~22%. "
            "Indian population has a higher prevalence of atherogenic dyslipidemia (high TG + low HDL + small dense LDL). "
            "First-line intervention: lifestyle modification (diet — reduce saturated fat to <7% of calories, increase soluble fibre, "
            "exercise 150 min/week). If LDL >160 or cardiovascular risk is high, statin therapy is indicated. "
            "Non-HDL cholesterol (Total - HDL) is a secondary target capturing VLDL atherogenic particles."
        ),
        "source": "AHA/ACC 2018 Cholesterol Guidelines; Harrison's Principles Ch. 400",
        "tags": ["cholesterol", "ldl", "cardiovascular", "dyslipidemia", "statin", "lipid"]
    },
    {
        "id": "lipid_002",
        "category": "Lipid Profile",
        "title": "Elevated Triglycerides — Metabolic and Cardiac Risk",
        "content": (
            "Triglycerides: Normal <150, Borderline-high 150-199, High 200-499, Very high ≥500 mg/dL. "
            "Causes of elevated TG: obesity, metabolic syndrome, uncontrolled diabetes, excessive alcohol, "
            "high carbohydrate diet (especially refined sugars), hypothyroidism, nephrotic syndrome, medications (beta-blockers, thiazides). "
            "TG ≥500 mg/dL: risk of acute pancreatitis — requires urgent treatment. "
            "Indian diet rich in refined carbohydrates and cooking oils contributes to high TG prevalence. "
            "Management: weight loss (5-10% reduces TG by 20%), reduce refined carbs and alcohol, omega-3 fatty acids, "
            "exercise. If TG >500, fibrates (fenofibrate) are first-line pharmacotherapy."
        ),
        "source": "AHA/ACC Guidelines; Endocrine Society Clinical Practice Guideline on Hypertriglyceridemia",
        "tags": ["triglycerides", "metabolic syndrome", "pancreatitis", "lipid"]
    },
    {
        "id": "lipid_003",
        "category": "Lipid Profile",
        "title": "Low HDL Cholesterol — Atherogenic Risk Factor",
        "content": (
            "HDL <40 mg/dL (males) or <50 mg/dL (females) is an independent cardiovascular risk factor. "
            "HDL performs reverse cholesterol transport — removing cholesterol from arterial walls. "
            "Low HDL is a hallmark of metabolic syndrome (along with high TG, central obesity, elevated BP, impaired fasting glucose). "
            "Causes: sedentary lifestyle, smoking, obesity, high-carbohydrate diet, type 2 diabetes, genetic factors. "
            "Non-pharmacological improvement: aerobic exercise (raises HDL by 5-10%), smoking cessation, weight loss, "
            "moderate alcohol intake. No drug has convincingly shown that raising HDL reduces CV events independently — "
            "focus remains on LDL lowering. "
            "TC/HDL ratio >4.5 and LDL/HDL ratio >3.0 indicate significantly elevated atherogenic risk."
        ),
        "source": "AHA/ACC 2018 Guidelines; Harrison's Principles Ch. 400",
        "tags": ["hdl", "cardiovascular", "metabolic syndrome", "atherogenic", "lipid"]
    },

    # ================================================================
    # LIVER FUNCTION — INTERPRETATIONS
    # ================================================================
    {
        "id": "liver_001",
        "category": "Liver Function",
        "title": "Elevated AST and ALT — Hepatocellular Pattern",
        "content": (
            "AST (SGOT) and ALT (SGPT) are aminotransferase enzymes released during hepatocyte injury. "
            "ALT is more liver-specific than AST (AST is also found in heart, muscle, kidney). "
            "Pattern recognition: ALT > AST suggests non-alcoholic fatty liver disease (NAFLD), viral hepatitis, drug-induced injury. "
            "AST > ALT (ratio >2:1) strongly suggests alcoholic liver disease. "
            "Mild elevation (1-3x ULN): NAFLD (most common cause globally), medications (statins, NSAIDs, antibiotics), "
            "chronic hepatitis B/C, hemochromatosis, autoimmune hepatitis, celiac disease. "
            "Moderate elevation (3-10x ULN): acute viral hepatitis, autoimmune flare, drug toxicity. "
            "Severe elevation (>10x ULN): acute viral hepatitis, ischemic hepatitis, acetaminophen toxicity, autoimmune hepatitis flare. "
            "NAFLD affects an estimated 30-40% of Indian urban population. Initial workup: hepatitis B/C serology, "
            "abdominal ultrasound, alcohol history, medication review."
        ),
        "source": "ACG Clinical Guideline for Evaluation of Abnormal Liver Chemistries; Harrison's Ch. 334",
        "tags": ["ast", "alt", "sgot", "sgpt", "liver", "nafld", "hepatitis"]
    },
    {
        "id": "liver_002",
        "category": "Liver Function",
        "title": "Elevated GGT — Alcohol, Cholestasis, and Metabolic Causes",
        "content": (
            "GGT (Gamma-Glutamyl Transferase) is highly sensitive but non-specific for liver disease. "
            "Elevated GGT with elevated ALP suggests cholestatic (biliary) disease. "
            "Elevated GGT with elevated ALT/AST suggests hepatocellular disease with possible alcohol component. "
            "Isolated GGT elevation: alcohol use (most common — GGT is the most sensitive marker of alcohol intake), "
            "medications (phenytoin, barbiturates, carbamazepine), NAFLD, metabolic syndrome, pancreatic disease. "
            "GGT is now recognized as an independent predictor of metabolic syndrome and cardiovascular disease. "
            "If GGT elevated with normal ALP: consider alcohol, medications, or metabolic syndrome rather than cholestasis."
        ),
        "source": "ACG Guidelines; MSD Manual — GGT",
        "tags": ["ggt", "liver", "alcohol", "cholestasis", "metabolic syndrome"]
    },
    {
        "id": "liver_003",
        "category": "Liver Function",
        "title": "Elevated Bilirubin — Jaundice Differential",
        "content": (
            "Total bilirubin >1.2 mg/dL is elevated; clinical jaundice appears at >2.5 mg/dL. "
            "Unconjugated (indirect) hyperbilirubinemia: hemolysis, Gilbert syndrome (benign, affects 5-10% of population — "
            "unconjugated bilirubin rises with fasting/stress), ineffective erythropoiesis. "
            "Conjugated (direct) hyperbilirubinemia: hepatocellular disease (hepatitis, cirrhosis), "
            "cholestasis (gallstones, pancreatic head tumour, drug-induced), sepsis. "
            "Mild isolated unconjugated elevation (1.2-3 mg/dL) in a young healthy adult with normal LFT: most likely Gilbert syndrome — "
            "benign, no treatment needed. Confirm with fasting provocation test."
        ),
        "source": "Harrison's Principles Ch. 334; MSD Manual — Jaundice",
        "tags": ["bilirubin", "jaundice", "gilbert", "liver", "cholestasis"]
    },

    # ================================================================
    # THYROID — INTERPRETATIONS
    # ================================================================
    {
        "id": "thyroid_001",
        "category": "Thyroid",
        "title": "Elevated TSH — Hypothyroidism Spectrum",
        "content": (
            "TSH >4.94 µIU/mL with normal Free T4: subclinical hypothyroidism. "
            "TSH >4.94 with low Free T4 (<0.70 ng/dL): overt hypothyroidism. "
            "Most common cause worldwide: Hashimoto thyroiditis (autoimmune) — confirmed by positive Anti-TPO antibodies. "
            "In iodine-sufficient areas like urban India, Hashimoto's accounts for >90% of hypothyroidism cases. "
            "Symptoms: fatigue, weight gain, cold intolerance, constipation, dry skin, hair loss, menstrual irregularity, depression. "
            "Subclinical hypothyroidism (TSH 4.5-10, normal FT4): treat if symptomatic, if Anti-TPO positive (high progression risk), "
            "if TSH >10, if pregnant or planning pregnancy. "
            "Treatment: levothyroxine 1.6 µg/kg/day (full replacement dose); start low in elderly/cardiac patients. "
            "Monitor TSH 6-8 weeks after dose change. Target TSH 0.5-2.5 µIU/mL on treatment."
        ),
        "source": "ATA 2014 Guidelines for Hypothyroidism; Harrison's Principles Ch. 375",
        "tags": ["tsh", "hypothyroidism", "hashimoto", "thyroid", "levothyroxine"]
    },
    {
        "id": "thyroid_002",
        "category": "Thyroid",
        "title": "Elevated Anti-TPO Antibodies — Autoimmune Thyroid Disease",
        "content": (
            "Anti-TPO (thyroid peroxidase antibodies) >34 IU/mL indicates autoimmune thyroid disease. "
            "Present in >90% of Hashimoto thyroiditis and 60-80% of Graves disease. "
            "In subclinical hypothyroidism, positive Anti-TPO increases annual risk of progression to overt hypothyroidism to ~4.3% "
            "(vs ~2.6% if Anti-TPO negative). "
            "Very high titres (>300 IU/mL) strongly suggest active autoimmune thyroiditis. "
            "Clinical significance: identifies patients who benefit from earlier levothyroxine initiation, "
            "predicts postpartum thyroiditis risk, and is associated with increased miscarriage risk in pregnancy. "
            "No specific treatment for antibodies themselves — treat the thyroid dysfunction they cause."
        ),
        "source": "ATA Guidelines; Harrison's Principles Ch. 375",
        "tags": ["anti-tpo", "hashimoto", "autoimmune", "thyroid"]
    },
    {
        "id": "thyroid_003",
        "category": "Thyroid",
        "title": "Low Free T4 with High TSH — Overt Hypothyroidism",
        "content": (
            "Free T4 below 0.70 ng/dL with elevated TSH confirms overt primary hypothyroidism. "
            "The most reliable pattern: high TSH + low FT4 = primary hypothyroidism (thyroid gland failure). "
            "If TSH is normal/low with low FT4: consider central (secondary) hypothyroidism — pituitary/hypothalamic cause. "
            "Immediate clinical implications: initiate levothyroxine replacement therapy. "
            "Associated metabolic effects: elevated LDL cholesterol (hypothyroidism reduces LDL receptor expression), "
            "elevated CK (subclinical myopathy), elevated prolactin, menstrual dysfunction. "
            "Many lab abnormalities (high cholesterol, high CK, anaemia) resolve with adequate thyroid replacement."
        ),
        "source": "ATA Guidelines; Endocrine Society Clinical Practice Guidelines",
        "tags": ["free t4", "hypothyroidism", "tsh", "thyroid", "levothyroxine"]
    },

    # ================================================================
    # KIDNEY FUNCTION — INTERPRETATIONS
    # ================================================================
    {
        "id": "kidney_001",
        "category": "Kidney Function",
        "title": "Elevated Uric Acid — Hyperuricemia and Gout",
        "content": (
            "Uric acid >7.2 mg/dL (males) or >6.0 mg/dL (females) is hyperuricemia. "
            "Primary cause: underexcretion of uric acid by kidneys (90% of cases) or overproduction (10%). "
            "Risk factors: purine-rich diet (red meat, organ meats, seafood), alcohol (especially beer), "
            "obesity, metabolic syndrome, chronic kidney disease, diuretic use, genetic factors. "
            "Complications: gout (acute inflammatory arthritis — classically affects first MTP joint), "
            "uric acid nephrolithiasis, chronic gouty arthritis, urate nephropathy. "
            "Asymptomatic hyperuricemia: pharmacological treatment generally not recommended unless very high (>13 mg/dL) "
            "or recurrent nephrolithiasis. Lifestyle: reduce purine intake, limit alcohol, hydrate well, weight loss. "
            "Hyperuricemia is now considered an independent risk factor for cardiovascular disease and CKD progression."
        ),
        "source": "ACR Guidelines for Gout Management 2020; Harrison's Principles Ch. 395",
        "tags": ["uric acid", "gout", "hyperuricemia", "kidney"]
    },
    {
        "id": "kidney_002",
        "category": "Kidney Function",
        "title": "eGFR Staging — Chronic Kidney Disease Classification",
        "content": (
            "eGFR (estimated Glomerular Filtration Rate) stages per KDIGO guidelines: "
            "G1: ≥90 (Normal — but if albuminuria present, still CKD). G2: 60-89 (Mildly decreased). "
            "G3a: 45-59 (Mild-moderate decrease). G3b: 30-44 (Moderate-severe decrease). "
            "G4: 15-29 (Severely decreased). G5: <15 (Kidney failure — dialysis consideration). "
            "CKD diagnosis requires eGFR <60 OR evidence of kidney damage (albuminuria, structural abnormality) "
            "persisting for >3 months. "
            "Key implications: adjust drug doses for eGFR <60 (especially metformin, NSAIDs, contrast agents). "
            "Refer to nephrology if eGFR <30 or rapid decline (>5 mL/min/year). "
            "Serum creatinine alone is insufficient — always use eGFR (CKD-EPI equation accounts for age, sex, creatinine)."
        ),
        "source": "KDIGO 2024 CKD Guidelines; Harrison's Principles Ch. 305",
        "tags": ["egfr", "ckd", "kidney", "creatinine", "nephrology"]
    },

    # ================================================================
    # BLOOD GLUCOSE / DIABETES — INTERPRETATIONS
    # ================================================================
    {
        "id": "diabetes_001",
        "category": "Blood Glucose",
        "title": "Prediabetes — FBS 100-125 and HbA1c 5.7-6.4%",
        "content": (
            "Prediabetes is defined by: Fasting glucose 100-125 mg/dL (Impaired Fasting Glucose), OR "
            "HbA1c 5.7-6.4%, OR 2-hour OGTT glucose 140-199 mg/dL (Impaired Glucose Tolerance). "
            "Annual conversion rate to type 2 diabetes: 5-10% without intervention. "
            "Landmark Diabetes Prevention Program (DPP) trial showed: lifestyle modification (7% weight loss + "
            "150 min/week moderate exercise) reduces diabetes risk by 58% — more effective than metformin (31% reduction). "
            "Indian Diabetes Prevention Programme (IDPP) confirmed similar results in Indian population. "
            "India has ~136 million prediabetics per ICMR-INDIAB study — the highest burden globally. "
            "Recommended actions: dietary modification (reduce refined carbs, increase fibre), regular exercise, "
            "weight management, annual FBS/HbA1c monitoring. Consider metformin if BMI >35 or age <60 with additional risk factors."
        ),
        "source": "ADA Standards of Medical Care in Diabetes 2024; ICMR Guidelines for Type 2 Diabetes; DPP Trial",
        "tags": ["prediabetes", "hba1c", "fasting glucose", "diabetes prevention", "blood glucose"]
    },
    {
        "id": "diabetes_002",
        "category": "Blood Glucose",
        "title": "HbA1c Interpretation — 3-Month Glycemic Average",
        "content": (
            "HbA1c reflects average blood glucose over 2-3 months (lifespan of red blood cells). "
            "Interpretation: <5.7% Normal, 5.7-6.4% Prediabetes, ≥6.5% Diabetes (diagnostic threshold). "
            "Estimated average glucose: HbA1c 6% ≈ 126 mg/dL, 7% ≈ 154 mg/dL, 8% ≈ 183 mg/dL. "
            "Treatment target for most adults with diabetes: <7% (ADA recommendation). "
            "Conditions that affect HbA1c accuracy: haemoglobin variants (HbS, HbC), iron deficiency anaemia "
            "(falsely elevates HbA1c), chronic kidney disease, pregnancy, recent blood transfusion. "
            "In India, HbA1c is preferred over fasting glucose for screening due to no fasting requirement "
            "and lower day-to-day variability."
        ),
        "source": "ADA Standards of Care 2024; ICMR Guidelines; Harrison's Principles Ch. 396",
        "tags": ["hba1c", "glycated haemoglobin", "diabetes", "blood glucose"]
    },

    # ================================================================
    # VITAMINS & MINERALS — INTERPRETATIONS
    # ================================================================
    {
        "id": "vitamin_001",
        "category": "Vitamins",
        "title": "Vitamin D Deficiency — Skeletal and Extraskeletal Effects",
        "content": (
            "25-OH Vitamin D levels: Deficient <20 ng/mL, Insufficient 20-29 ng/mL, Sufficient 30-100 ng/mL. "
            "Prevalence in India: 70-100% of the population is Vitamin D deficient despite tropical latitude — "
            "attributed to dark skin pigmentation, indoor lifestyle, pollution, vegetarian diet, and cultural practices. "
            "Skeletal effects: osteomalacia (bone softening), osteoporosis (increased fracture risk), "
            "rickets (children), muscle weakness, bone pain. "
            "Extraskeletal associations: increased cardiovascular risk, immune dysfunction, depression, "
            "insulin resistance, increased cancer risk (observational data). "
            "Treatment: Cholecalciferol (D3) — Deficiency: 60,000 IU weekly for 8 weeks loading, then 1000-2000 IU daily maintenance. "
            "Insufficiency: 1000-2000 IU daily. Recheck levels after 3 months. "
            "Co-supplement: calcium 1000 mg/day for bone health. Sun exposure 15-20 min/day on arms and face."
        ),
        "source": "Endocrine Society Clinical Practice Guideline 2024; ICMR-NIN Dietary Guidelines; Harrison's Ch. 403",
        "tags": ["vitamin d", "deficiency", "osteoporosis", "cholecalciferol", "bone health"]
    },
    {
        "id": "vitamin_002",
        "category": "Vitamins",
        "title": "Vitamin B12 Deficiency — Neurological and Haematological Effects",
        "content": (
            "Vitamin B12 <211 pg/mL is deficient. Grey zone 211-300 pg/mL may be functionally deficient. "
            "Haematological manifestation: megaloblastic anaemia (high MCV >100 fL, hypersegmented neutrophils). "
            "Neurological manifestation: subacute combined degeneration of spinal cord (posterior columns + lateral corticospinal tracts), "
            "peripheral neuropathy (tingling, numbness in hands/feet), cognitive impairment, depression. "
            "Neurological damage can occur WITHOUT anaemia — B12 must be checked independently. "
            "Causes in India: vegetarian/vegan diet (most common — B12 is found almost exclusively in animal products), "
            "pernicious anaemia (autoimmune gastritis), H. pylori infection (common in India), metformin use, PPI use. "
            "Treatment: If severe deficiency (<150 pg/mL) or neurological symptoms: IM cyanocobalamin 1000 µg daily for 7 days, "
            "then weekly for 4 weeks, then monthly. Mild deficiency: oral B12 1000-2000 µg daily. "
            "Response: reticulocytosis in 5-7 days, Hb normalizes in 6-8 weeks, neurological recovery may take 6-12 months."
        ),
        "source": "British Society for Haematology Guidelines; Harrison's Principles Ch. 93; ICMR-NIN Guidelines",
        "tags": ["vitamin b12", "deficiency", "megaloblastic", "neuropathy", "vegetarian"]
    },
    {
        "id": "vitamin_003",
        "category": "Iron Studies",
        "title": "Iron Deficiency — Comprehensive Iron Panel Interpretation",
        "content": (
            "Iron deficiency progresses through 3 stages: "
            "Stage 1 — Storage depletion: low ferritin (<30 ng/mL), normal Hb, normal iron. "
            "Stage 2 — Iron-deficient erythropoiesis: low ferritin, low serum iron, high TIBC, low transferrin saturation (<20%). "
            "Stage 3 — Iron deficiency anaemia: all of above PLUS low Hb, low MCV (microcytic), high RDW. "
            "Ferritin is the single most useful test: <30 ng/mL is diagnostic of iron deficiency (sensitivity ~92%). "
            "However, ferritin is an acute-phase reactant — may be falsely normal/elevated in inflammation, infection, liver disease. "
            "If ferritin 30-100 with clinical suspicion: check transferrin saturation (<20% confirms iron deficiency). "
            "TIBC >370 µg/dL suggests iron deficiency (body increases transferrin production to capture more iron). "
            "India has the highest burden of iron deficiency anaemia globally: ~50% of women, ~25% of men per NFHS-5. "
            "Treatment: oral ferrous sulfate 325 mg (65 mg elemental iron) 2-3 times daily on empty stomach with vitamin C. "
            "IV iron (ferric carboxymaltose) if oral intolerant, severe anaemia, or malabsorption."
        ),
        "source": "WHO Iron Deficiency Anaemia Guidelines; BSH Guidelines; Harrison's Ch. 93",
        "tags": ["iron", "ferritin", "tibc", "transferrin saturation", "iron deficiency", "anaemia"]
    },

    # ================================================================
    # COMBINED PATTERN ANALYSIS
    # ================================================================
    {
        "id": "pattern_001",
        "category": "Combined Analysis",
        "title": "Metabolic Syndrome — Diagnostic Criteria and Implications",
        "content": (
            "Metabolic syndrome (IDF/AHA harmonized criteria) requires ≥3 of: "
            "1) Waist circumference ≥90 cm (males) / ≥80 cm (females) [South Asian cutoffs]. "
            "2) Triglycerides ≥150 mg/dL. 3) HDL <40 mg/dL (males) / <50 mg/dL (females). "
            "4) Blood pressure ≥130/85 mmHg. 5) Fasting glucose ≥100 mg/dL. "
            "A lab panel showing high TG + low HDL + elevated fasting glucose strongly suggests metabolic syndrome "
            "even without BP and waist measurements. "
            "Prevalence in India: 30-40% in urban areas per ICMR studies. "
            "Metabolic syndrome doubles cardiovascular disease risk and increases type 2 diabetes risk 5-fold. "
            "Management is lifestyle-first: weight loss 7-10%, exercise 150 min/week, Mediterranean/DASH diet. "
            "Individual components may require specific pharmacotherapy (statins, antihypertensives, metformin)."
        ),
        "source": "IDF/AHA/NHLBI Joint Scientific Statement; ICMR Guidelines",
        "tags": ["metabolic syndrome", "triglycerides", "hdl", "glucose", "cardiovascular", "combined"]
    },
    {
        "id": "pattern_002",
        "category": "Combined Analysis",
        "title": "Hypothyroidism Causing Dyslipidemia — Connection Pattern",
        "content": (
            "Hypothyroidism (elevated TSH) directly causes secondary dyslipidemia: "
            "Mechanism: thyroid hormone upregulates hepatic LDL receptors — hypothyroidism reduces LDL clearance, "
            "leading to elevated LDL and total cholesterol. Also elevates TG by reducing lipoprotein lipase activity. "
            "Clinical rule: ALWAYS check thyroid function before initiating statin therapy for new-onset dyslipidemia. "
            "Treating hypothyroidism with levothyroxine may normalize lipids without needing statins. "
            "Expected lipid improvement with adequate thyroid replacement: LDL reduction of 10-30%. "
            "Also consider: hypothyroidism causes elevated CK (pseudo-myopathy), which can be confused with statin side effects. "
            "Other secondary causes of dyslipidemia to exclude: diabetes, nephrotic syndrome, obstructive liver disease, "
            "medications (thiazides, beta-blockers, corticosteroids)."
        ),
        "source": "ATA Guidelines; AHA/ACC Cholesterol Guidelines; Harrison's Ch. 375, 400",
        "tags": ["hypothyroidism", "dyslipidemia", "ldl", "tsh", "statin", "combined"]
    },
    {
        "id": "pattern_003",
        "category": "Combined Analysis",
        "title": "Iron Deficiency with B12 Deficiency — Combined Deficiency Pattern",
        "content": (
            "Concurrent iron and B12 deficiency is common in Indian vegetarian population. "
            "Diagnostic challenge: MCV may be falsely normal because iron deficiency (microcytic) and B12 deficiency (macrocytic) "
            "cancel each other out. RDW will be HIGH (mixed population of small and large RBCs). "
            "Clue: normal MCV + high RDW + low Hb → suspect combined deficiency. "
            "Confirm with: ferritin (<30), B12 (<211), peripheral smear showing dimorphic picture. "
            "Treatment must address BOTH deficiencies simultaneously. "
            "Start B12 replacement first or concurrently — if only iron is given, the masked megaloblastic anaemia "
            "may worsen due to increased erythropoiesis consuming remaining B12 stores. "
            "Common in: vegetarians, pregnant women, elderly, post-bariatric surgery, chronic H. pylori infection."
        ),
        "source": "BSH Guidelines; Harrison's Principles Ch. 93; ICMR-NIN Dietary Guidelines",
        "tags": ["iron deficiency", "b12 deficiency", "combined", "vegetarian", "dimorphic", "anaemia"]
    },
    {
        "id": "pattern_004",
        "category": "Combined Analysis",
        "title": "NAFLD Pattern — Liver Enzymes with Metabolic Risk Factors",
        "content": (
            "Non-Alcoholic Fatty Liver Disease (NAFLD) is suggested by: mildly elevated ALT (1-3x ULN), "
            "often ALT > AST, elevated GGT, with concurrent metabolic risk factors (obesity, diabetes, dyslipidemia). "
            "NAFLD is the most common cause of incidentally discovered elevated liver enzymes globally. "
            "Prevalence in India: 30-40% in urban populations per meta-analysis. "
            "Spectrum: Simple steatosis → NASH (steatohepatitis) → Fibrosis → Cirrhosis → Hepatocellular carcinoma. "
            "Key workup: abdominal ultrasound (fatty liver), exclude other causes (viral hepatitis, alcohol, autoimmune, "
            "Wilson disease, hemochromatosis), FIB-4 score for fibrosis assessment. "
            "No approved pharmacotherapy — management is lifestyle: weight loss 7-10% (proven to reverse NASH), "
            "exercise, reduce fructose/refined carbs, avoid alcohol completely. "
            "Pioglitazone and Vitamin E may benefit NASH without diabetes. GLP-1 agonists show promise."
        ),
        "source": "AASLD Practice Guidance on NAFLD 2023; INASL Guidelines; Harrison's Ch. 336",
        "tags": ["nafld", "fatty liver", "alt", "ast", "ggt", "metabolic", "liver", "combined"]
    },
    {
        "id": "pattern_005",
        "category": "Combined Analysis",
        "title": "Hashimoto Thyroiditis with Vitamin D Deficiency — Autoimmune Connection",
        "content": (
            "Vitamin D deficiency is significantly more prevalent in patients with Hashimoto thyroiditis. "
            "Multiple studies show inverse correlation between Vitamin D levels and Anti-TPO titre. "
            "Proposed mechanism: Vitamin D modulates immune function — deficiency promotes Th1-mediated autoimmunity. "
            "Supplementation evidence: some RCTs show Vitamin D supplementation reduces Anti-TPO levels in Hashimoto's patients, "
            "though not all studies agree. Target level ≥40 ng/mL recommended. "
            "Clinical approach: if Hashimoto's + Vitamin D deficient, aggressive Vitamin D repletion is warranted "
            "both for bone health (hypothyroidism + D deficiency compounds osteoporosis risk) and potential immune modulation. "
            "Also screen for: B12 deficiency (autoimmune clustering — pernicious anaemia is more common in Hashimoto's patients), "
            "celiac disease (associated autoimmune condition)."
        ),
        "source": "Endocrine Society Guidelines; Thyroid Journal meta-analysis; Harrison's Ch. 375",
        "tags": ["hashimoto", "vitamin d", "autoimmune", "anti-tpo", "thyroid", "combined"]
    },
]


def get_all_chunks() -> list[dict]:
    """Return all knowledge chunks."""
    return MEDICAL_KNOWLEDGE


def get_chunks_by_category(category: str) -> list[dict]:
    """Return chunks for a specific category."""
    return [c for c in MEDICAL_KNOWLEDGE if c["category"].lower() == category.lower()]


def get_chunks_by_tags(tags: list[str]) -> list[dict]:
    """Return chunks matching any of the given tags."""
    tags_lower = {t.lower() for t in tags}
    return [c for c in MEDICAL_KNOWLEDGE if tags_lower & {t.lower() for t in c["tags"]}]

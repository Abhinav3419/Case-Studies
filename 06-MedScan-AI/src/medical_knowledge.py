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

    # ================================================================
    # INFECTIOUS DISEASE MARKERS
    # ================================================================
    {
        "id": "infect_001",
        "category": "Infectious Disease",
        "title": "CRP and Procalcitonin — Bacterial vs Viral Differentiation",
        "content": (
            "CRP (C-Reactive Protein) is a non-specific acute-phase reactant produced by the liver. "
            "CRP >10 mg/L suggests significant inflammation; >100 mg/L strongly suggests bacterial infection or severe inflammatory condition. "
            "Procalcitonin (PCT) is more specific for bacterial infection: PCT <0.05 ng/mL = normal, "
            "0.05-0.5 = possible local bacterial infection, 0.5-2.0 = likely bacterial sepsis, "
            "2.0-10.0 = severe sepsis, >10.0 = septic shock with high mortality risk. "
            "Key clinical utility: PCT helps distinguish bacterial from viral infections — PCT remains low in viral infections "
            "while CRP rises in both. PCT-guided antibiotic stewardship reduces antibiotic duration by 2-3 days without adverse outcomes. "
            "In COVID-19: CRP >100 mg/L predicts severe disease; PCT >0.5 suggests bacterial superinfection. "
            "Serial CRP monitoring (every 24-48 hrs) tracks treatment response — halving of CRP suggests effective therapy."
        ),
        "source": "Surviving Sepsis Campaign 2021; Harrison's Principles Ch. 297; Lancet ID meta-analysis on PCT",
        "tags": ["crp", "procalcitonin", "bacterial", "viral", "sepsis", "infection", "covid"]
    },
    {
        "id": "infect_002",
        "category": "Infectious Disease",
        "title": "HIV Monitoring — CD4 Count and Viral Load Interpretation",
        "content": (
            "CD4 count is the primary marker for immune status in HIV: "
            "CD4 >500 cells/µL = adequate immune function (Stage 1). "
            "CD4 350-499 = mild immunosuppression (Stage 2). "
            "CD4 200-349 = advanced immunosuppression, OI prophylaxis needed (Stage 3). "
            "CD4 <200 = AIDS-defining, severe risk of opportunistic infections (PCP, Toxoplasma, Cryptococcus). "
            "WHO and NACO (India) now recommend immediate ART initiation regardless of CD4 count ('Test and Treat'). "
            "Viral load (HIV RNA) is the primary marker for treatment efficacy: "
            "Undetectable (<20 copies/mL) = treatment success and U=U (undetectable = untransmittable). "
            "Viral load >200 copies/mL on two occasions = virological failure — check adherence, consider resistance testing. "
            "India has the third-largest HIV population globally (~2.4 million per NACO 2023). "
            "CD4 recovery: expect ~100 cells/µL increase per year on effective ART."
        ),
        "source": "WHO Consolidated HIV Guidelines 2024; NACO India ART Guidelines; Harrison's Ch. 197",
        "tags": ["hiv", "cd4", "viral load", "aids", "art", "immunodeficiency"]
    },
    {
        "id": "infect_003",
        "category": "Infectious Disease",
        "title": "Hepatitis B Panel — Serological Interpretation",
        "content": (
            "Hepatitis B serological patterns: "
            "HBsAg positive + Anti-HBc IgM positive = acute HBV infection. "
            "HBsAg positive + Anti-HBc IgG positive + HBeAg positive = chronic active HBV (high infectivity). "
            "HBsAg positive + Anti-HBc IgG positive + Anti-HBe positive = chronic inactive carrier (low infectivity). "
            "HBsAg negative + Anti-HBs positive + Anti-HBc positive = resolved past infection (immune). "
            "HBsAg negative + Anti-HBs positive + Anti-HBc negative = vaccinated (immune). "
            "All negative = susceptible, needs vaccination. "
            "India is hyperendemic for HBV with ~40 million chronic carriers per INASL. "
            "HBV DNA viral load determines treatment need: treat if >2000 IU/mL with elevated ALT or significant fibrosis. "
            "First-line treatment: Tenofovir or Entecavir (long-term, possibly lifelong). "
            "All HBsAg-positive patients need hepatocellular carcinoma screening (AFP + ultrasound every 6 months)."
        ),
        "source": "AASLD HBV Guidelines 2024; INASL Guidelines; Harrison's Ch. 332",
        "tags": ["hepatitis b", "hbsag", "hbv", "liver", "vaccination", "infection"]
    },
    {
        "id": "infect_004",
        "category": "Infectious Disease",
        "title": "Dengue Diagnostics — NS1, IgM, IgG Interpretation",
        "content": (
            "Dengue diagnostic timeline: "
            "Day 1-5 of fever: NS1 antigen positive (sensitivity 90%+ in primary infection, lower in secondary). "
            "Day 5+: NS1 declines, IgM becomes positive (persists 2-3 months). "
            "IgG: rises in secondary infection (appears by day 2-3), in primary infection appears after 2 weeks. "
            "High IgG/IgM ratio (>1.4) suggests secondary dengue — higher risk of Dengue Hemorrhagic Fever (DHF). "
            "Warning signs for severe dengue: platelet count <100,000/µL, haematocrit rise >20%, "
            "abdominal pain, persistent vomiting, mucosal bleeding, lethargy. "
            "India reports 100,000+ dengue cases annually (vastly underreported). "
            "No specific antiviral — management is supportive: IV fluids, platelet monitoring every 12-24 hrs, "
            "avoid NSAIDs and aspirin (bleeding risk). Platelet transfusion only if <10,000 or active bleeding."
        ),
        "source": "WHO Dengue Guidelines 2009 (updated 2024); NVBDCP India Guidelines; Harrison's Ch. 204",
        "tags": ["dengue", "ns1", "igm", "platelet", "hemorrhagic fever", "infection"]
    },
    {
        "id": "infect_005",
        "category": "Infectious Disease",
        "title": "Tuberculosis Markers — ADA, Quantiferon, and Diagnosis",
        "content": (
            "TB diagnosis in India (highest burden globally — ~2.8 million cases/year per RNTCP): "
            "Quantiferon-TB Gold (IGRA): positive ≥0.35 IU/mL indicates TB infection (latent or active). "
            "Cannot distinguish latent from active TB — clinical correlation required. "
            "ADA (Adenosine Deaminase): Pleural ADA >40 U/L = 92% sensitivity for tuberculous pleural effusion. "
            "CSF ADA >10 U/L suggests TB meningitis. Peritoneal ADA >39 U/L suggests abdominal TB. "
            "Sputum GeneXpert MTB/RIF: gold standard for pulmonary TB — detects MTB and rifampicin resistance in 2 hours. "
            "AFB smear microscopy: low sensitivity (45-80%) but widely available. "
            "TB blood markers: elevated ESR, lymphocytosis, anaemia of chronic disease, low albumin. "
            "RNTCP (now NTEP) regimen: HRZE for 2 months intensive + HR for 4 months continuation. "
            "Drug-resistant TB needs MDR-TB regimen with bedaquiline-based shorter regimen."
        ),
        "source": "NTEP India Guidelines 2024; WHO TB Guidelines; Harrison's Ch. 173",
        "tags": ["tuberculosis", "tb", "ada", "quantiferon", "igra", "genexpert", "infection"]
    },
    {
        "id": "infect_006",
        "category": "Infectious Disease",
        "title": "COVID-19 Severity Markers — D-dimer, Ferritin, IL-6, LDH",
        "content": (
            "COVID-19 laboratory predictors of severity: "
            "D-dimer >1000 ng/mL: 18x higher mortality risk — indicates coagulopathy and microthrombi formation. "
            "Ferritin >500 ng/mL: suggests hyperinflammation/cytokine storm (macrophage activation). "
            "IL-6 >100 pg/mL: correlates with cytokine storm severity — tocilizumab indicated in this range. "
            "LDH >400 U/L: indicates tissue damage and correlates with lung involvement severity. "
            "CRP >100 mg/L: predicts ICU admission and mechanical ventilation need. "
            "Lymphopenia (<1000/µL): hallmark of severe COVID-19 — correlates with T-cell exhaustion. "
            "NLR (Neutrophil-Lymphocyte Ratio) >5: independent predictor of critical illness. "
            "Procalcitonin >0.5 ng/mL in COVID-19: suggests bacterial co-infection — add antibiotics. "
            "These markers guide triaging: mild (normal labs) → moderate (1-2 elevated) → severe (multiple elevated) → critical (all markedly elevated with organ dysfunction)."
        ),
        "source": "WHO COVID-19 Clinical Management Guide 2023; NIH COVID-19 Treatment Guidelines; Lancet meta-analysis",
        "tags": ["covid", "d-dimer", "ferritin", "il-6", "ldh", "cytokine storm", "coagulopathy"]
    },
    {
        "id": "infect_007",
        "category": "Infectious Disease",
        "title": "Malaria and Typhoid — Endemic Disease Markers in India",
        "content": (
            "Malaria diagnosis: Peripheral smear (gold standard) identifies species and parasitaemia %. "
            "Rapid Diagnostic Test (RDT): detects P. falciparum HRP-2 and pan-Plasmodium pLDH antigens. "
            "Parasitaemia >5% = severe malaria (per WHO) — requires IV artesunate. "
            "Lab features of severe malaria: anaemia, thrombocytopenia, hypoglycaemia, elevated bilirubin, elevated creatinine. "
            "Typhoid (Salmonella typhi): Blood culture is gold standard (positive in 60-80% week 1). "
            "Widal test: O titre ≥1:160 and H titre ≥1:160 suggestive in endemic areas (India). "
            "Single Widal is unreliable — rising titres (4-fold increase in paired samples 1 week apart) are more diagnostic. "
            "Typhoid complications: intestinal perforation (week 3), GI bleeding, encephalopathy. "
            "Treatment: Azithromycin or Ceftriaxone (resistance to fluoroquinolones increasing in India)."
        ),
        "source": "WHO Malaria Guidelines 2023; Indian NVBDCP; Harrison's Ch. 219, 164",
        "tags": ["malaria", "typhoid", "widal", "parasitaemia", "endemic", "infection"]
    },

    # ================================================================
    # TUMOUR MARKERS
    # ================================================================
    {
        "id": "tumour_001",
        "category": "Tumour Markers",
        "title": "PSA — Prostate Cancer Screening and Monitoring",
        "content": (
            "PSA (Prostate-Specific Antigen) interpretation: "
            "PSA <4.0 ng/mL: normal (but 15% of cancers occur with PSA <4). "
            "PSA 4-10 ng/mL: grey zone — 25% chance of cancer; calculate free PSA ratio. "
            "Free PSA/Total PSA <10%: high cancer suspicion. >25%: likely BPH (benign). "
            "PSA >10 ng/mL: 50%+ probability of prostate cancer — biopsy strongly recommended. "
            "PSA >20 ng/mL: high probability of cancer with possible extraprostatic extension. "
            "PSA velocity >0.75 ng/mL/year: suspicious even if PSA is in normal range. "
            "Non-cancer causes of elevated PSA: BPH (most common), prostatitis, recent ejaculation, "
            "urinary retention, cycling, DRE examination. "
            "PSA is organ-specific (prostate) but NOT cancer-specific. "
            "USPSTF recommends shared decision-making for PSA screening in men 55-69 years. "
            "In post-treatment monitoring: PSA should be undetectable after radical prostatectomy; "
            "rising PSA indicates biochemical recurrence."
        ),
        "source": "NCCN Prostate Cancer Guidelines 2024; AUA/ASTRO Guidelines; Harrison's Ch. 83",
        "tags": ["psa", "prostate", "cancer", "bph", "screening", "tumour marker"]
    },
    {
        "id": "tumour_002",
        "category": "Tumour Markers",
        "title": "CA-125, CEA, AFP, CA 19-9 — Major Tumour Markers Panel",
        "content": (
            "CA-125: Primary marker for ovarian cancer. >35 U/mL is elevated. "
            "Non-malignant causes: endometriosis, PID, cirrhosis, heart failure, pregnancy, menstruation. "
            "Most useful for monitoring treatment response and recurrence in known ovarian cancer. "
            "CEA (Carcinoembryonic Antigen): Elevated in colorectal, lung, breast, pancreatic cancers. "
            "Normal <5 ng/mL (higher in smokers). Primary role: monitoring colorectal cancer recurrence post-surgery. "
            "NOT recommended for primary cancer screening due to low specificity. "
            "AFP (Alpha-Fetoprotein): Elevated in hepatocellular carcinoma (HCC) and testicular germ cell tumours. "
            "AFP >400 ng/mL in cirrhotic patient: highly suspicious for HCC. "
            "In testicular cancer: AFP elevated in yolk sac tumours and mixed germ cell tumours (NOT pure seminoma). "
            "CA 19-9: Pancreatic and biliary cancer marker. >37 U/mL is elevated. "
            "70-90% sensitive for pancreatic adenocarcinoma. Also elevated in cholestasis, pancreatitis, cholangitis. "
            "Not expressed in Lewis antigen-negative individuals (5-10% of population — false negatives). "
            "All tumour markers have LIMITED value for primary diagnosis — they are best for MONITORING known cancers."
        ),
        "source": "NCCN Guidelines (various); ASCO Tumour Marker Guidelines; Harrison's Ch. 73",
        "tags": ["ca-125", "cea", "afp", "ca19-9", "ovarian", "colorectal", "liver", "pancreatic", "tumour marker"]
    },
    {
        "id": "tumour_003",
        "category": "Tumour Markers",
        "title": "LDH and SPEP — Lymphoma and Myeloma Screening",
        "content": (
            "LDH (Lactate Dehydrogenase): Non-specific tissue damage marker. "
            "Markedly elevated LDH with lymphadenopathy/B symptoms suggests lymphoma (especially DLBCL, Burkitt). "
            "LDH is a component of the International Prognostic Index (IPI) for aggressive lymphoma. "
            "Other causes of elevated LDH: haemolysis, MI, pulmonary embolism, liver disease, rhabdomyolysis, any malignancy. "
            "SPEP (Serum Protein Electrophoresis): Detects monoclonal bands (M-protein/M-spike). "
            "Presence of M-spike suggests: Multiple Myeloma, Waldenstrom macroglobulinemia, "
            "MGUS (Monoclonal Gammopathy of Undetermined Significance), Amyloidosis. "
            "If M-spike detected: quantify (>3 g/dL = likely myeloma), check serum free light chains, "
            "urine for Bence-Jones protein, skeletal survey, bone marrow biopsy. "
            "MGUS: M-protein <3 g/dL + bone marrow plasma cells <10% + no end-organ damage (CRAB criteria). "
            "MGUS progresses to myeloma at ~1% per year — requires long-term monitoring."
        ),
        "source": "IMWG Diagnostic Criteria 2014; NCCN Myeloma Guidelines; Harrison's Ch. 107",
        "tags": ["ldh", "spep", "lymphoma", "myeloma", "m-spike", "mgus", "tumour marker"]
    },

    # ================================================================
    # GENETIC / HAEMATOLOGICAL MARKERS
    # ================================================================
    {
        "id": "genetic_001",
        "category": "Genetic / Haematology",
        "title": "Haemoglobin Electrophoresis — Sickle Cell and Thalassemia Screening",
        "content": (
            "Haemoglobin electrophoresis / HPLC separates Hb variants: "
            "Normal adult pattern: HbA 95-98%, HbA2 2.0-3.3%, HbF <2%. "
            "Beta-Thalassemia Trait: HbA2 elevated (3.5-8%), HbF may be slightly elevated, mild microcytic anaemia. "
            "Most common inherited anaemia in India — carrier rate 3-17% depending on community. "
            "Beta-Thalassemia Major: HbF 60-90%, HbA absent or very low, severe anaemia requiring transfusions. "
            "Sickle Cell Trait: HbS 20-40%, HbA 55-75%, usually asymptomatic. "
            "Sickle Cell Disease: HbS >50% (usually 80-95%), HbF variable, severe haemolytic anaemia + vaso-occlusive crises. "
            "India's tribal populations (central/eastern India) have sickle cell carrier rates of 10-35%. "
            "Government of India launched National Sickle Cell Anaemia Elimination Mission (2023) for screening. "
            "Genetic counselling essential: if both partners are carriers of same haemoglobinopathy, "
            "25% chance of affected child. Pre-marital and antenatal screening recommended."
        ),
        "source": "ICMR Haemoglobinopathy Guidelines; WHO Sickle Cell Guidelines; Harrison's Ch. 94",
        "tags": ["haemoglobin electrophoresis", "sickle cell", "thalassemia", "hba2", "hbf", "hbs", "genetic"]
    },
    {
        "id": "genetic_002",
        "category": "Genetic / Haematology",
        "title": "G6PD Deficiency — Drug and Food-Induced Haemolysis",
        "content": (
            "G6PD deficiency is the most common enzyme deficiency worldwide (~400 million affected). "
            "X-linked recessive — males predominantly affected; female carriers may have partial deficiency. "
            "G6PD protects red blood cells from oxidative stress. Deficiency causes episodic haemolytic anaemia "
            "triggered by oxidant drugs, infections, or fava beans. "
            "Drugs to AVOID: primaquine (anti-malarial), dapsone, rasburicase, nitrofurantoin, "
            "methylene blue, high-dose aspirin, sulfonamides. "
            "Clinical presentation: acute haemolysis 24-72 hrs after trigger — dark urine, jaundice, anaemia, "
            "reticulocytosis, elevated bilirubin, elevated LDH, low haptoglobin. "
            "Diagnosis: G6PD quantitative assay — but may be falsely normal during acute haemolysis "
            "(young reticulocytes have higher G6PD). Recheck 2-3 months after episode. "
            "In India, prevalence varies 3-15% across different communities. "
            "Neonatal jaundice is a major risk in G6PD-deficient newborns — can cause kernicterus if untreated."
        ),
        "source": "WHO G6PD Guidelines; British Journal of Haematology; Harrison's Ch. 94",
        "tags": ["g6pd", "haemolysis", "enzyme deficiency", "drug safety", "genetic"]
    },

    # ================================================================
    # COAGULATION PATTERNS
    # ================================================================
    {
        "id": "coag_001",
        "category": "Coagulation",
        "title": "Coagulation Panel — PT/INR, aPTT, Fibrinogen Interpretation",
        "content": (
            "Coagulation screening panel interpretation: "
            "Isolated prolonged PT/INR (normal aPTT): Factor VII deficiency, early warfarin effect, "
            "early liver disease, mild Vitamin K deficiency. "
            "Isolated prolonged aPTT (normal PT): Haemophilia A (Factor VIII) or B (Factor IX), "
            "von Willebrand disease, heparin therapy, lupus anticoagulant (paradoxically thrombotic). "
            "Both PT and aPTT prolonged: DIC, severe liver disease, supratherapeutic anticoagulation, "
            "massive transfusion, common pathway deficiency (Factor X, V, II, fibrinogen). "
            "DIC pattern: prolonged PT + aPTT + low fibrinogen + elevated D-dimer + low platelets + "
            "schistocytes on smear. DIC is always secondary — treat the underlying cause (sepsis, malignancy, obstetric emergency). "
            "D-dimer: sensitive but non-specific for thrombosis. <500 ng/mL effectively rules out DVT/PE "
            "in low-risk patients (high negative predictive value). "
            "INR therapeutic ranges: 2.0-3.0 for DVT/PE/AF; 2.5-3.5 for mechanical heart valves. "
            "Fibrinogen <100 mg/dL = critical bleeding risk — consider cryoprecipitate transfusion."
        ),
        "source": "British Society for Haematology Coagulation Guidelines; ISTH DIC Criteria; Harrison's Ch. 78",
        "tags": ["coagulation", "pt", "inr", "aptt", "fibrinogen", "d-dimer", "dic", "haemophilia", "warfarin"]
    },

    # ================================================================
    # COMBINED PATTERNS (NEW — INFECTIOUS + TUMOUR)
    # ================================================================
    {
        "id": "pattern_006",
        "category": "Combined Analysis",
        "title": "Sepsis Screening — CRP + Procalcitonin + WBC + Lactate Pattern",
        "content": (
            "Sepsis pattern recognition from lab panel: "
            "WBC >12,000 or <4,000 + CRP >100 mg/L + Procalcitonin >2 ng/mL = high probability of bacterial sepsis. "
            "Add elevated lactate (>2 mmol/L) = septic shock criteria per Sepsis-3 definition. "
            "SOFA score components from labs: platelets, bilirubin, creatinine assess organ dysfunction. "
            "qSOFA (bedside): altered mentation + SBP <100 + RR >22 — any 2 of 3 = high mortality risk. "
            "Sepsis bundle (hour-1): blood cultures before antibiotics, broad-spectrum antibiotics, "
            "IV fluids 30 mL/kg, measure lactate, repeat lactate if >2. "
            "In Indian ICUs: sepsis mortality remains 40-60% — early recognition from lab patterns is critical. "
            "A lab panel showing elevated WBC + CRP + PCT together has >90% positive predictive value for bacterial sepsis."
        ),
        "source": "Surviving Sepsis Campaign 2021; Sepsis-3 Consensus Definition; Harrison's Ch. 297",
        "tags": ["sepsis", "crp", "procalcitonin", "wbc", "lactate", "combined"]
    },
    {
        "id": "pattern_007",
        "category": "Combined Analysis",
        "title": "Tumour Marker Patterns — When to Suspect Malignancy",
        "content": (
            "Combined tumour marker patterns that raise suspicion: "
            "Elevated PSA + elevated ALP + bone pain in elderly male → prostate cancer with bone metastases. "
            "Elevated AFP + elevated liver enzymes + known cirrhosis → hepatocellular carcinoma. "
            "Elevated CA 19-9 + obstructive jaundice + weight loss → pancreatic head carcinoma. "
            "Elevated LDH + lymphadenopathy + B-symptoms (fever, night sweats, weight loss) → lymphoma. "
            "M-spike on SPEP + bone pain + anaemia + hypercalcaemia + elevated creatinine (CRAB) → multiple myeloma. "
            "Elevated CEA post-surgery (was normalized) → colorectal cancer recurrence. "
            "CRITICAL: No tumour marker alone diagnoses cancer. All elevated markers require tissue diagnosis (biopsy). "
            "Tumour markers are most valuable for: monitoring treatment response, detecting recurrence, and guiding prognosis."
        ),
        "source": "NCCN Guidelines; ASCO Tumour Marker Guidelines; Harrison's Ch. 73",
        "tags": ["psa", "afp", "ca19-9", "ldh", "cea", "spep", "malignancy", "combined"]
    },
    {
        "id": "pattern_008",
        "category": "Combined Analysis",
        "title": "DIC Pattern — Coagulopathy with Multi-Organ Involvement",
        "content": (
            "Disseminated Intravascular Coagulation (DIC) laboratory pattern: "
            "Prolonged PT + prolonged aPTT + low fibrinogen (<150 mg/dL) + elevated D-dimer (>4x normal) + "
            "thrombocytopenia (<100,000) + schistocytes on peripheral smear. "
            "ISTH DIC scoring system: platelets + D-dimer + fibrinogen + PT prolongation = overt DIC if score ≥5. "
            "Common triggers: sepsis (most common), major trauma, obstetric emergencies (placental abruption, "
            "amniotic fluid embolism), acute promyelocytic leukaemia (APL), snake envenomation (common in India). "
            "DIC is always SECONDARY — the primary disease must be identified and treated urgently. "
            "Management: treat underlying cause, transfuse blood products only if active bleeding or procedure needed "
            "(platelets if <50,000, cryoprecipitate if fibrinogen <100, FFP if PT/aPTT prolonged with bleeding). "
            "Do NOT give heparin in acute DIC with bleeding — only consider in chronic DIC with thrombosis predominance."
        ),
        "source": "ISTH DIC Guidelines; British Society for Haematology; Harrison's Ch. 78",
        "tags": ["dic", "coagulopathy", "d-dimer", "fibrinogen", "platelets", "sepsis", "combined"]
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

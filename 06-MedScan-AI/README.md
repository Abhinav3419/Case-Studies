# MedScan AI — Intelligent Clinical Report Analyzer

**LLM-powered system that parses clinical lab report PDFs, extracts biomarkers, validates against medical references, and generates cited differential analysis using RAG.**

*Built as a portfolio-grade case study demonstrating LLM orchestration, RAG architecture, PDF parsing, and domain-specific AI for healthcare.*

---

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-In_Progress_(Day_1_Complete)-00C853?style=flat-square)
![Tests](https://img.shields.io/badge/Tests-4/4_Passing-00C853?style=flat-square)
![Biomarkers](https://img.shields.io/badge/Reference_DB-56_Biomarkers_|_209_Aliases-1a5276?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## What Does It Do?

Upload a blood test / pathology PDF → the system:

1. **Extracts** structured biomarker data from any Indian lab format (Thyrocare, Dr. Lal PathLabs, SRL, Metropolis, etc.)
2. **Validates** each value against clinically standardized reference ranges (Harrison's, WHO, ICMR, Tietz)
3. **Flags** abnormal, critical, and borderline values with deviation percentages
4. **Classifies** into interpretation bands (e.g., FBS → "prediabetes", Vitamin D → "deficient", LDL → "high")
5. *(Coming)* **Analyzes** using LLM + RAG over medical literature to explain every abnormality with citable sources
6. *(Coming)* **Generates** a comprehensive clinical interpretation report with differential analysis

---

## Day 1 Results — Extraction Engine

### Extraction Accuracy

| Metric | Report 1 (Full Panel) | Report 2 (Thyroid) |
|--------|----------------------|-------------------|
| Tests Extracted | 52 | 7 |
| Abnormal Detection | **12/12 (100%)** | **4/4 (100%)** |
| Patient Info Parsed | Name, Age, Sex, ID, Lab, Dates ✓ | Name, Age, Sex, ID, Lab ✓ |
| Extraction Method | Table-based (primary) | Table-based (primary) |
| Critical Values Flagged | 0 | 0 |

### Sample Output — Abnormal Values Detected

```
🔴 ABNORMAL VALUES (28):
   🔻 Haemoglobin (Hb)                  12.8 g/dL    LOW          1.5%       13.0 - 17.0
   🔺 Total WBC Count                   11200 cells/  HIGH         12.0%      4000 - 10000
   🔺 ESR (Westergren)                  22 mm/hr      HIGH         46.7%      0 - 15
   🔺 Total Cholesterol                 238 mg/dL     HIGH         19.0%      0 - 200 [borderline_high]
   🔺 Triglycerides                     195 mg/dL     HIGH         30.0%      0 - 150 [borderline_high]
   🔺 LDL Cholesterol (Calculated)      161 mg/dL     HIGH         61.0%      0 - 100 [high]
   🔺 SGPT (ALT)                        68 U/L        HIGH         65.9%      0 - 41
   🔺 TSH (Ultrasensitive)              6.82 µIU/mL   HIGH         38.1%      0.35 - 4.94
   🔺 HbA1c                             6.1 %         HIGH         7.0%       0 - 5.7 [prediabetes]
   🔻 Vitamin D (25-OH)                 14.2 ng/mL    LOW          52.7%      30 - 100 [deficient]
   🔻 Vitamin B12                       185 pg/mL     LOW          12.3%      211 - 946
   🔻 Ferritin                          18 ng/mL      LOW          10.0%      20 - 250
```

### Clinical Reference Database

| Category | Biomarkers Covered | Key Tests |
|----------|-------------------|-----------|
| CBC | 16 | Hb, RBC, WBC, Platelets, ESR, Differentials, MCV/MCH/MCHC |
| Lipid Profile | 5 | Total Cholesterol, LDL, HDL, Triglycerides, VLDL |
| Liver Function | 11 | AST, ALT, ALP, Bilirubin, GGT, Albumin, Proteins |
| Thyroid | 6 | TSH, Free T3/T4, Total T3/T4, Anti-TPO |
| Kidney Function | 11 | Creatinine, BUN, Uric Acid, eGFR, Electrolytes |
| Blood Glucose | 2 | Fasting Blood Sugar, HbA1c |
| Vitamins & Iron | 7 | Vitamin D, B12, Iron, Ferritin, TIBC, Folate |
| **Total** | **56 biomarkers** | **209 aliases for fuzzy matching** |

All reference ranges are gender-specific where applicable, with critical thresholds and multi-band interpretation (e.g., FBS: normal → prediabetes → diabetes).

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        MedScan AI Pipeline                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    ┌──────────────┐    ┌────────────────────┐     │
│  │ PDF Input│───►│ pdfplumber   │───►│ Table Extraction   │     │
│  │ (Any Lab)│    │ Text + Table │    │ + Regex Fallback   │     │
│  └──────────┘    └──────────────┘    └────────┬───────────┘     │
│                                               │                 │
│                                               ▼                 │
│  ┌──────────────────┐    ┌────────────────────────────────┐     │
│  │ Patient Info     │    │ Biomarker Matching Engine      │     │
│  │ Parser (Regex)   │    │ 56 canonical + 209 aliases     │     │
│  └──────────────────┘    │ Exact → Partial → Word-level   │     │
│                          └────────────────┬───────────────┘     │
│                                           │                     │
│                                           ▼                     │
│  ┌──────────────────────────────────────────────────────┐       │
│  │ Clinical Validation Engine                           │       │
│  │ • Gender-specific reference ranges                   │       │
│  │ • Flag: NORMAL / HIGH / LOW / CRITICAL               │       │
│  │ • Deviation % calculation                            │       │
│  │ • Interpretation bands (prediabetes, deficient, etc.)│       │
│  └──────────────────────────┬───────────────────────────┘       │
│                             │                                   │
│                             ▼                                   │
│  ┌────────────┐    ┌──────────────┐    ┌──────────────────┐     │
│  │ JSON Output│    │ Summary View │    │ (Day 2+)         │     │
│  │ Structured │    │ Color-coded  │    │ RAG Analysis     │     │
│  └────────────┘    └──────────────┘    │ LLM Reasoning    │     │
│                                        │ Cited References │     │
│                                        └──────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
medscan-ai/
├── src/
│   ├── __init__.py
│   ├── pdf_extractor.py          # Core extraction engine (table + regex + validation)
│   └── clinical_references.py    # 56-biomarker reference DB with 209 aliases
│
├── tests/
│   ├── generate_sample_reports.py # Generates realistic Indian lab report PDFs
│   └── test_extraction.py         # 4-suite test harness (4/4 passing)
│
├── data/
│   ├── sample_reports/            # Generated test PDFs
│   └── processed/                 # Extraction output JSONs
│
├── config/
│   └── settings.json              # Project configuration
│
├── docs/                          # (Methodology documentation)
├── requirements.txt
└── README.md
```

---

## Quick Start

```bash
git clone https://github.com/Abhinav3419/medscan-ai.git
cd medscan-ai
pip install -r requirements.txt

# Generate sample lab reports for testing
python tests/generate_sample_reports.py

# Run the full test suite
python tests/test_extraction.py

# Extract a specific report
python -m src.pdf_extractor data/sample_reports/sample_report_01_cbc_lipid.pdf
```

---

## Extraction Engine — How It Works

### 1. PDF Parsing (Dual Strategy)

The engine uses **pdfplumber** for layout-aware extraction. Tables are the primary extraction target (structured lab reports are inherently tabular). A regex-based fallback activates when table extraction yields fewer than 3 biomarkers — this handles non-standard formats, text-heavy reports, or PDFs with broken table structures.

### 2. Biomarker Matching (3-Tier Fuzzy Match)

Each extracted test name is matched against the reference database using a cascading strategy:

- **Tier 1 — Exact match**: Direct lookup on canonical name or any registered alias
- **Tier 2 — Partial match**: Longest substring match (requires ≥3 characters) including parenthetical content (catches "SGOT (AST)" → `sgot_ast`)
- **Tier 3 — Word-level match**: Set intersection of words with strict thresholds to prevent false positives

### 3. Clinical Validation

For every matched biomarker:

- Reference range is selected based on **patient gender** (male/female/default)
- Value is classified as NORMAL / HIGH / LOW / CRITICAL_HIGH / CRITICAL_LOW
- **Deviation percentage** is computed: how far the value falls outside the reference range
- **Interpretation bands** are assigned where applicable (e.g., HbA1c 6.1% → "prediabetes")

### 4. Patient Info Extraction

Multi-pattern regex extracts: name, age, sex, patient ID, sample ID, referring doctor, collection date, report date, sample type, and lab name. Handles diverse Indian lab header formats.

---

## Roadmap

| Day | Milestone | Status |
|-----|-----------|--------|
| **1** | PDF Parsing + Biomarker Extraction Engine | ✅ Complete |
| **2** | Medical Knowledge Base + RAG Pipeline (ChromaDB + embeddings) | 🔲 Next |
| **3** | LLM Analysis Engine + Clinical Reasoning Chain | 🔲 Planned |
| **4** | MCP Integration + Streamlit UI | 🔲 Planned |
| **5** | Validation, Edge Cases, Documentation + GitHub Polish | 🔲 Planned |

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| PDF Parsing | pdfplumber, pypdf |
| Reference Database | Custom Python (56 biomarkers, Harrison's/WHO/ICMR/Tietz) |
| Sample Generation | ReportLab |
| RAG  | LangChain, ChromaDB, sentence-transformers |
| LLM  | Claude API / OpenAI / Ollama (local) |
| UI  | Streamlit |
| Testing | Custom test harness with assertion-based validation |

---

## Reference Sources

1. Harrison's Principles of Internal Medicine, 21st Edition
2. Tietz Clinical Guide to Laboratory Tests, 6th Edition
3. WHO Clinical Guidelines for Laboratory Diagnostics
4. ICMR (Indian Council of Medical Research) — Standard Reference Ranges
5. Drik Panchang — (for cultural calendar features in related project)

---

## Disclaimer

**This tool is for educational and informational purposes only.** It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for interpretation of clinical test results.

---

## Author

**Abhinav Pandey**
M.Tech (Applied Mechanics), MNNIT Allahabad · B.Tech (E&I), Ghaziabad

[Email](mailto:abhinavpandey3419@gmail.com) · [LinkedIn](https://www.linkedin.com/in/abhinavpandey-ai-ml/) · [GitHub](https://github.com/Abhinav3419) · [Portfolio](https://abhinav3419.github.io/)

---

## License

MIT — See [LICENSE](LICENSE)

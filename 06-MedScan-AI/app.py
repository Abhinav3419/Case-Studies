"""
MedScan AI — Streamlit Web Interface (Gen-Z Modern UI)
=========================================================
Upload clinical lab report PDF or radiology text → full AI-powered analysis
with rich visualizations, animated gauges, and modern glassmorphism design.
"""

import streamlit as st
import os
import sys
import json
import tempfile
import plotly.graph_objects as go
import plotly.express as px

sys.path.insert(0, os.path.dirname(__file__))

from src.pdf_extractor import extract_report
from src.llm_engine import ClinicalAnalysisEngine, format_clinical_report, report_to_json
from src.radiology_parser import parse_radiology_report, correlate_with_bloodwork
from src.medical_verifier import MedicalVerificationSystem

st.set_page_config(
    page_title="MedScan AI",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Gen-Z CSS ──
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --accent: #6C5CE7;
    --accent2: #00CEC9;
    --danger: #FF6B6B;
    --warning: #FECA57;
    --success: #00D2D3;
    --bg-glass: rgba(255,255,255,0.05);
    --border-glass: rgba(255,255,255,0.1);
}

* { font-family: 'Inter', sans-serif !important; }

.hero-container {
    background: linear-gradient(135deg, #0c0c1d 0%, #1a1a3e 40%, #2d1b69 100%);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-container::before {
    content: '';
    position: absolute; top: -50%; right: -20%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(108,92,231,0.3) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-container::after {
    content: '';
    position: absolute; bottom: -30%; left: -10%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(0,206,201,0.2) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-size: 2.8rem; font-weight: 800; color: white;
    letter-spacing: -1px; position: relative; z-index: 1;
    background: linear-gradient(135deg, #fff 0%, #a29bfe 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 1.05rem; color: rgba(255,255,255,0.6);
    position: relative; z-index: 1; margin-top: 0.3rem;
}

.glass-card {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.stat-pill {
    display: inline-flex; align-items: center; gap: 0.5rem;
    background: rgba(108,92,231,0.15);
    border: 1px solid rgba(108,92,231,0.3);
    border-radius: 50px; padding: 0.6rem 1.2rem;
    font-weight: 600; font-size: 0.9rem;
}
.stat-pill-danger {
    background: rgba(255,107,107,0.15);
    border-color: rgba(255,107,107,0.3);
    color: #FF6B6B;
}
.stat-pill-success {
    background: rgba(0,210,211,0.15);
    border-color: rgba(0,210,211,0.3);
    color: #00D2D3;
}
.stat-pill-warning {
    background: rgba(254,202,87,0.15);
    border-color: rgba(254,202,87,0.3);
    color: #FECA57;
}

.badge-urgency {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    font-size: 0.72rem; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase;
}
.badge-routine { background: rgba(0,210,211,0.2); color: #00D2D3; }
.badge-soon { background: rgba(254,202,87,0.2); color: #FECA57; }
.badge-urgent { background: rgba(255,107,107,0.2); color: #FF6B6B; }
.badge-emergency { background: rgba(255,50,50,0.3); color: #FF3232; }

.section-header {
    font-size: 1.4rem; font-weight: 700; letter-spacing: -0.5px;
    margin: 1.5rem 0 0.8rem;
    display: flex; align-items: center; gap: 0.5rem;
}

.finding-card {
    background: linear-gradient(135deg, rgba(108,92,231,0.08) 0%, rgba(0,206,201,0.05) 100%);
    border: 1px solid rgba(108,92,231,0.15);
    border-radius: 14px; padding: 1.2rem; margin-bottom: 0.8rem;
}

.source-chip {
    display: inline-block; background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px; padding: 2px 10px;
    font-size: 0.7rem; color: rgba(255,255,255,0.5);
}

.disclaimer-banner {
    background: linear-gradient(135deg, rgba(255,107,107,0.1) 0%, rgba(254,202,87,0.1) 100%);
    border: 1px solid rgba(255,107,107,0.2);
    border-radius: 14px; padding: 1rem 1.5rem;
    font-size: 0.85rem; color: rgba(255,255,255,0.7);
    margin-top: 2rem;
}

div[data-testid="stExpander"] {
    border: 1px solid rgba(108,92,231,0.15) !important;
    border-radius: 14px !important;
    background: rgba(108,92,231,0.03) !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    padding: 8px 20px !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers: Plotly Charts ──

def make_gauge(value, min_val, max_val, title, ref_low, ref_high, unit=""):
    """Animated gauge chart for a biomarker."""
    is_normal = ref_low <= value <= ref_high
    color = "#00D2D3" if is_normal else ("#FF6B6B" if value > ref_high else "#6C5CE7")

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        number={"suffix": f" {unit}", "font": {"size": 28, "color": "white"}},
        title={"text": title, "font": {"size": 14, "color": "rgba(255,255,255,0.7)"}},
        gauge={
            "axis": {"range": [min_val, max_val], "tickcolor": "rgba(255,255,255,0.3)"},
            "bar": {"color": color, "thickness": 0.3},
            "bgcolor": "rgba(255,255,255,0.05)",
            "borderwidth": 0,
            "steps": [
                {"range": [ref_low, ref_high], "color": "rgba(0,210,211,0.15)"},
            ],
            "threshold": {
                "line": {"color": "white", "width": 2},
                "thickness": 0.8, "value": value,
            },
        },
    ))
    fig.update_layout(
        height=200, margin=dict(l=20, r=20, t=40, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "white"},
    )
    return fig


def make_deviation_bar_chart(interpretations):
    """Horizontal bar chart of biomarker deviations."""
    data = sorted(
        [{"name": bi.test_name.split("(")[0].strip()[:20],
          "deviation": bi.deviation_pct * (1 if "HIGH" in bi.flag else -1),
          "flag": bi.flag, "urgency": bi.urgency}
         for bi in interpretations if bi.deviation_pct > 0],
        key=lambda x: abs(x["deviation"]), reverse=True
    )[:15]

    if not data:
        return None

    colors = ["#FF6B6B" if d["deviation"] > 0 else "#6C5CE7" for d in data]

    fig = go.Figure(go.Bar(
        y=[d["name"] for d in data],
        x=[d["deviation"] for d in data],
        orientation='h',
        marker_color=colors,
        marker_line_width=0,
        text=[f"{d['deviation']:+.1f}%" for d in data],
        textposition="outside",
        textfont={"size": 11, "color": "rgba(255,255,255,0.7)"},
    ))
    fig.update_layout(
        height=max(300, len(data) * 32),
        margin=dict(l=10, r=60, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            title="Deviation from normal (%)", title_font=dict(size=11, color="rgba(255,255,255,0.5)"),
            gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.2)",
            tickfont=dict(color="rgba(255,255,255,0.5)"),
        ),
        yaxis=dict(tickfont=dict(size=11, color="rgba(255,255,255,0.8)"), autorange="reversed"),
        font={"color": "white"},
    )
    return fig


def make_category_donut(interpretations):
    """Donut chart of abnormal biomarkers by body system."""
    from collections import Counter
    cat_map = {
        "haemoglobin": "Blood", "total_wbc_count": "Blood", "esr": "Blood", "rdw": "Blood",
        "packed_cell_volume": "Blood", "neutrophils": "Blood",
        "total_cholesterol": "Lipids", "triglycerides": "Lipids", "hdl_cholesterol": "Lipids",
        "ldl_cholesterol": "Lipids", "vldl_cholesterol": "Lipids",
        "sgot_ast": "Liver", "sgpt_alt": "Liver", "ggt": "Liver",
        "total_bilirubin": "Liver", "direct_bilirubin": "Liver",
        "tsh": "Thyroid", "free_t3": "Thyroid", "free_t4": "Thyroid",
        "fasting_blood_sugar": "Diabetes", "hba1c": "Diabetes",
        "vitamin_d": "Vitamins", "vitamin_b12": "Vitamins",
        "iron_serum": "Iron", "ferritin": "Iron", "tibc": "Iron", "transferrin_saturation": "Iron",
        "uric_acid": "Kidney", "crp": "Infection", "procalcitonin": "Infection",
        "psa": "Tumour", "ca125": "Tumour", "cea": "Tumour", "afp": "Tumour",
        "d_dimer": "Coagulation", "pt": "Coagulation", "aptt": "Coagulation",
    }
    cats = [cat_map.get(bi.canonical_name, "Other") for bi in interpretations]
    counts = Counter(cats)

    palette = ["#6C5CE7", "#00CEC9", "#FF6B6B", "#FECA57", "#a29bfe",
               "#fd79a8", "#55efc4", "#fdcb6e", "#74b9ff"]

    fig = go.Figure(go.Pie(
        labels=list(counts.keys()), values=list(counts.values()),
        hole=0.55, marker=dict(colors=palette[:len(counts)], line=dict(width=0)),
        textinfo="label+percent", textfont=dict(size=11, color="white"),
        hovertemplate="%{label}: %{value} abnormal<extra></extra>",
    ))
    fig.update_layout(
        height=280, margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"), showlegend=False,
        annotations=[dict(text="Systems", x=0.5, y=0.5, font_size=13, font_color="rgba(255,255,255,0.5)", showarrow=False)],
    )
    return fig


def make_urgency_breakdown(interpretations):
    """Stacked bar showing urgency distribution."""
    from collections import Counter
    urgencies = Counter(bi.urgency for bi in interpretations)
    colors = {"routine": "#00D2D3", "soon": "#FECA57", "urgent": "#FF6B6B", "emergency": "#FF3232"}

    fig = go.Figure()
    x_val = 0
    for urg in ["routine", "soon", "urgent", "emergency"]:
        count = urgencies.get(urg, 0)
        if count > 0:
            fig.add_trace(go.Bar(
                x=[count], y=["Urgency"], orientation="h",
                name=urg.capitalize(), marker_color=colors.get(urg, "#888"),
                text=[f"{urg.capitalize()}: {count}"], textposition="inside",
                textfont=dict(size=12, color="white"),
                hovertemplate=f"{urg.capitalize()}: {count}<extra></extra>",
            ))

    fig.update_layout(
        barmode="stack", height=80,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        showlegend=False, font=dict(color="white"),
    )
    return fig


# ── Sidebar ──
with st.sidebar:
    st.markdown("## 🧬 MedScan AI")
    st.markdown("`v0.4 — Day 4`")
    st.markdown("---")

    analysis_mode = st.selectbox(
        "⚡ Analysis Engine",
        ["Local (offline)", "Anthropic (Claude)", "OpenAI (GPT-4o)"],
        index=0,
    )
    mode = {"Local (offline)": "local", "Anthropic (Claude)": "anthropic", "OpenAI (GPT-4o)": "openai"}[analysis_mode]

    st.markdown("---")
    st.markdown("### 📊 Coverage")
    coverage_items = [
        "CBC & Blood Count", "Lipid Profile", "Liver Function", "Thyroid Panel",
        "Kidney Function", "Diabetes / HbA1c", "Vitamins & Iron",
        "🆕 Infectious Disease", "🆕 Tumour Markers", "🆕 Coagulation",
        "🆕 Genetic / Haematology", "🆕 Radiology Text Reports",
    ]
    for item in coverage_items:
        st.markdown(f"- {item}")

    st.markdown("---")
    st.markdown("### 📚 Sources")
    st.caption("Harrison's · WHO · ICMR · AHA/ACC · ADA · NCCN · ATA · KDIGO · ISTH · NACO")


# ── Hero Section ──
st.markdown("""
<div class="hero-container">
    <div class="hero-title">MedScan AI</div>
    <div class="hero-sub">Upload a clinical lab report or radiology text — get AI-powered analysis with cited medical references</div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──
tab_blood, tab_radiology = st.tabs(["🩸 Blood Report (PDF)", "🔬 Radiology Report (Text)"])

with tab_blood:
    col_upload, col_demo = st.columns([3, 1])
    with col_upload:
        uploaded_file = st.file_uploader("Upload lab report PDF", type=["pdf"], label_visibility="collapsed",
                                          help="Thyrocare, Dr. Lal PathLabs, SRL, Metropolis, etc.")
    with col_demo:
        st.markdown("<br>", unsafe_allow_html=True)
        use_demo = st.button("🔬 Demo Report", use_container_width=True)

    if uploaded_file is not None or use_demo:
        if use_demo:
            pdf_path = os.path.join(os.path.dirname(__file__), "data", "sample_reports", "sample_report_01_cbc_lipid.pdf")
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                pdf_path = tmp.name

        with st.spinner("🧬 Analyzing biomarkers..."):
            engine = ClinicalAnalysisEngine(mode=mode)
            report = engine.analyze_report(pdf_path)
            extraction = extract_report(pdf_path)

        # ── Stats Pills ──
        st.markdown("")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f'<div class="stat-pill">&#x1F9EA; {report.total_tests} tests analyzed</div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="stat-pill stat-pill-danger">&#x26A0;&#xFE0F; {report.abnormal_count} abnormal</div>', unsafe_allow_html=True)
        with c3:
            urgent_n = sum(1 for bi in report.biomarker_interpretations if bi.urgency in ("urgent", "emergency"))
            st.markdown(f'<div class="stat-pill stat-pill-warning">&#x1F525; {urgent_n} need attention</div>', unsafe_allow_html=True)
        with c4:
            normal_n = report.total_tests - report.abnormal_count
            st.markdown(f'<div class="stat-pill stat-pill-success">&#x2705; {normal_n} normal</div>', unsafe_allow_html=True)

        # ── Patient Card ──
        st.markdown(f"""
        <div class="glass-card" style="margin-top:1rem;">
            <div style="display:flex;gap:2rem;flex-wrap:wrap;">
                <div><span style="color:rgba(255,255,255,0.5);font-size:0.8rem;">Patient</span><br>
                    <span style="font-weight:700;font-size:1.1rem;">{report.patient_name or 'N/A'}</span></div>
                <div><span style="color:rgba(255,255,255,0.5);font-size:0.8rem;">Age / Sex</span><br>
                    <span style="font-weight:600;">{report.patient_age or 'N/A'} / {report.patient_sex or 'N/A'}</span></div>
                <div><span style="color:rgba(255,255,255,0.5);font-size:0.8rem;">Lab</span><br>
                    <span style="font-weight:600;">{report.lab_name or 'N/A'}</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Executive Summary ──
        st.markdown('<div class="section-header">📋 Executive Summary#x1F4CB; Executive Summary</div>', unsafe_allow_html=True)
        st.info(report.executive_summary)

        # ── Urgency Bar ──
        urg_fig = make_urgency_breakdown(report.biomarker_interpretations)
        st.plotly_chart(urg_fig, use_container_width=True, config={"displayModeBar": False})

        # ── Visual Dashboard Row ──
        st.markdown('<div class="section-header">📊 Visual Dashboard#x1F4CA; Visual Dashboard</div>', unsafe_allow_html=True)
        viz_col1, viz_col2 = st.columns([3, 2])

        with viz_col1:
            dev_fig = make_deviation_bar_chart(report.biomarker_interpretations)
            if dev_fig:
                st.plotly_chart(dev_fig, use_container_width=True, config={"displayModeBar": False})

        with viz_col2:
            donut_fig = make_category_donut(report.biomarker_interpretations)
            st.plotly_chart(donut_fig, use_container_width=True, config={"displayModeBar": False})

        # ── Key Gauges ──
        key_biomarkers = ["haemoglobin", "hba1c", "tsh", "ldl_cholesterol", "vitamin_d", "ferritin"]
        gauge_cols = st.columns(3)
        gauge_count = 0
        for bi in report.biomarker_interpretations:
            if bi.canonical_name in key_biomarkers and gauge_count < 6:
                ref_data = None
                from src.clinical_references import REFERENCE_RANGES
                if bi.canonical_name in REFERENCE_RANGES:
                    ref_data = REFERENCE_RANGES[bi.canonical_name]
                if ref_data and bi.value is not None:
                    rr = ref_data.get("ref_range", {})
                    sex_key = report.patient_sex.lower() if report.patient_sex else "all"
                    if sex_key in rr:
                        lo, hi = rr[sex_key]
                    elif "all" in rr:
                        lo, hi = rr["all"]
                    else:
                        continue
                    gauge_min = min(lo * 0.3, bi.value * 0.5)
                    gauge_max = max(hi * 1.5, bi.value * 1.3)
                    with gauge_cols[gauge_count % 3]:
                        fig = make_gauge(bi.value, gauge_min, gauge_max,
                                         bi.test_name.split("(")[0].strip(), lo, hi, bi.unit)
                        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                    gauge_count += 1

        # ── Detailed Interpretations ──
        st.markdown('<div class="section-header">🔴 Abnormal Values#x1F534; Abnormal Values — Detailed Interpretation</div>', unsafe_allow_html=True)

        for bi in report.biomarker_interpretations:
            flag_arrow = "HIGH" if "HIGH" in bi.flag else "LOW"
            label = f"{bi.test_name} — {bi.value} {bi.unit} [{bi.flag}] ({bi.urgency.upper()})"

            with st.expander(label, expanded=False):
                st.markdown(f'<span class="badge-urgency badge-{bi.urgency}">{bi.urgency.upper()}</span>', unsafe_allow_html=True)
                st.markdown(f"**{bi.clinical_significance}**")

                if bi.interpretation_band:
                    st.markdown(f"Band: `{bi.interpretation_band}` · Deviation: `{bi.deviation_pct}%`")

                c_a, c_b = st.columns(2)
                with c_a:
                    st.markdown("**Possible Causes:**")
                    for cause in bi.possible_causes:
                        st.markdown(f"- {cause}")
                with c_b:
                    st.markdown("**Recommended Actions:**")
                    for action in bi.recommended_actions:
                        st.markdown(f"- {action}")

                if bi.sources:
                    st.markdown(f'<span class="source-chip">📚 {bi.sources[0]}</span>', unsafe_allow_html=True)

        # ── Combined Patterns ──
        if report.pattern_interpretations:
            st.markdown('<div class="section-header">🔗 Cross-Biomarker#x1F517; Cross-Biomarker Patterns</div>', unsafe_allow_html=True)
            for p in report.pattern_interpretations:
                st.markdown(f"""
                <div class="finding-card">
                    <div style="font-weight:700;font-size:1.05rem;margin-bottom:0.5rem;">🔗 {p.pattern_name}</div>
                    <div style="color:rgba(255,255,255,0.7);font-size:0.9rem;margin-bottom:0.5rem;">{p.clinical_reasoning[:300]}...</div>
                    <div style="font-weight:600;">Suggests: {p.diagnosis_suggestion}</div>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("Recommended workup", expanded=False):
                    for w in p.recommended_workup:
                        st.markdown(f"- {w}")
                    if p.sources:
                        st.markdown(f'<span class="source-chip">📚 {p.sources[0]}</span>', unsafe_allow_html=True)

        # ── Normal Values Table ──
        st.markdown('<div class="section-header">🟢 Normal Values#x1F7E2; Normal Values</div>', unsafe_allow_html=True)
        normals = [b for b in extraction.biomarkers if not b.is_abnormal]
        if normals:
            normal_df = [{"Test": b.test_name, "Value": f"{b.value_raw} {b.unit}",
                         "Reference": b.reference_range_reported or b.reference_range_standard}
                        for b in normals]
            st.dataframe(normal_df, use_container_width=True, hide_index=True)

        # ── Recommendations ──
        r_col1, r_col2 = st.columns(2)
        with r_col1:
            st.markdown('<div class="section-header">💪 Lifestyle#x1F4AA; Lifestyle</div>', unsafe_allow_html=True)
            for rec in report.lifestyle_recommendations:
                st.markdown(f"- {rec}")
        with r_col2:
            st.markdown('<div class="section-header">🔬 Follow-up Tests#x1F52C; Follow-up Tests</div>', unsafe_allow_html=True)
            for test in report.follow_up_tests:
                st.markdown(f"- {test}")

        # ── Downloads ──
        st.markdown("---")
        dl1, dl2 = st.columns(2)
        with dl1:
            st.download_button("📥 Download JSON Report", report_to_json(report),
                               "medscan_report.json", "application/json", use_container_width=True)
        with dl2:
            st.download_button("📥 Download Text Report", format_clinical_report(report),
                               "medscan_report.txt", "text/plain", use_container_width=True)

        # ── Disclaimer ──
        st.markdown(f'<div class="disclaimer-banner">⚕️ <b>DISCLAIMER:</b> {report.disclaimer}</div>', unsafe_allow_html=True)

        if not use_demo and os.path.exists(pdf_path):
            os.unlink(pdf_path)


with tab_radiology:
    st.markdown("### 📝 Paste Radiology Report Text")
    st.caption("Paste the radiologist's written findings from a CT, MRI, X-ray, or ultrasound report.")

    sample_rad = """CT ABDOMEN WITH CONTRAST — FINDINGS:
Liver is mildly enlarged (span 17.2 cm) with diffuse fatty liver changes. No focal hepatic mass.
Mild hepatomegaly noted. Intrahepatic biliary radicles are not dilated.
Gallbladder is distended with a 6mm calculus noted in the neck.
Spleen is normal in size. Pancreas appears normal.
Both kidneys are normal in size with a 4mm renal calculus in the lower pole of left kidney.
No hydronephrosis. No free fluid in the abdomen.
Mild mesenteric lymphadenopathy noted.

IMPRESSION:
1. Fatty liver with mild hepatomegaly.
2. Cholelithiasis (6mm calculus).
3. Left renal calculus (4mm).
4. Mild mesenteric lymphadenopathy — correlate clinically."""

    rad_text = st.text_area("Radiology report text", value="", height=250,
                             placeholder="Paste report here or click 'Use Sample' below...")

    if st.button("📋 Use Sample Report"):
        rad_text = sample_rad
        st.rerun()

    if rad_text.strip():
        rad_report = parse_radiology_report(rad_text)

        st.markdown(f"""
        <div class="glass-card">
            <div style="display:flex;gap:2rem;">
                <div><span style="color:rgba(255,255,255,0.5);font-size:0.8rem;">Modality</span><br>
                    <span style="font-weight:700;">{rad_report.modality}</span></div>
                <div><span style="color:rgba(255,255,255,0.5);font-size:0.8rem;">Body Part</span><br>
                    <span style="font-weight:700;">{rad_report.body_part}</span></div>
                <div><span style="color:rgba(255,255,255,0.5);font-size:0.8rem;">Findings</span><br>
                    <span style="font-weight:700;">{len(rad_report.findings)} detected</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if rad_report.impression:
            st.markdown("**Impression:**")
            st.info(rad_report.impression)

        if rad_report.findings:
            st.markdown('<div class="section-header">🔍 Structured Findings#x1F50D; Structured Findings</div>', unsafe_allow_html=True)

            severity_colors = {"mild": "#FECA57", "moderate": "#FF9F43", "severe": "#FF6B6B"}

            for f in rad_report.findings:
                sev_color = severity_colors.get(f.severity, "#888")
                st.markdown(f"""
                <div class="finding-card">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <span style="font-weight:700;">{f.body_region}: {f.finding[:100]}</span>
                        <span style="background:{sev_color}22;color:{sev_color};padding:2px 10px;border-radius:20px;font-size:0.75rem;font-weight:700;">{f.severity.upper()}</span>
                    </div>
                    <div style="color:rgba(255,255,255,0.6);font-size:0.85rem;margin-top:0.5rem;">
                        Category: {f.category} · Related labs: {', '.join(f.related_biomarkers[:4])}
                    </div>
                    <div style="color:rgba(255,255,255,0.5);font-size:0.8rem;margin-top:0.3rem;">
                        💡 {f.recommended_correlation}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No specific findings matched. Try pasting a more detailed radiology report.")

        # ── Anatomical Verification (Multi-Agent) ──
        if rad_report.findings:
            st.markdown('<div class="section-header">🛡️ Anatomical Verification#x1F6E1;🛡️ Anatomical Verification#xFE0F; Anatomical Verification (AI Auditor)</div>', unsafe_allow_html=True)

            verifier = MedicalVerificationSystem()
            v_report = verifier.verify_radiology(
                rad_report.findings, rad_report.body_part.lower(), rad_report.modality
            )

            vc1, vc2, vc3 = st.columns(3)
            with vc1:
                st.markdown(f'<div class="stat-pill stat-pill-success">✅ {v_report.valid_facts} valid</div>', unsafe_allow_html=True)
            with vc2:
                st.markdown(f'<div class="stat-pill stat-pill-danger">🚨 {v_report.flagged_facts} flagged</div>', unsafe_allow_html=True)
            with vc3:
                conf_pct = int(v_report.overall_confidence * 100)
                st.markdown(f'<div class="stat-pill">🎯 {conf_pct}% confidence</div>', unsafe_allow_html=True)

            if v_report.flagged_facts > 0:
                for ar in v_report.audit_results:
                    if not ar.is_valid:
                        st.markdown(f"""
                        <div style="background:rgba(255,50,50,0.1);border:1px solid rgba(255,50,50,0.3);
                                    border-radius:12px;padding:1rem;margin:0.5rem 0;">
                            <div style="font-weight:700;color:#FF6B6B;">⚠️ {ar.error_type.replace('_',' ').upper()}</div>
                            <div style="color:rgba(255,255,255,0.8);margin-top:0.3rem;">{ar.error_message}</div>
                            <details style="margin-top:0.5rem;color:rgba(255,255,255,0.5);font-size:0.8rem;">
                                <summary>Chain-of-thought reasoning</summary>
                                <pre style="white-space:pre-wrap;font-size:0.75rem;color:rgba(255,255,255,0.6);">{ar.cot_reasoning}</pre>
                            </details>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.success("All findings passed anatomical verification — no inconsistencies detected.")

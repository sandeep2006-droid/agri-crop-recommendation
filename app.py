import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ── CONFIG ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tamil Nadu Crop Advisor",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CUSTOM CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #f5f2eb;
}

.hero {
    background: #1a3a2a;
    border-radius: 16px;
    padding: 36px 40px 28px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '🌾';
    font-size: 120px;
    position: absolute;
    right: 40px;
    top: 10px;
    opacity: 0.12;
}

.hero h1 {
    font-family: 'DM Serif Display', serif;
    color: #e8f5e0;
    font-size: 2.2rem;
    margin: 0 0 6px 0;
    font-weight: 400;
}

.hero p {
    color: #94b88a;
    margin: 0;
    font-size: 1rem;
}

.input-card {
    background: white;
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 24px;
    border: 1px solid #e8e2d8;
}

.crop-card {
    background: white;
    border-radius: 14px;
    padding: 22px 24px;
    margin-bottom: 14px;
    border: 1px solid #e8e2d8;
    border-left: 5px solid #2d7a4f;
    min-height: 90px;
}

.avoid-card {
    background: #fff8f8;
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 10px;
    border: 1px solid #f0d8d8;
    border-left: 5px solid #ff334d;
    min-height: 72px;
}

.alt-card {
    background: #f0f8f4;
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 8px;
    border: 1px solid #c8e6d4;
    border-left: 5px solid #2d8a55;
    min-height: 50px;
}

.risk-panel {
    background: white;
    border-radius: 14px;
    padding: 22px 24px;
    border: 1px solid #e8e2d8;
    margin-bottom: 16px;
    min-height: 90px;
}

.section-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #7a8f82;
    margin-bottom: 12px;
    margin-top: 4px;
}

.no-data {
    background: #f9f7f3;
    border-radius: 10px;
    padding: 16px;
    text-align: center;
    color: #8a9a8f;
    font-size: 0.92rem;
    border: 1px dashed #d0ccc4;
}

</style>
""", unsafe_allow_html=True)


# ── LOAD ────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("FINAL_READY_DATASET.csv")
    df.columns = df.columns.str.strip().str.replace(" ", "_")
    return df


@st.cache_resource
def load_model():
    return joblib.load("clf_model.pkl")


df = load_data()
clf = load_model()


FEATURES = [
    "Water_Score",
    "Temp_Score",
    "Soil_Score",
    "Avg_Rainfall_mm",
    "Production_MT",
    "District_Temp_Min",
    "District_Temp_Max",
    "Water_Min",
    "Water_Max"
]


# ── HELPERS ─────────────────────────────────────────────────────────
def predict_score(row_df):
    proba = clf.predict_proba(row_df[FEATURES])[0]
    return proba[0] * 0.0 + proba[1] * 0.5 + proba[2] * 1.0


def match_label(score):
    if score >= 0.7:
        return "✅ Good"
    elif score >= 0.4:
        return "🟡 Moderate"
    else:
        return "❌ Low"


def score_class(score):
    if score >= 0.65:
        return ""
    elif score >= 0.45:
        return "moderate"
    else:
        return "poor"


# ── HERO ────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>Tamil Nadu Crop Advisor</h1>
  <p>AI-powered recommendations based on district rainfall, soil, and historical yield data</p>
</div>
""", unsafe_allow_html=True)


# ── INPUTS ──────────────────────────────────────────────────────────
st.markdown(
    '<div class="input-card">',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:
    district = st.selectbox(
        "📍 District",
        sorted(df["District"].unique())
    )

with c2:
    season = st.selectbox(
        "🌦 Season",
        ["Kharif", "Rabi"]
    )

with c3:
    crop_input = st.selectbox(
        "🔍 Check a specific crop",
        ["None"] + sorted(df["Crop"].unique())
    )

st.markdown('</div>', unsafe_allow_html=True)


# ── FILTER & SCORE ──────────────────────────────────────────────────
df_d = df[
    (df["District"] == district) &
    ((df["Season"] == season) | (df["Season"] == "Annual"))
].copy()


if not df_d.empty:

    df_d["ML_Score"] = df_d.apply(
        lambda r: predict_score(pd.DataFrame([r])),
        axis=1
    )

    df_d["Final_Score"] = (
        0.6 * df_d["Suitability_Score"] +
        0.4 * df_d["ML_Score"]
    )


df_sorted = df_d.sort_values(
    "Final_Score",
    ascending=False
)


# ── ORIGINAL SELECTION LOGIC ───────────────────────────────────────
top = df_sorted[
    df_sorted["Final_Score"] > 0.55
].head(3)

if top.empty:
    top = df_sorted.head(2)


avoid = df_sorted[
    df_sorted["Final_Score"] < 0.45
]

avoid = avoid[
    ~avoid["Crop"].isin(top["Crop"])
].head(3)


existing_crops = set(df_d["Crop"])

alternate = df[
    (~df["Crop"].isin(existing_crops)) &
    (df["Suitability_Score"] > 0.6)
].drop_duplicates(
    subset=["Crop"]
).head(4)


# ── LAYOUT ──────────────────────────────────────────────────────────
left, right = st.columns([3, 2])


# ═══════════════════════════════════════════════════════════════════
# LEFT SIDE
# ═══════════════════════════════════════════════════════════════════

with left:

    # ── RECOMMENDED CROPS ──────────────────────────────────────────
    st.markdown(
        '<p class="section-label">Recommended Crops</p>',
        unsafe_allow_html=True
    )

    # Three empty recommendation boxes
    for _ in range(3):
        st.markdown(
            '<div class="crop-card"></div>',
            unsafe_allow_html=True
        )


    # ── ALTERNATE OPTIONS ──────────────────────────────────────────
    st.markdown(
        '<p class="section-label" style="margin-top:24px">Alternate Options</p>',
        unsafe_allow_html=True
    )

    # Four empty alternate-option boxes
    for _ in range(4):
        st.markdown(
            '<div class="alt-card"></div>',
            unsafe_allow_html=True
        )


# ═══════════════════════════════════════════════════════════════════
# RIGHT SIDE
# ═══════════════════════════════════════════════════════════════════

with right:

    # ── CROPS TO AVOID ─────────────────────────────────────────────
    st.markdown(
        '<p class="section-label">Crops to Avoid</p>',
        unsafe_allow_html=True
    )

    # Three empty avoid boxes
    for _ in range(3):
        st.markdown(
            '<div class="avoid-card"></div>',
            unsafe_allow_html=True
        )


    # ── RISK ASSESSMENT ────────────────────────────────────────────
    st.markdown(
        '<p class="section-label" style="margin-top:20px">Risk Assessment</p>',
        unsafe_allow_html=True
    )

    # Empty risk assessment box
    st.markdown(
        '<div class="risk-panel"></div>',
        unsafe_allow_html=True
    )


    # ── DISTRICT SUMMARY ───────────────────────────────────────────
    # This section remains fully functional.

    if not df_d.empty:

        st.markdown(
            '<p class="section-label" style="margin-top:20px">District Summary</p>',
            unsafe_allow_html=True
        )

        avg_rain = df_d["Avg_Rainfall_mm"].iloc[0]

        num_crops = len(df_d)

        best_crop = (
            df_sorted.iloc[0]["Crop"].title()
            if not df_sorted.empty
            else "N/A"
        )

        st.markdown(
            f"""
            <div class="risk-panel">
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;text-align:center;">

                    <div style="background:#f5f2eb;border-radius:10px;padding:14px;">
                        <div style="font-size:1.4rem;font-weight:600;color:#1a3a2a;">
                            {avg_rain:.0f}
                            <span style="font-size:0.75rem;color:#7a8f82;">
                                mm
                            </span>
                        </div>

                        <div style="font-size:0.75rem;color:#7a8f82;margin-top:2px;">
                            Avg Rainfall
                        </div>
                    </div>


                    <div style="background:#f5f2eb;border-radius:10px;padding:14px;">
                        <div style="font-size:1.4rem;font-weight:600;color:#1a3a2a;">
                            {num_crops}
                        </div>

                        <div style="font-size:0.75rem;color:#7a8f82;margin-top:2px;">
                            Crops Tracked
                        </div>
                    </div>

                </div>


                <div style="margin-top:10px;background:#e8f5e0;border-radius:10px;padding:12px;text-align:center;font-size:0.85rem;color:#1a5c35;">
                    <span style="font-weight:600;">
                        Top pick this season:
                    </span>
                    {best_crop}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

import streamlit as st
import pandas as pd

# ── CONFIG ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Agricrop Recommendation Portal",
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

.info-box {
    background: white;
    border-radius: 14px;
    padding: 22px 24px;
    margin-bottom: 24px;
    border: 1px solid #e8e2d8;
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

.stat-box {
    background: white;
    border-radius: 12px;
    padding: 18px;
    border: 1px solid #e8e2d8;
    text-align: center;
}

.stat-number {
    font-size: 1.5rem;
    font-weight: 600;
    color: #1a3a2a;
}

.stat-label {
    font-size: 0.78rem;
    color: #7a8f82;
    margin-top: 4px;
}

</style>
""", unsafe_allow_html=True)


# ── LOAD DATASET ────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("FINAL_READY_DATASET.csv")
    df.columns = df.columns.str.strip().str.replace(" ", "_")
    return df


df = load_data()


# ── HEADER ──────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>Agricrop Recommendation Portal</h1>
    <p>Agricultural dataset preparation and exploration</p>
</div>
""", unsafe_allow_html=True)


# ── DATASET STATUS ─────────────────────────────────────────────────
st.success("Cleaned agricultural dataset loaded successfully.")


# ── DATASET OVERVIEW ────────────────────────────────────────────────
st.markdown(
    '<p class="section-label">Dataset Overview</p>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-number">{len(df):,}</div>
        <div class="stat-label">Records</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-number">{len(df.columns)}</div>
        <div class="stat-label">Features / Columns</div>
    </div>
    """, unsafe_allow_html=True)

if "District" in df.columns:
    district_count = df["District"].nunique()
else:
    district_count = 0

with c3:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-number">{district_count}</div>
        <div class="stat-label">Districts</div>
    </div>
    """, unsafe_allow_html=True)

if "Crop" in df.columns:
    crop_count = df["Crop"].nunique()
else:
    crop_count = 0

with c4:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-number">{crop_count}</div>
        <div class="stat-label">Crop Types</div>
    </div>
    """, unsafe_allow_html=True)


st.write("")


# ── FILTERS ────────────────────────────────────────────────────────
st.markdown(
    '<p class="section-label">Explore Dataset</p>',
    unsafe_allow_html=True
)

f1, f2 = st.columns(2)

filtered_df = df.copy()

with f1:
    if "District" in df.columns:
        districts = ["All Districts"] + sorted(
            df["District"].dropna().astype(str).unique().tolist()
        )

        selected_district = st.selectbox(
            "📍 District",
            districts
        )

        if selected_district != "All Districts":
            filtered_df = filtered_df[
                filtered_df["District"].astype(str) == selected_district
            ]

with f2:
    if "Season" in df.columns:
        seasons = ["All Seasons"] + sorted(
            df["Season"].dropna().astype(str).unique().tolist()
        )

        selected_season = st.selectbox(
            "🌦 Season",
            seasons
        )

        if selected_season != "All Seasons":
            filtered_df = filtered_df[
                filtered_df["Season"].astype(str) == selected_season
            ]


# ── DATASET TABLE ───────────────────────────────────────────────────
st.markdown(
    '<p class="section-label" style="margin-top:24px">Cleaned Dataset</p>',
    unsafe_allow_html=True
)

st.write(
    f"Showing **{len(filtered_df):,}** of **{len(df):,}** records."
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=500
)


# ── DATASET INFORMATION ────────────────────────────────────────────
st.markdown(
    '<p class="section-label" style="margin-top:28px">Dataset Information</p>',
    unsafe_allow_html=True
)

tab1, tab2 = st.tabs(["Column Information", "Basic Statistics"])

with tab1:
    column_info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": [str(df[col].dtype) for col in df.columns],
        "Non-Null Values": [df[col].notna().sum() for col in df.columns],
        "Missing Values": [df[col].isna().sum() for col in df.columns]
    })

    st.dataframe(
        column_info,
        use_container_width=True,
        hide_index=True
    )

with tab2:
    numeric_df = df.select_dtypes(include="number")

    if not numeric_df.empty:
        st.dataframe(
            numeric_df.describe().round(2),
            use_container_width=True
        )
    else:
        st.info("No numeric columns available for statistical summary.")


# ── FOOTER ──────────────────────────────────────────────────────────
st.markdown("---")

st.caption(
    "DA1: Data collection, cleaning, processing and dataset exploration"
)

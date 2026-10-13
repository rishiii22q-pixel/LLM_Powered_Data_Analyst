
import os

import pandas as pd
import plotly.express as px
import streamlit as st
from groq import Groq


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# DARK THEME + RESPONSIVE DESIGN
# ==================================================

st.markdown("""
<style>
:root {
    --bg-dark: #0b1220;
    --bg-panel: #121d2f;
    --bg-panel-strong: #16253d;
    --bg-soft: #1a2b43;
    --text-primary: #eef4ff;
    --text-muted: #adc1dd;
    --primary: #3b82f6;
    --primary-strong: #2563eb;
    --accent: #8ec5ff;
    --border: rgba(255, 255, 255, 0.08);
    --shadow: 0 18px 40px rgba(6, 10, 20, 0.35);
}

/* Main application */
.stApp {
    background: linear-gradient(180deg, #09111d 0%, #0d1729 100%);
    color: var(--text-primary);
}

[data-testid="stAppViewContainer"] {
    background: transparent;
}

[data-testid="stHeader"] {
    background: rgba(9, 17, 29, 0.9);
    border-bottom: 1px solid var(--border);
    backdrop-filter: blur(8px);
}

.block-container {
    max-width: 1420px;
    padding: 1.5rem 1.5rem 3rem 1.5rem;
}

html, body, [class*="css"], p, label, span, li {
    color: var(--text-primary);
}

h1, h2, h3, h4 {
    color: #f8fbff !important;
    letter-spacing: -0.02em;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(9, 17, 29, 0.96);
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] > div {
    background: rgba(9, 17, 29, 0.96);
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
    color: #dfeaff !important;
}

/* Hero section */
.hero {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, rgba(14, 27, 45, 0.95), rgba(59, 130, 246, 0.85));
    border: 1px solid rgba(142, 197, 255, 0.2);
    border-radius: 22px;
    padding: 28px 28px;
    margin-bottom: 24px;
    box-shadow: var(--shadow);
}

.hero::before {
    content: "";
    position: absolute;
    right: -40px;
    top: -40px;
    width: 220px;
    height: 220px;
    border-radius: 50%;
    background: rgba(142, 197, 255, 0.18);
    filter: blur(10px);
}

.hero h1 {
    position: relative;
    z-index: 1;
    font-size: clamp(28px, 4vw, 42px);
    line-height: 1.15;
    color: #ffffff !important;
    margin: 0 0 12px 0;
}

.hero p {
    position: relative;
    z-index: 1;
    font-size: 16px;
    line-height: 1.8;
    color: #dfeeff !important;
    margin: 0;
    max-width: 820px;
}

/* Home layout */
.info-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 18px;
    margin: 18px 0 26px;
}

.info-card {
    background: linear-gradient(180deg, rgba(18, 29, 47, 0.96), rgba(17, 24, 39, 0.88));
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 18px;
    padding: 20px 18px;
    box-shadow: 0 10px 24px rgba(5, 10, 18, 0.2);
}

.info-card .step {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border-radius: 10px;
    background: rgba(59, 130, 246, 0.18);
    color: #cfe3ff;
    font-weight: 700;
    margin-bottom: 12px;
}

.info-card h3 {
    margin: 0 0 10px;
    font-size: 1.1rem;
    color: #f8fbff !important;
}

.info-card p {
    margin: 0;
    color: var(--text-muted) !important;
    line-height: 1.7;
}

.simple-panel {
    background: linear-gradient(180deg, rgba(18, 29, 47, 0.94), rgba(14, 22, 36, 0.88));
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 20px;
    padding: 22px 22px 18px;
    margin-top: 10px;
    box-shadow: var(--shadow);
}

.simple-panel h2 {
    margin: 0 0 12px;
    font-size: 2rem;
    color: #f8fbff !important;
}

.simple-panel p {
    color: var(--text-muted) !important;
    line-height: 1.8;
    margin: 0;
}

/* Section headings */
.section-heading {
    font-size: 23px;
    font-weight: 700;
    color: #f8fafc;
    margin: 20px 0 14px 0;
    letter-spacing: -0.02em;
}

.small-muted {
    color: var(--text-muted);
    font-size: 14px;
    line-height: 1.6;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(180deg, rgba(17, 24, 39, 0.8), rgba(15, 23, 42, 0.92));
    border: 1px solid rgba(148, 163, 184, 0.16);
    border-radius: 16px;
    padding: 18px 16px;
    min-width: 0;
    box-shadow: 0 10px 20px rgba(2, 6, 23, 0.18);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    border-color: rgba(96, 165, 250, 0.6);
    box-shadow: 0 14px 28px rgba(37, 99, 235, 0.13);
}

[data-testid="stMetricLabel"] {
    color: #b8c4d8 !important;
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-weight: 700 !important;
}

[data-testid="stMetricDelta"] {
    color: #93c5fd !important;
}

/* Tabs */
[data-testid="stTabs"] [role="tablist"] {
    gap: 8px;
    border-bottom: 1px solid rgba(148, 163, 184, 0.25);
    margin-bottom: 12px;
}

[data-testid="stTabs"] button[role="tab"] {
    color: #dfe8f8 !important;
    background: rgba(15, 23, 42, 0.56);
    border: 1px solid transparent;
    border-radius: 12px 12px 0 0;
    padding: 12px 16px;
    font-weight: 600;
    transition: all 0.2s ease;
}

[data-testid="stTabs"] button[role="tab"]:hover {
    border-color: rgba(96, 165, 250, 0.35);
    color: #f8fafc !important;
}

[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #dbeafe !important;
    border: 1px solid rgba(96, 165, 250, 0.45);
    border-bottom: none;
    background: rgba(30, 41, 59, 0.8);
    box-shadow: inset 0 -1px 0 rgba(96, 165, 250, 0.6);
}

/* Inputs and dropdowns */
.stTextInput input,
.stTextArea textarea,
[data-baseweb="select"] > div,
[data-testid="stNumberInput"] input {
    background: rgba(17, 24, 39, 0.9) !important;
    color: #f8fafc !important;
    border: 1px solid rgba(148, 163, 184, 0.28) !important;
    border-radius: 12px !important;
    box-shadow: 0 0 0 0 rgba(96, 165, 250, 0);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: rgba(96, 165, 250, 0.9) !important;
    box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.14) !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #94a3b8 !important;
}

[data-baseweb="popover"],
[data-baseweb="menu"],
[data-baseweb="listbox"] {
    background: #172033 !important;
    color: #f8fafc !important;
}

[data-baseweb="menu"] *,
[data-baseweb="listbox"] * {
    color: #f8fafc !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(17, 24, 39, 0.8);
    border: 1px dashed rgba(148, 163, 184, 0.3);
    border-radius: 16px;
    padding: 16px;
    box-shadow: inset 0 0 0 1px rgba(148, 163, 184, 0.08);
}

[data-testid="stFileUploader"] section {
    background: rgba(17, 24, 39, 0.8);
}

/* Buttons */
.stButton > button,
.stDownloadButton > button {
    min-height: 46px;
    border-radius: 12px;
    font-weight: 600;
    border: 1px solid rgba(96, 165, 250, 0.75);
    background: linear-gradient(135deg, #2563eb, #3b82f6);
    color: #ffffff !important;
    transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease;
    box-shadow: 0 10px 18px rgba(37, 99, 235, 0.28);
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    filter: brightness(1.04);
    transform: translateY(-1px);
    box-shadow: 0 14px 22px rgba(37, 99, 235, 0.34);
}

/* Tables */
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    border: 1px solid rgba(148, 163, 184, 0.2);
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.12);
}

/* Dividers */
hr {
    border-color: rgba(148, 163, 184, 0.2) !important;
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Footer */
.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 13px;
    line-height: 1.8;
    padding: 28px 8px 10px;
}

@keyframes floatLift {
    from {
        opacity: 0;
        transform: translateY(8px);
    }
    to {
        opacity: 1;
        transform: translateY(0px);
    }
}

/* Responsive layout */
@media (max-width: 980px) {
    .block-container {
        padding: 1.1rem 1rem 2rem;
    }

    .hero {
        padding: 24px 20px;
        border-radius: 18px;
    }

    .info-grid {
        grid-template-columns: 1fr;
    }

    [data-testid="stTabs"] button[role="tab"] {
        font-size: 12px;
        padding: 10px 12px;
    }
}

@media (max-width: 680px) {
    .block-container {
        padding: 0.8rem 0.75rem 1.6rem;
    }

    .hero {
        padding: 20px 16px;
        border-radius: 16px;
        margin-bottom: 18px;
    }

    .hero h1 {
        font-size: 27px;
    }

    .hero p {
        font-size: 14px;
        line-height: 1.7;
    }

    .section-heading {
        font-size: 20px;
    }

    [data-testid="stMetric"] {
        padding: 12px;
        border-radius: 12px;
    }

    [data-testid="stMetricValue"] {
        font-size: 22px;
    }

    [data-testid="stTabs"] [role="tablist"] {
        gap: 6px;
        overflow-x: auto;
        white-space: nowrap;
        flex-wrap: nowrap;
    }

    [data-testid="stTabs"] button[role="tab"] {
        padding: 10px 10px;
        font-size: 11px;
        min-width: fit-content;
    }

    .stButton > button,
    .stDownloadButton > button {
        width: 100%;
    }
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# AI FUNCTION
# ==================================================

def ask_ai(question, df):
    api_key = st.secrets.get("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing from Streamlit secrets."
        )

    client = Groq(api_key=api_key)

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    text_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    # Provide dataset information and exact summaries.
    dataset_info = f"""
Dataset rows: {len(df)}
Dataset columns: {len(df.columns)}
Column names: {list(df.columns)}

Sample rows:
{df.head(15).to_csv(index=False)}

Numeric summary:
{df[numeric_columns].describe().to_string()
 if numeric_columns else "No numeric columns"}
"""

    # Exact category totals for the AI to reference.
    for text_col in text_columns:
        values = (
            df[text_col]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        dataset_info += (
            f"\n\nUnique values in {text_col}: "
            f"{values[:100]}"
        )

        for num_col in numeric_columns:
            grouped = (
                df.groupby(text_col, dropna=False)[num_col]
                .sum()
                .sort_values(ascending=False)
            )

            dataset_info += (
                f"\n\nTotal {num_col} grouped by {text_col}:\n"
                f"{grouped.head(50).to_string()}"
            )

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional data analyst. "
                    "Answer clearly using the supplied dataset "
                    "information. Never invent statistics. "
                    "Use exact provided totals and summaries. "
                    "For questions about available products or "
                    "categories, use the supplied unique values. "
                    "If the information is insufficient, say so. "
                    "Use readable headings and bullet points."
                )
            },
            {
                "role": "user",
                "content": (
                    f"DATASET INFORMATION:\n{dataset_info}\n\n"
                    f"QUESTION:\n{question}"
                )
            }
        ],
        temperature=0.2,
        max_tokens=700
    )

    return response.choices[0].message.content


# ==================================================
# SIDEBAR
# ==================================================

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown("## 📊 Data Analyst")
    st.caption("Smart workspace")

    st.markdown("---")

    st.markdown("### Quick status")
    st.success("Dataset ready")
    st.info("AI ready with Groq")

    st.markdown("### Quick guide")
    st.write("📁 Upload CSV")
    st.write("📋 Review rows")
    st.write("📈 Build charts")
    st.write("💡 See insights")
    st.write("🤖 Ask AI")

    st.markdown("---")

    if st.button("Load sample dataset", use_container_width=True, key="sidebar_sample_load"):
        if os.path.exists("sales.csv"):
            st.session_state["sample_data_loaded"] = True
            st.success("Sample dataset loaded.")
        else:
            st.warning("No sample dataset file found in the project folder.")

    st.caption("Simple. Clear. Data-driven.")


# ==================================================
# HEADER / HOME PAGE
# ==================================================

st.markdown("""
<div class="hero">
    <h1>AI-Powered Data Analyst</h1>
    <p>
        Turn raw CSV files into clean insights. Upload your data, review the structure,
        explore trends with charts, and ask natural-language questions to uncover what matters.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='section-heading'>How it works</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card">
        <div class="step">1</div>
        <h3>Upload</h3>
        <p>Select a CSV file from your device. The dashboard accepts standard spreadsheet data and reads it automatically.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <div class="step">2</div>
        <h3>Review</h3>
        <p>Check the dataset preview, column types, missing values, and statistics before you start exploring.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card">
        <div class="step">3</div>
        <h3>Analyze</h3>
        <p>Use interactive charts, key insights, and AI-powered question answering to understand your data faster.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="simple-panel">
    <h2>Upload your dataset</h2>
    <p>Click below to upload a CSV file. Once the file is loaded, the app will show the dataset preview, summary metrics, visual charts, and AI-based analysis tools.</p>
</div>
""", unsafe_allow_html=True)


# ==================================================
# UPLOAD DATASET
# ==================================================

st.markdown(
    '<div class="section-heading">Choose a file</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"],
    help="Upload your own dataset to start analysing."
)

df = None

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception:
        st.error(
            "Unable to read this file. Please check that "
            "it is a valid CSV file."
        )
        st.stop()

elif st.session_state.get("sample_data_loaded"):
    try:
        df = pd.read_csv("sales.csv")
        st.info(
            "Sample dataset loaded from the sidebar. Upload your own CSV "
            "to analyse a different dataset."
        )
    except Exception:
        st.warning("The sample sales.csv file could not be read.")

elif os.path.exists("sales.csv"):
    try:
        df = pd.read_csv("sales.csv")
        st.info(
            "Sample dataset loaded. Upload your own CSV "
            "to analyse a different dataset."
        )
    except Exception:
        st.warning("The sample sales.csv file could not be read.")

if df is None:
    st.markdown("""
    <div style="
        background:#111c2e;
        border:1px solid #334155;
        padding:25px;
        border-radius:16px;
        margin-top:18px;">
        <h3 style="color:#f8fafc;">Welcome to your data workspace</h3>
        <p style="color:#cbd5e1;line-height:1.8;">
        Upload a CSV dataset to access data summaries,
        interactive charts, automatic insights and AI-powered
        question answering.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.stop()

if df.empty:
    st.warning("The uploaded dataset contains no data rows.")
    st.stop()

if len(df.columns) == 0:
    st.warning("No columns were found in the uploaded dataset.")
    st.stop()


# ==================================================
# PREPARE DATA
# ==================================================

numeric_columns = df.select_dtypes(
    include="number"
).columns.tolist()

text_columns = df.select_dtypes(
    include=["object", "category"]
).columns.tolist()


# ==================================================
# OVERVIEW METRICS
# ==================================================

st.markdown(
    '<div class="section-heading">Dataset Overview</div>',
    unsafe_allow_html=True
)

m1, m2, m3, m4 = st.columns(4)

m1.metric("Total Rows", f"{df.shape[0]:,}")
m2.metric("Total Columns", f"{df.shape[1]:,}")
m3.metric("Numeric Columns", len(numeric_columns))
m4.metric("Missing Values", f"{df.isna().sum().sum():,}")


# ==================================================
# MAIN WORKSPACE
# ==================================================

overview_tab, charts_tab, insights_tab, ai_tab = st.tabs([
    "📋 Overview",
    "📈 Charts",
    "💡 Insights",
    "🤖 Ask AI"
])


# ==================================================
# TAB 1 — DATASET OVERVIEW
# ==================================================

with overview_tab:
    st.markdown("### Dataset Preview")
    st.caption("Review your data before starting the analysis.")

    st.markdown("### Dataset Preview")
    st.dataframe(
        df.head(100),
        use_container_width=True,
        hide_index=True,
        height=520
    )

    st.markdown("### Column Information")

    column_info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": [
            str(df[col].dtype) for col in df.columns
        ],
        "Missing Values": [
            int(df[col].isna().sum()) for col in df.columns
        ],
        "Unique Values": [
            int(df[col].nunique()) for col in df.columns
        ]
    })

    st.dataframe(
        column_info,
        use_container_width=True,
        hide_index=True
    )

    if numeric_columns:
        st.markdown("### Statistical Summary")

        st.dataframe(
            df[numeric_columns].describe().round(2),
            use_container_width=True
        )

    st.download_button(
        "⬇️ Download Dataset",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="analysed_dataset.csv",
        mime="text/csv",
        use_container_width=True
    )


# ==================================================
# TAB 2 — DATA VISUALIZATION
# ==================================================

with charts_tab:
    st.markdown("### Interactive Data Visualization")
    st.caption("Choose the chart that best explains your data.")

    if not numeric_columns:
        st.warning(
            "No numeric columns were detected. "
            "Charts require at least one numeric column."
        )

    else:
        chart_type = st.selectbox(
            "Chart type",
            ["Bar Chart", "Line Chart", "Histogram"]
        )

        if chart_type in ["Bar Chart", "Line Chart"]:
            x_column = st.selectbox(
                "X-axis",
                df.columns.tolist()
            )

            y_column = st.selectbox(
                "Y-axis",
                numeric_columns
            )

            if chart_type == "Bar Chart":
                fig = px.bar(
                    df,
                    x=x_column,
                    y=y_column,
                    title=f"{y_column} by {x_column}",
                    template="plotly_dark"
                )
            else:
                fig = px.line(
                    df,
                    x=x_column,
                    y=y_column,
                    title=f"{y_column} over {x_column}",
                    markers=True,
                    template="plotly_dark"
                )

        else:
            hist_column = st.selectbox(
                "Numeric column",
                numeric_columns
            )

            fig = px.histogram(
                df,
                x=hist_column,
                title=f"Distribution of {hist_column}",
                template="plotly_dark"
            )

        fig.update_layout(
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font=dict(color="#e5e7eb", size=13),
            title_font=dict(color="#f8fafc", size=20),
            margin=dict(l=15, r=15, t=60, b=20),
            legend=dict(
                bgcolor="rgba(17,24,39,0.7)",
                font=dict(color="#e5e7eb")
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            theme=None
        )


# ==================================================
# TAB 3 — AUTOMATIC INSIGHTS
# ==================================================

with insights_tab:
    st.markdown("### Automatic Data Insights")
    st.caption(
        "Explore important statistics calculated directly using Pandas."
    )

    if not numeric_columns:
        st.warning("No numeric columns are available for analysis.")

    else:
        selected_column = st.selectbox(
            "Select a numeric column",
            numeric_columns,
            key="insight_column"
        )

        values = df[selected_column].dropna()

        if values.empty:
            st.warning("This column has no valid numeric values.")

        else:
            a, b, c, d = st.columns(4)

            a.metric("Total", f"{values.sum():,.2f}")
            b.metric("Average", f"{values.mean():,.2f}")
            c.metric("Highest", f"{values.max():,.2f}")
            d.metric("Lowest", f"{values.min():,.2f}")

            highest_idx = values.idxmax()
            lowest_idx = values.idxmin()

            st.markdown("### Record with the highest value")
            st.dataframe(
                df.loc[[highest_idx]],
                use_container_width=True,
                hide_index=True
            )

            st.markdown("### Record with the lowest value")
            st.dataframe(
                df.loc[[lowest_idx]],
                use_container_width=True,
                hide_index=True
            )

            if text_columns:
                category_column = st.selectbox(
                    "Group totals by category",
                    text_columns,
                    key="insight_category"
                )

                category_totals = (
                    df.groupby(
                        category_column,
                        dropna=False
                    )[selected_column]
                    .sum()
                    .sort_values(ascending=False)
                    .reset_index()
                )

                st.markdown("### Category-wise totals")

                st.dataframe(
                    category_totals,
                    use_container_width=True,
                    hide_index=True
                )

                if not category_totals.empty:
                    top = category_totals.iloc[0]

                    st.success(
                        f"Top category: {top[category_column]} — "
                        f"{top[selected_column]:,.2f}"
                    )


# ==================================================
# TAB 4 — ASK AI
# ==================================================

with ai_tab:
    st.markdown("### Ask Questions About Your Data")
    st.caption(
        "Ask questions in everyday English and get AI-generated answers."
    )

    with st.expander("💬 Example questions", expanded=True):
        st.markdown("""
        - What products are available in this dataset?
        - Which product has the highest sales?
        - What is the average sales value?
        - Which category has the highest total?
        - Summarize this dataset.
        """)

    question = st.text_input(
        "Your question",
        placeholder="e.g. Which category has the highest sales?",
        key="ai_question"
    )

    if st.button(
        "✨ Analyse with AI",
        type="primary",
        use_container_width=True
    ):
        if not question.strip():
            st.warning("Please enter a question.")

        else:
            q = question.lower().strip()

            # Use Pandas for common exact calculations.
            numeric_match = next(
                (
                    col for col in numeric_columns
                    if col.lower() in q
                ),
                numeric_columns[0] if numeric_columns else None
            )

            if (
                numeric_match
                and any(word in q for word in ["total", "sum"])
            ):
                st.success(
                    f"Total {numeric_match}: "
                    f"{df[numeric_match].sum():,.2f}"
                )

            elif (
                numeric_match
                and any(word in q for word in ["average", "mean"])
            ):
                st.success(
                    f"Average {numeric_match}: "
                    f"{df[numeric_match].mean():,.2f}"
                )

            elif (
                numeric_match
                and any(
                    word in q
                    for word in ["highest", "maximum", "max"]
                )
            ):
                valid = df[numeric_match].dropna()

                if valid.empty:
                    st.warning("No valid values were found.")

                else:
                    idx = valid.idxmax()
                    st.markdown("### Highest-value record")
                    st.dataframe(
                        df.loc[[idx]],
                        use_container_width=True,
                        hide_index=True
                    )

            elif (
                numeric_match
                and any(
                    word in q
                    for word in ["lowest", "minimum", "min"]
                )
            ):
                valid = df[numeric_match].dropna()

                if valid.empty:
                    st.warning("No valid values were found.")

                else:
                    idx = valid.idxmin()
                    st.markdown("### Lowest-value record")
                    st.dataframe(
                        df.loc[[idx]],
                        use_container_width=True,
                        hide_index=True
                    )

            else:
                try:
                    with st.spinner(
                        "AI is analysing your dataset..."
                    ):
                        answer = ask_ai(question, df)

                    st.markdown("### 🤖 AI Answer")
                    st.markdown(answer)

                except Exception:
                    st.error(
                        "The AI request could not be completed."
                    )

                    st.info(
                        "Check your Groq API key, internet connection, "
                        "model availability, and free-tier limits. "
                        "Your Pandas analysis and charts can still work."
                    )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.markdown("""
<div class="footer">
    <strong>AI-Powered Data Analyst</strong><br>
    Intelligent analysis · Interactive visualizations · AI assistance<br>
    Built with Streamlit, Pandas, Plotly and Groq
</div>
""", unsafe_allow_html=True)

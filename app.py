"""
ReNew OCR Document Tracker - Streamlit App

Extracts data from procurement PDFs and fills Excel tracker sheets.
Styled to match https://www.renew.com/ brand identity.
"""

import os
import tempfile
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

from config import CASE_DESCRIPTIONS, COLUMN_MAPPINGS, OPENROUTER_MODELS, SHEET_NAMES
from ocr_engine import extract_text_from_pdf, get_combined_text, get_page_count
from extractor import DocumentExtractor
from mapper import map_to_tracker
from excel_writer import write_tracker

# ── Page Config ──
st.set_page_config(
    page_title="ReNew OCR Tracker",
    page_icon="R",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── ReNew Brand Theme CSS ──
st.markdown("""
<style>
    /* ── Import Google Fonts (closest to Gotham) ── */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800;900&display=swap');

    /* ── Global Font ── */
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }

    /* ── Hide Streamlit branding ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ── Main background ── */
    .stApp {
        background-color: #F6F6F6;
    }

    /* ── Sidebar styling ── */
    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e0e0e0;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stRadio label span {
        color: #313638 !important;
    }

    /* ── Green accent buttons ── */
    .stButton > button[kind="primary"],
    .stDownloadButton > button[kind="primary"] {
        background-color: #72BF44 !important;
        border: none !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        padding: 0.6rem 2rem !important;
        font-family: 'Montserrat', sans-serif !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stDownloadButton > button[kind="primary"]:hover {
        background-color: #5fa836 !important;
        box-shadow: 0 4px 15px rgba(114, 191, 68, 0.4) !important;
        transform: translateY(-1px) !important;
    }

    /* ── Regular buttons ── */
    .stButton > button:not([kind="primary"]) {
        border: 2px solid #72BF44 !important;
        color: #72BF44 !important;
        background: transparent !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    /* ── Headers ── */
    h1 {
        color: #313638 !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px !important;
    }
    h2, h3 {
        color: #313638 !important;
        font-weight: 700 !important;
    }

    /* ── Success/Info alerts ── */
    .stSuccess {
        background-color: rgba(114, 191, 68, 0.1) !important;
        border-left: 4px solid #72BF44 !important;
    }
    .stInfo {
        background-color: rgba(15, 52, 96, 0.08) !important;
        border-left: 4px solid #0f3460 !important;
    }

    /* ── File uploader ── */
    .stFileUploader {
        border: 2px dashed #72BF44 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }

    /* ── Progress bars ── */
    .stProgress > div > div > div {
        background-color: #72BF44 !important;
    }

    /* ── Dataframe styling ── */
    .stDataFrame {
        border-radius: 8px !important;
        overflow: hidden !important;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        font-weight: 600 !important;
        color: #313638 !important;
    }

    /* ── Card-like containers ── */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 12px !important;
        border: 1px solid #e0e0e0 !important;
    }

    /* ── Radio buttons green ── */
    .stRadio > div[role="radiogroup"] > label > div:first-child {
        color: #72BF44 !important;
    }

    /* ── Selectbox ── */
    .stSelectbox [data-baseweb="select"] {
        border-radius: 8px !important;
    }

    /* ── Custom header banner ── */
    .renew-header {
        background: linear-gradient(135deg, #313638 0%, #1a1a2e 100%);
        padding: 1.5rem 2rem;
        border-radius: 0 0 16px 16px;
        margin: -1rem -1rem 2rem -1rem;
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    .renew-header img {
        height: 45px;
    }
    .renew-header .title {
        color: #ffffff;
        font-size: 1.6rem;
        font-weight: 700;
        letter-spacing: -0.3px;
    }
    .renew-header .subtitle {
        color: #72BF44;
        font-size: 0.9rem;
        font-weight: 500;
        margin-top: 2px;
    }

    /* ── Step cards ── */
    .step-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-left: 4px solid #72BF44;
    }
    .step-card h3 {
        margin-top: 0;
        color: #313638;
    }

    /* ── Stats row ── */
    .stat-box {
        background: white;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    .stat-box .number {
        font-size: 1.8rem;
        font-weight: 800;
        color: #72BF44;
    }
    .stat-box .label {
        font-size: 0.75rem;
        color: #666;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* ── Footer ── */
    .renew-footer {
        text-align: center;
        padding: 1.5rem;
        color: #999;
        font-size: 0.8rem;
        border-top: 1px solid #e0e0e0;
        margin-top: 3rem;
    }
    .renew-footer a {
        color: #72BF44;
        text-decoration: none;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ── Header Banner with Logo ──
st.markdown("""
<div class="renew-header">
    <img src="https://dg4e57nn4fnta.cloudfront.net/logos/ReNew.svg" alt="ReNew Logo" onerror="this.style.display='none'">
    <div>
        <div class="title">OCR Document Tracker</div>
        <div class="subtitle">Procurement PDF Data Extraction & Excel Tracker</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 1.5rem 0;">
        <img src="https://dg4e57nn4fnta.cloudfront.net/logos/ReNew.svg"
             width="140" alt="ReNew" onerror="this.style.display='none'">
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Configuration")

    # API Key from .env
    api_key_input = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key_input:
        st.error("API key not found in .env file.")
    else:
        st.success("API key loaded")

    model = st.selectbox(
        "LLM Model",
        options=OPENROUTER_MODELS,
        index=0,
        help="Model used to structure extracted text into tracker fields.",
    )

    st.markdown("---")
    st.markdown("### Case Selection")

    case_number = st.radio(
        "Select Case Type",
        options=[1, 2, 3],
        format_func=lambda x: f"Case {x}",
        help="Select the procurement case type matching your PDF.",
    )

    # Case description in a styled box
    st.info(CASE_DESCRIPTIONS[case_number])

    st.markdown("---")
    st.markdown(
        '<p style="text-align:center; font-size:0.7rem; color:#999;">'
        'Powered by EMB Global'
        '</p>',
        unsafe_allow_html=True,
    )

# ── Main Content Area ──
# Upload section
st.markdown("### Upload Document")
uploaded_file = st.file_uploader(
    "Upload PDF Document",
    type=["pdf"],
    help="Upload the procurement PDF for the selected case type.",
    label_visibility="collapsed",
)

if uploaded_file:
    file_size_mb = uploaded_file.size / 1024 / 1024
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div class="stat-box"><div class="number">PDF</div>'
            f'<div class="label">{uploaded_file.name}</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div class="stat-box"><div class="number">{file_size_mb:.1f} MB</div>'
            f'<div class="label">File Size</div></div>',
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f'<div class="stat-box"><div class="number">Case {case_number}</div>'
            f'<div class="label">Selected Type</div></div>',
            unsafe_allow_html=True,
        )

st.markdown("")

# Process button
if st.button("Process Document", type="primary", disabled=not (uploaded_file and api_key_input)):
    if not api_key_input:
        st.error("Please provide an OpenRouter API key in the `.env` file.")
        st.stop()
    if not uploaded_file:
        st.error("Please upload a PDF file.")
        st.stop()

    # Save uploaded file to temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    try:
        # ── Step 1: OCR Text Extraction ──
        st.markdown('<div class="step-card"><h3>Step 1 — OCR Text Extraction</h3>', unsafe_allow_html=True)
        page_count = get_page_count(tmp_path)
        st.write(f"PDF has **{page_count}** pages. Extracting text...")

        phase1_bar = st.progress(0, text="Phase 1: Extracting digital text...")

        def update_phase1(current, total):
            phase1_bar.progress(
                current / total,
                text=f"Phase 1: Extracting digital text — page {current}/{total}...",
            )

        phase2_placeholder = st.empty()
        phase2_bar = phase2_placeholder.progress(0, text="Phase 2: Waiting for scanned pages...")

        def update_phase2(current, total, page_num):
            phase2_bar.progress(
                current / total,
                text=f"Phase 2: OCR scanned page {current}/{total} (pg {page_num})...",
            )

        pages = extract_text_from_pdf(
            tmp_path,
            progress_callback=update_phase1,
            ocr_progress_callback=update_phase2,
        )
        phase1_bar.progress(1.0, text="Phase 1: Digital text extraction complete!")

        ocr_count = sum(1 for p in pages if p["method"] == "tesseract")
        if ocr_count > 0:
            phase2_bar.progress(1.0, text=f"Phase 2: OCR complete! ({ocr_count} scanned pages)")
        else:
            phase2_placeholder.empty()

        # Stats
        pymupdf_count = sum(1 for p in pages if p["method"] == "pymupdf")
        tesseract_count = sum(1 for p in pages if p["method"] == "tesseract")
        no_text_count = sum(1 for p in pages if p["method"] == "no_text")
        failed_count = sum(1 for p in pages if "failed" in p.get("method", ""))

        sc1, sc2, sc3, sc4 = st.columns(4)
        with sc1:
            st.metric("Digital Pages", pymupdf_count)
        with sc2:
            st.metric("OCR Pages", tesseract_count)
        with sc3:
            st.metric("Blank (Skipped)", no_text_count)
        with sc4:
            st.metric("Failed", failed_count)

        combined_text = get_combined_text(pages)
        if not combined_text.strip():
            st.error("No text could be extracted from the PDF.")
            st.stop()

        with st.expander("View extracted text (first 5000 chars)"):
            st.text(combined_text[:5000])

        st.markdown('</div>', unsafe_allow_html=True)

        # ── Step 2: LLM Structuring ──
        st.markdown('<div class="step-card"><h3>Step 2 — AI Data Extraction</h3>', unsafe_allow_html=True)
        with st.spinner(f"Sending to **{model}** via OpenRouter for structuring..."):
            extractor = DocumentExtractor(api_key=api_key_input, model=model)
            extracted = extractor.extract(combined_text, case_number)

        st.success("Data structured successfully!")

        with st.expander("View extracted JSON"):
            st.json(extracted)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Step 3: Map to Tracker ──
        st.markdown('<div class="step-card"><h3>Step 3 — Tracker Preview</h3>', unsafe_allow_html=True)
        rows = map_to_tracker(extracted, case_number)
        st.write(f"Generated **{len(rows)}** row(s) for the tracker.")

        col_map = COLUMN_MAPPINGS[case_number]
        inv_map = {v: k for k, v in col_map.items()}

        preview_data = []
        for row in rows:
            row_dict = {}
            for col_num, value in sorted(row.items()):
                field_name = inv_map.get(col_num, f"col_{col_num}")
                row_dict[field_name] = value
            preview_data.append(row_dict)

        df = pd.DataFrame(preview_data)
        st.dataframe(df, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Step 4: Download ──
        st.markdown('<div class="step-card"><h3>Step 4 — Download Tracker</h3>', unsafe_allow_html=True)
        excel_bytes = write_tracker(rows, case_number)

        st.download_button(
            label=f"Download {SHEET_NAMES[case_number]}.xlsx",
            data=excel_bytes,
            file_name=f"Filled_{SHEET_NAMES[case_number]}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
        )
        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error: {str(e)}")
        import traceback
        with st.expander("Error details"):
            st.code(traceback.format_exc())

    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass

# ── Footer ──
st.markdown("""
<div class="renew-footer">
    <a href="https://www.renew.com" target="_blank">ReNew</a> — OCR Document Tracker
    &nbsp;|&nbsp; Powering India's clean energy future
</div>
""", unsafe_allow_html=True)

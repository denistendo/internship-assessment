"""
Streamlit web application for Sunbird AI GenAI pipeline.
Redesigned with Sunbird AI branding and polished UI.
"""

import streamlit as st
import os
from backend.pipeline import ProcessingPipeline

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sunbird AI · Voice Pipeline",
    page_icon="🐦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #0D0F12 !important;
    color: #F0EDE6 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { background: #13161B !important; border-right: 1px solid #1E2228 !important; }
[data-testid="block-container"] { padding: 2rem 3rem 4rem !important; max-width: 1100px !important; }

/* ── Hero ── */
.hero {
    display: flex;
    align-items: center;
    gap: 18px;
    margin-bottom: 8px;
}
.hero-logo {
    width: 52px; height: 52px;
    background: linear-gradient(135deg, #F5A623 0%, #F76B1C 100%);
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 26px;
    flex-shrink: 0;
    box-shadow: 0 4px 20px rgba(245,166,35,0.35);
}
.hero-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 2.2rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
    line-height: 1.1;
    background: linear-gradient(90deg, #F5A623 0%, #FFFFFF 60%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 !important;
}
.hero-sub {
    font-size: 0.95rem;
    color: #8A8F9A;
    margin: 0 0 0 70px;
    letter-spacing: 0.01em;
}

/* ── Pipeline steps strip ── */
.pipeline-strip {
    display: flex;
    align-items: center;
    gap: 0;
    background: #13161B;
    border: 1px solid #1E2228;
    border-radius: 14px;
    padding: 14px 20px;
    margin: 24px 0 32px;
    overflow-x: auto;
}
.pipe-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    flex: 1;
    min-width: 70px;
}
.pipe-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    background: #1A1D24;
    border: 1px solid #2A2E38;
    display: flex; align-items: center; justify-content: center;
    font-size: 17px;
}
.pipe-label {
    font-size: 0.68rem;
    color: #6B7280;
    text-align: center;
    font-weight: 500;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.pipe-arrow {
    color: #2A2E38;
    font-size: 18px;
    margin: 0 2px;
    flex-shrink: 0;
    padding-bottom: 18px;
}

/* ── Section labels ── */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #F5A623;
    margin-bottom: 10px;
}

/* ── Cards ── */
.card {
    background: #13161B;
    border: 1px solid #1E2228;
    border-radius: 16px;
    padding: 20px 22px;
    margin-bottom: 16px;
    transition: border-color 0.2s;
}
.card:hover { border-color: #2E3340; }

/* ── Input toggle pills ── */
[data-testid="stRadio"] > div {
    display: flex !important;
    gap: 10px !important;
    flex-direction: row !important;
}
[data-testid="stRadio"] label {
    background: #1A1D24 !important;
    border: 1px solid #2A2E38 !important;
    border-radius: 50px !important;
    padding: 7px 20px !important;
    cursor: pointer !important;
    font-size: 0.88rem !important;
    color: #9CA3AF !important;
    transition: all 0.18s !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stRadio"] label:has(input:checked) {
    background: linear-gradient(135deg, #F5A623, #F76B1C) !important;
    border-color: transparent !important;
    color: #fff !important;
    font-weight: 500 !important;
    box-shadow: 0 2px 12px rgba(245,166,35,0.3) !important;
}
[data-testid="stRadio"] label input { display: none !important; }
[data-testid="stRadio"] > label { display: none !important; }

/* ── Text area ── */
[data-testid="stTextArea"] textarea {
    background: #0D0F12 !important;
    border: 1px solid #2A2E38 !important;
    border-radius: 12px !important;
    color: #F0EDE6 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.93rem !important;
    resize: vertical !important;
    transition: border-color 0.2s !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: #F5A623 !important;
    box-shadow: 0 0 0 3px rgba(245,166,35,0.12) !important;
}
[data-testid="stTextArea"] label { color: #6B7280 !important; font-size: 0.82rem !important; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #0D0F12 !important;
    border: 1px dashed #2A2E38 !important;
    border-radius: 12px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"]:hover { border-color: #F5A623 !important; }
[data-testid="stFileUploader"] label { color: #9CA3AF !important; }

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: #1A1D24 !important;
    border: 1px solid #2A2E38 !important;
    border-radius: 10px !important;
    color: #F0EDE6 !important;
}
[data-testid="stSelectbox"] label { color: #6B7280 !important; font-size: 0.82rem !important; }

/* ── Primary button ── */
[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #F5A623 0%, #F76B1C 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.03em !important;
    padding: 14px 0 !important;
    box-shadow: 0 4px 20px rgba(245,166,35,0.3) !important;
    transition: all 0.2s !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 28px rgba(245,166,35,0.45) !important;
}
[data-testid="stButton"] > button[kind="primary"]:active { transform: translateY(0) !important; }

/* ── Result tabs ── */
[data-testid="stTabs"] [data-testid="stTab"] {
    background: transparent !important;
    border: 1px solid #1E2228 !important;
    border-radius: 8px !important;
    color: #6B7280 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    padding: 7px 16px !important;
    margin-right: 6px !important;
    transition: all 0.18s !important;
}
[data-testid="stTabs"] [data-testid="stTab"][aria-selected="true"] {
    background: #1A1D24 !important;
    border-color: #F5A623 !important;
    color: #F5A623 !important;
    font-weight: 600 !important;
}
[data-testid="stTabPanel"] {
    background: #13161B !important;
    border: 1px solid #1E2228 !important;
    border-radius: 0 12px 12px 12px !important;
    padding: 20px !important;
}

/* ── Result text blocks ── */
.result-text {
    background: #0D0F12;
    border-left: 3px solid #F5A623;
    border-radius: 0 8px 8px 0;
    padding: 14px 16px;
    font-size: 0.93rem;
    line-height: 1.65;
    color: #D1CBBC;
    margin-top: 8px;
}

/* ── Status messages ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] p { color: #F5A623 !important; font-family: 'DM Sans', sans-serif !important; }

/* ── Divider ── */
hr { border-color: #1E2228 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0D0F12; }
::-webkit-scrollbar-thumb { background: #2A2E38; border-radius: 3px; }

/* ── Caption / small text ── */
[data-testid="stCaptionContainer"] { color: #6B7280 !important; font-size: 0.8rem !important; }

/* ── Success/info badges ── */
.badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(245,166,35,0.1);
    border: 1px solid rgba(245,166,35,0.25);
    color: #F5A623;
    border-radius: 50px;
    padding: 4px 12px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.02em;
}
</style>
""", unsafe_allow_html=True)


# ── Pipeline init ─────────────────────────────────────────────────────────────
@st.cache_resource
def get_pipeline():
    try:
        return ProcessingPipeline()
    except ValueError as e:
        st.error(f"Configuration error: {e}. Set `SUNBIRD_API_TOKEN` in your `.env` file.")
        return None


pipeline = get_pipeline()

# ── Hero header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-logo">🐦</div>
    <div class="hero-title">Sunbird AI</div>
</div>
<p class="hero-sub">Speech · Summarisation · Translation · Synthesis — all in one pipeline</p>
""", unsafe_allow_html=True)

# ── Pipeline strip ────────────────────────────────────────────────────────────
st.markdown("""
<div class="pipeline-strip">
    <div class="pipe-step">
        <div class="pipe-icon">📥</div>
        <div class="pipe-label">Input</div>
    </div>
    <div class="pipe-arrow">›</div>
    <div class="pipe-step">
        <div class="pipe-icon">🎙️</div>
        <div class="pipe-label">Transcribe</div>
    </div>
    <div class="pipe-arrow">›</div>
    <div class="pipe-step">
        <div class="pipe-icon">✂️</div>
        <div class="pipe-label">Summarise</div>
    </div>
    <div class="pipe-arrow">›</div>
    <div class="pipe-step">
        <div class="pipe-icon">🌍</div>
        <div class="pipe-label">Translate</div>
    </div>
    <div class="pipe-arrow">›</div>
    <div class="pipe-step">
        <div class="pipe-icon">🔊</div>
        <div class="pipe-label">Synthesise</div>
    </div>
    <div class="pipe-arrow">›</div>
    <div class="pipe-step">
        <div class="pipe-icon">🎧</div>
        <div class="pipe-label">Output</div>
    </div>
</div>
""", unsafe_allow_html=True)

if pipeline is None:
    st.stop()

# ── Layout: left input / right settings ──────────────────────────────────────
left, right = st.columns([3, 1], gap="large")

with left:
    st.markdown('<div class="section-label">01 — Input</div>', unsafe_allow_html=True)

    input_type = st.radio(
        "Input mode",
        options=["📄 Text", "🎙️ Audio File"],
        horizontal=True,
        label_visibility="collapsed",
    )

    input_data = None

    if input_type == "📄 Text":
        input_data = st.text_area(
            "Your text",
            placeholder="Type or paste any text here to summarise and translate…",
            height=160,
            label_visibility="collapsed",
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload audio (MP3 · WAV · M4A · OGG · FLAC, max 5 min)",
            type=["mp3", "wav", "m4a", "ogg", "flac"],
            label_visibility="visible",
        )

        if uploaded_file is not None:
            temp_audio_path = f"temp_{uploaded_file.name}"
            with open(temp_audio_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            file_size_mb = os.path.getsize(temp_audio_path) / (1024 * 1024)

            if file_size_mb > 50:          # ~5 min ≈ 5-50 MB depending on format
                st.error("Audio exceeds the 5-minute limit. Please upload a shorter clip.")
                os.remove(temp_audio_path)
            else:
                st.caption(f"✓  {uploaded_file.name} · {file_size_mb:.1f} MB")
                input_data = temp_audio_path

with right:
    st.markdown('<div class="section-label">02 — Language</div>', unsafe_allow_html=True)
    supported_langs = list(ProcessingPipeline.get_supported_languages().keys())
    target_language = st.selectbox(
        "Translate to",
        supported_langs,
        label_visibility="collapsed",
    )
    st.markdown(f'<div class="badge">🌍 {target_language}</div>', unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)

# ── Run button ────────────────────────────────────────────────────────────────
run = st.button("Run Pipeline →", type="primary", use_container_width=True)

# ── Processing & results ──────────────────────────────────────────────────────
if run:
    if not input_data:
        st.error("Please provide some input — paste text or upload an audio file.")
    else:
        with st.spinner("Processing through Sunbird AI…"):
            input_type_key = "audio" if input_type == "🎙️ Audio File" else "text"
            results = pipeline.run_full_pipeline(
                input_type=input_type_key,
                input_data=input_data,
                target_language=target_language,
            )

        if results["success"]:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-label">03 — Results</div>', unsafe_allow_html=True)

            tabs = st.tabs(["Original", "Transcript", "Summary", "Translation", "Audio"])

            with tabs[0]:
                st.markdown(f'<div class="result-text">{results["original_text"]}</div>', unsafe_allow_html=True)

            with tabs[1]:
                if input_type_key == "audio" and results.get("transcript"):
                    st.markdown(f'<div class="result-text">{results["transcript"]}</div>', unsafe_allow_html=True)
                else:
                    st.caption("No transcription — text input was used directly.")

            with tabs[2]:
                st.markdown(f'<div class="result-text">{results["summary"]}</div>', unsafe_allow_html=True)

            with tabs[3]:
                st.markdown(f'<div class="result-text">{results["translation"]}</div>', unsafe_allow_html=True)

            with tabs[4]:
                if results.get("audio_file") and os.path.exists(results["audio_file"]):
                    with open(results["audio_file"], "rb") as af:
                        st.audio(af.read(), format="audio/mp3")
                else:
                    st.warning("Audio synthesis did not return a file.")

        else:
            st.error("Pipeline failed. See details below.")
            for err in results.get("errors", []):
                st.caption(f"• {err}")

        # Cleanup temp file
        if input_type == "🎙️ Audio File" and input_data and os.path.exists(input_data):
            try:
                os.remove(input_data)
            except Exception:
                pass

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#2A2E38; font-size:0.78rem; font-family:'DM Sans',sans-serif; letter-spacing:0.05em;">
    SUNBIRD AI &nbsp;·&nbsp; VOICE PIPELINE &nbsp;·&nbsp;
    <a href="https://docs.sunbird.ai" style="color:#F5A623; text-decoration:none;">DOCS</a>
    &nbsp;·&nbsp;
    <a href="https://sunbird.ai" style="color:#F5A623; text-decoration:none;">SUNBIRD.AI</a>
</div>
""", unsafe_allow_html=True)
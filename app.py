import streamlit as st
import os
import base64
from backend.pipeline import ProcessingPipeline
from dotenv import load_dotenv

load_dotenv()

# Page config
st.set_page_config(
    page_title="Sunbird Echo AI",
    page_icon="🐦",
    layout="wide"
)

# Initialize Session State
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "results" not in st.session_state:
    st.session_state.results = None

def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

def clear_results():
    st.session_state.results = None

# Custom CSS for the beautiful UI & Animations
css_base = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

/* HIDE STREAMLIT HEADER/FOOTER (Removes Deploy Button) */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

html, body, [class*="st-"] {
    font-family: 'Nunito', sans-serif;
}

/* Animations */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
.animated {
    animation: fadeInUp 0.6s ease-out forwards;
}

/* Header Area */
.custom-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0 30px 0;
}
.logo-title-group {
    display: flex;
    align-items: center;
    gap: 15px;
}
.header-logo {
    width: 40px;
}
.header-text {
    display: flex;
    flex-direction: column;
}
.header-title {
    font-size: 1.4rem;
    font-weight: 800;
    color: var(--text-color);
    margin: 0;
    line-height: 1.1;
}
.header-subtitle {
    font-size: 0.9rem;
    color: var(--text-muted);
    margin: 0;
}

/* Hero Section */
.hero-title {
    font-size: 3.5rem;
    font-weight: 800;
    color: var(--text-color);
    line-height: 1.1;
    margin-bottom: 20px;
    text-align: center;
}
.hero-title span {
    color: #D97706; /* Amber */
}
.hero-subtitle {
    font-size: 1.2rem;
    color: var(--text-muted);
    text-align: center;
    max-width: 600px;
    margin: 0 auto 40px auto;
}

/* Tags */
.tags-container {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    justify-content: center;
    margin-bottom: 50px;
}
.tag {
    background: var(--tag-bg);
    color: var(--tag-text);
    padding: 8px 18px;
    border-radius: 50px;
    font-weight: 600;
    font-size: 0.95rem;
    display: flex;
    align-items: center;
    gap: 8px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.tag:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(217, 119, 6, 0.15);
}

/* Cards & System Overview */
.system-card {
    background: var(--card-bg);
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.03);
    border: 1px solid var(--card-border);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.system-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.06);
}

.step-row {
    display: flex;
    align-items: flex-start;
    gap: 15px;
    margin-bottom: 20px;
}
.step-number {
    background: var(--step-bg);
    color: #D97706;
    font-weight: 800;
    width: 35px;
    height: 35px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    flex-shrink: 0;
}
.step-text {
    color: var(--text-muted);
    font-size: 0.95rem;
}
.step-text b {
    color: var(--text-color);
    font-size: 1.05rem;
}

/* Segmented Control / Radio Styling */
div[role="radiogroup"] {
    background: var(--radio-bg) !important;
    border-radius: 50px !important;
    padding: 5px !important;
    gap: 0 !important;
}
div[role="radiogroup"] > label {
    border-radius: 40px !important;
    padding: 10px 30px !important;
    margin: 0 !important;
    background: transparent !important;
    border: none !important;
}
div[role="radiogroup"] > label[data-checked="true"] {
    background: var(--card-bg) !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
}
div[role="radiogroup"] > label[data-checked="true"] p {
    color: var(--text-color) !important;
}

/* File uploader hover */
[data-testid="stFileUploader"] {
    background: transparent !important;
    border: 1px dashed var(--card-border) !important;
    border-radius: 15px !important;
    padding: 20px !important;
    transition: border-color 0.2s ease;
}
[data-testid="stFileUploader"]:hover {
    border-color: #D97706 !important;
}

/* Custom button overrides */
[data-testid="baseButton-primary"] {
    border-radius: 12px !important;
    font-weight: 700 !important;
    padding: 10px 20px !important;
    box-shadow: 0 4px 15px rgba(242, 169, 80, 0.4) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}
[data-testid="baseButton-primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(242, 169, 80, 0.6) !important;
}
[data-testid="baseButton-secondary"] {
    border-radius: 12px !important;
}

/* Result Cards inside Tabs */
.result-box {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    padding: 20px;
    border-radius: 15px;
    color: var(--text-color);
    font-size: 1.05rem;
}
</style>
"""

# Variables injection depending on Theme state
if st.session_state.dark_mode:
    css_theme = """
    <style>
    :root {
        --text-color: #EAEAEA;
        --text-muted: #A39B92;
        --card-bg: #1A1A1A;
        --card-border: #333333;
        --tag-bg: #2C1E0F;
        --tag-text: #F2A950;
        --step-bg: #2C1E0F;
        --radio-bg: #111111;
    }
    .stApp {
        background-color: #0F0F0F !important;
    }
    p, span, div, label {
        color: var(--text-muted);
    }
    </style>
    """
else:
    css_theme = """
    <style>
    :root {
        --text-color: #3A2311;
        --text-muted: #6B5B4C;
        --card-bg: #FFFFFF;
        --card-border: #F0E8D9;
        --tag-bg: #F4E9D8;
        --tag-text: #784A1C;
        --step-bg: #FDF8EF;
        --radio-bg: #F4E9D8;
    }
    .stApp {
        background-color: #FDF8EF !important;
    }
    </style>
    """

st.markdown(css_base + css_theme, unsafe_allow_html=True)

# Helper function to load logo
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

logo_base64 = get_base64_image("logo.png")
logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="header-logo">' if logo_base64 else '<span style="font-size:30px;">🐦</span>'

# Render Custom Header
col_logo, col_theme = st.columns([5, 1])
with col_logo:
    st.markdown(f"""
    <div class="custom-header animated">
        <div class="logo-title-group">
            {logo_html}
            <div class="header-text">
                <div class="header-title">Sunbird Echo AI</div>
                <div class="header-subtitle">Voicing Uganda's languages</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
with col_theme:
    st.markdown("<br>", unsafe_allow_html=True)
    theme_label = "☀️ Light Mode" if st.session_state.dark_mode else "🌙 Dark Mode"
    st.button(theme_label, on_click=toggle_dark_mode, use_container_width=True)


# Main layout logic
@st.cache_resource
def get_pipeline():
    try:
        return ProcessingPipeline()
    except Exception:
        return None

pipeline = get_pipeline()
api_token = os.getenv("SUNBIRD_API_TOKEN")

if not api_token or pipeline is None:
    st.error("⚠️ **Missing Sunbird API Token**")
    st.warning("Please configure your `.env` file with `SUNBIRD_API_TOKEN` and restart the application.")
    st.stop()


# Two-column layout
col_left, col_right = st.columns([1.1, 1], gap="large")

with col_left:
    st.markdown("""
    <div class="hero-title animated" style="animation-delay: 0.1s;">Transform Content into<br><span>Natural Speech</span></div>
    <div class="hero-subtitle animated" style="animation-delay: 0.2s;">An intelligent workspace for converting, translating, summarizing, and voicing content with a smooth modern experience.</div>
    <div class="tags-container animated" style="animation-delay: 0.3s;">
        <div class="tag">✨ Modern theme</div>
        <div class="tag">✨ 5+ regional dialects</div>
        <div class="tag">✨ Authentic AI voices</div>
        <div class="tag">✨ Instant responses</div>
        <div class="tag">✨ Quick processing</div>
        <div class="tag">✨ Seamless text-to-audio</div>
    </div>
    """, unsafe_allow_html=True)
    
    # DYNAMIC RENDER: If results exist, show results here instead of system overview
    if st.session_state.results is not None:
        st.markdown("<h3 class='animated' style='color: var(--text-color);'>Processing Results</h3>", unsafe_allow_html=True)
        results = st.session_state.results
        
        if results["success"]:
            tabs = st.tabs(["Original", "Transcript", "Summary", "Translation", "Audio"])
            
            with tabs[0]:
                st.markdown(f"<div class='result-box animated'>{results['original_text']}</div>", unsafe_allow_html=True)
            with tabs[1]:
                if results.get("transcript"):
                    st.markdown(f"<div class='result-box animated'>{results['transcript']}</div>", unsafe_allow_html=True)
                else:
                    st.info("No transcription needed for text input.")
            with tabs[2]:
                if results.get("summary"):
                    st.markdown(f"<div class='result-box animated'>{results['summary']}</div>", unsafe_allow_html=True)
                else:
                    st.info("Input was too short to require a summary.")
            with tabs[3]:
                st.markdown(f"<div class='result-box animated'>{results['translation']}</div>", unsafe_allow_html=True)
            with tabs[4]:
                if results.get("audio_file") and os.path.exists(results["audio_file"]):
                    st.markdown("<div class='result-box animated' style='padding-bottom: 5px;'>", unsafe_allow_html=True)
                    with open(results["audio_file"], "rb") as af:
                        st.audio(af.read(), format="audio/mp3")
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.warning("No audio file generated.")
                    
            st.markdown("<br>", unsafe_allow_html=True)
            st.button("↺ Start New Processing", on_click=clear_results)
            
        else:
            st.error("Pipeline failed.")
            for err in results.get("errors", []):
                st.write(f"- {err}")
            st.button("↺ Try Again", on_click=clear_results)
            
    else:
        # Show System Overview
        st.markdown("""
        <div class="system-card animated" style="animation-delay: 0.4s;">
            <h3 style="margin-top:0;">System Overview</h3>
            <div class="step-row">
                <div class="step-number">01</div>
                <div class="step-text"><b>Select Input Type</b><br>Choose Text for typed content or Voice for recorded speech.</div>
            </div>
            <div class="step-row">
                <div class="step-number">02</div>
                <div class="step-text"><b>Choose Output Language</b><br>Pick the language for the final translation and speech.</div>
            </div>
            <div class="step-row">
                <div class="step-number">03</div>
                <div class="step-text"><b>Upload or Enter Content</b><br>Type your text or upload an audio recording.</div>
            </div>
            <div class="step-row">
                <div class="step-number">04</div>
                <div class="step-text"><b>Inspect AI Results</b><br>View transcripts, summaries, translations, and timing.</div>
            </div>
            <div class="step-row" style="margin-bottom:0;">
                <div class="step-number">05</div>
                <div class="step-text"><b>Listen to Final Speech</b><br>Play the produced audio and confirm the quality.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_right:
    st.markdown("<div class='system-card animated' style='animation-delay: 0.5s;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0; color: var(--text-color);'>Content Input</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.8rem; font-weight: 700; color: #8C7C6D; letter-spacing: 1px; text-transform: uppercase;'>Input Options</p>", unsafe_allow_html=True)
    
    input_type = st.radio("Input Options", ["Text", "Voice"], horizontal=True, label_visibility="collapsed")
    
    input_data = None
    
    if input_type == "Text":
        input_data = st.text_area("Type your text here", placeholder="Enter your content...", height=150)
    else:
        st.markdown("<p style='margin-top: 15px; font-weight: 600; color: var(--text-color);'>Upload Audio</p>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload an audio recording", type=["mp3", "wav", "m4a", "ogg", "flac"], label_visibility="collapsed")
        if uploaded_file is not None:
            temp_audio_path = f"temp_{uploaded_file.name}"
            with open(temp_audio_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            file_size_mb = os.path.getsize(temp_audio_path) / (1024 * 1024)
            if file_size_mb > 50:
                st.error("Audio exceeds 5-minute limit.")
                os.remove(temp_audio_path)
            else:
                input_data = temp_audio_path
                st.success(f"Audio ready ({file_size_mb:.1f} MB)")

    st.markdown("<br><p style='font-size: 0.8rem; font-weight: 700; color: #8C7C6D; letter-spacing: 1px; text-transform: uppercase;'>Output Language</p>", unsafe_allow_html=True)
    supported_langs = list(ProcessingPipeline.get_supported_languages().keys())
    target_language = st.selectbox("Choose a preferred language", supported_langs, label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Process Button
    if st.button("✨ Start Processing", type="primary", use_container_width=True):
        if not input_data:
            st.error("Please provide an input (text or audio).")
        else:
            with st.spinner("Processing through Sunbird AI..."):
                input_type_key = "audio" if input_type == "Voice" else "text"
                results = pipeline.run_full_pipeline(
                    input_type=input_type_key,
                    input_data=input_data,
                    target_language=target_language
                )
                
                # Cleanup audio
                if input_type == "Voice" and input_data and os.path.exists(input_data):
                    try:
                        os.remove(input_data)
                    except Exception:
                        pass
                
                # Save results to session state and trigger rerun
                st.session_state.results = results
                st.rerun()
                
    st.markdown("</div>", unsafe_allow_html=True)
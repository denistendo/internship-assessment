import streamlit as st
import os
from backend.pipeline import ProcessingPipeline
from dotenv import load_dotenv

# Load environment variables just in case
load_dotenv()

# Page config
st.set_page_config(
    page_title="Sunbird AI Voice Pipeline",
    page_icon="🐦",
    layout="centered"
)

# Header
st.title("🐦 Sunbird AI Pipeline")
st.markdown("Speech · Summarisation · Translation · Synthesis — all in one pipeline.")

@st.cache_resource
def get_pipeline():
    try:
        return ProcessingPipeline()
    except Exception:
        return None

pipeline = get_pipeline()

# Check for API token
api_token = os.getenv("SUNBIRD_API_TOKEN")

if not api_token or pipeline is None:
    st.error("⚠️ **Missing Sunbird API Token**")
    st.warning("Please sign up at [api.sunbird.ai](https://api.sunbird.ai/), obtain a token, and add it to your `.env` file as `SUNBIRD_API_TOKEN=your_token_here`. Once added, restart the app.")
    st.stop()

st.divider()

# Input Section
st.header("1. Input")
input_type = st.radio("Choose input method:", ["Text", "Audio File"], horizontal=True)

input_data = None

if input_type == "Text":
    input_data = st.text_area("Enter text to summarize and translate:", height=150)
else:
    uploaded_file = st.file_uploader("Upload audio (MP3, WAV, M4A, OGG, FLAC) - Max 5 min", type=["audio/mp3", "audio/wav", "audio/m4a", "audio/ogg", "audio/flac", "audio/mpeg"])
    if uploaded_file is not None:
        # Save temp file
        temp_audio_path = f"temp_{uploaded_file.name}"
        with open(temp_audio_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        file_size_mb = os.path.getsize(temp_audio_path) / (1024 * 1024)
        if file_size_mb > 50:
            st.error("Audio exceeds the 5-minute limit (~50MB). Please upload a shorter clip.")
            os.remove(temp_audio_path)
        else:
            st.success(f"Audio uploaded successfully ({file_size_mb:.1f} MB)")
            input_data = temp_audio_path

# Settings Section
st.header("2. Language Settings")
supported_langs = list(ProcessingPipeline.get_supported_languages().keys())
target_language = st.selectbox("Select target language for translation:", supported_langs)

st.markdown("<br>", unsafe_allow_html=True)

# Run Pipeline
if st.button("Run Pipeline", type="primary", use_container_width=True):
    if not input_data:
        st.error("Please provide an input (text or upload an audio file).")
    else:
        with st.spinner("Processing your input through Sunbird AI..."):
            input_type_key = "audio" if input_type == "Audio File" else "text"
            results = pipeline.run_full_pipeline(
                input_type=input_type_key,
                input_data=input_data,
                target_language=target_language
            )

        if results["success"]:
            st.success("Pipeline completed successfully!")
            
            st.header("3. Results")
            tabs = st.tabs(["Original", "Transcript", "Summary", "Translation", "Audio"])
            
            with tabs[0]:
                st.write(results["original_text"])
                
            with tabs[1]:
                if input_type_key == "audio" and results.get("transcript"):
                    st.write(results["transcript"])
                else:
                    st.info("No transcription generated (Text input was used).")
                    
            with tabs[2]:
                st.write(results["summary"])
                
            with tabs[3]:
                st.write(results["translation"])
                
            with tabs[4]:
                if results.get("audio_file") and os.path.exists(results["audio_file"]):
                    with open(results["audio_file"], "rb") as af:
                        st.audio(af.read(), format="audio/mp3")
                else:
                    st.warning("No audio file was generated.")
        else:
            st.error("Pipeline failed. Please check the errors below.")
            for err in results.get("errors", []):
                st.write(f"- {err}")

        # Cleanup temporary audio files
        if input_type == "Audio File" and input_data and os.path.exists(input_data):
            try:
                os.remove(input_data)
            except Exception:
                pass
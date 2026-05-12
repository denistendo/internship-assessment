"""
Streamlit web application for Sunbird AI GenAI pipeline.

Provides UI for:
- Text/audio input switching
- Audio upload with 5-minute constraint
- Language selection for translation
- Display of intermediate and final results
"""

import streamlit as st
import os
from pathlib import Path
from backend.pipeline import ProcessingPipeline


# Page configuration
st.set_page_config(
    page_title="Sunbird AI GenAI App",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .step-header {
        color: #ff7f0e;
        font-size: 1.3em;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize pipeline
@st.cache_resource
def get_pipeline():
    """Get or create pipeline instance."""
    try:
        return ProcessingPipeline()
    except ValueError as e:
        st.error(f"❌ Configuration Error: {str(e)}")
        st.info("Please ensure `SUNBIRD_API_TOKEN` is set in your `.env` file.")
        return None


# Main UI
st.markdown('<div class="main-header">🎤 Sunbird AI GenAI Application</div>', unsafe_allow_html=True)
st.write("""
This application processes your input through a powerful AI pipeline:
1. **Input** — Provide text or upload audio
2. **Transcribe** — Convert audio to text (if needed)
3. **Summarize** — Extract key information
4. **Translate** — Convert to your chosen Ugandan local language
5. **Synthesize** — Generate audio of the translation
""")

st.divider()

# Check if pipeline is initialized
pipeline = get_pipeline()
if pipeline is None:
    st.stop()

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Language selection
    supported_langs = list(ProcessingPipeline.get_supported_languages().keys())
    target_language = st.selectbox(
        "🌍 Select translation language:",
        supported_langs,
        help="Choose the Ugandan local language for translation"
    )
    
    st.divider()
    st.info("""
    **About this app:**
    - Uses Sunbird AI APIs for all processing
    - Supports up to 5-minute audio files
    - Powered by Sunflower LLM
    """)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="step-header">📝 Step 1: Choose Your Input</div>', unsafe_allow_html=True)
    
    input_type = st.radio(
        "How would you like to provide input?",
        options=["📄 Text", "🎙️ Audio File"],
        horizontal=True,
        help="Choose between typing text or uploading an audio file"
    )
    
    input_data = None
    
    if input_type == "📄 Text":
        input_data = st.text_area(
            "Enter your text:",
            placeholder="Type or paste your text here...",
            height=150,
            help="The text you want to summarize and translate"
        )
    else:  # Audio File
        uploaded_file = st.file_uploader(
            "Upload audio file (max 5 minutes):",
            type=["mp3", "wav", "m4a", "ogg", "flac"],
            help="Supported formats: MP3, WAV, M4A, OGG, FLAC"
        )
        
        if uploaded_file is not None:
            # Save uploaded file temporarily
            temp_audio_path = f"temp_{uploaded_file.name}"
            with open(temp_audio_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Check file size
            file_size_mb = os.path.getsize(temp_audio_path) / (1024 * 1024)
            st.caption(f"📊 File size: {file_size_mb:.2f} MB")
            
            if file_size_mb > 5:
                st.error("❌ Audio file exceeds 5-minute limit (~5 MB). Please upload a shorter audio file.")
                os.remove(temp_audio_path)
                input_data = None
            else:
                input_data = temp_audio_path
                st.success("✅ Audio file ready for processing")

with col2:
    st.markdown('<div class="step-header">🎯 Target Language</div>', unsafe_allow_html=True)
    st.info(f"**Selected:** {target_language}")

st.divider()

# Process button
if st.button("🚀 Process", type="primary", use_container_width=True):
    if not input_data:
        st.error("❌ Please provide input (text or audio file)")
    else:
        # Show processing status
        with st.spinner("⏳ Processing your input..."):
            input_type_key = "audio" if input_type == "🎙️ Audio File" else "text"
            results = pipeline.run_full_pipeline(
                input_type=input_type_key,
                input_data=input_data,
                target_language=target_language
            )
        
        # Display results
        if results["success"]:
            st.success("✅ Processing complete!")
            st.divider()
            
            # Results tabs
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📝 Original",
                "🎙️ Transcript" if input_type == "🎙️ Audio File" else "ℹ️ Info",
                "✂️ Summary",
                "🌍 Translation",
                "🔊 Audio"
            ])
            
            with tab1:
                st.markdown("**Original Text:**")
                st.write(results["original_text"])
            
            with tab2:
                if input_type == "🎙️ Audio File" and results["transcript"]:
                    st.markdown("**Transcript from audio:**")
                    st.write(results["transcript"])
                else:
                    st.info("Processed text input (no transcription needed)")
            
            with tab3:
                st.markdown("**Summary:**")
                st.write(results["summary"])
            
            with tab4:
                st.markdown(f"**Translation to {target_language}:**")
                st.write(results["translation"])
            
            with tab5:
                if results["audio_file"] and os.path.exists(results["audio_file"]):
                    st.markdown("**Generated Audio (Translated Summary):**")
                    with open(results["audio_file"], "rb") as audio_file:
                        st.audio(audio_file.read(), format="audio/mp3")
                else:
                    st.error("❌ Audio file could not be generated")
        
        else:
            # Show errors
            st.error("❌ Processing failed. Please check the errors below:")
            for error in results["errors"]:
                st.warning(f"• {error}")
        
        # Cleanup temporary audio file
        if input_type == "🎙️ Audio File" and input_data and os.path.exists(input_data):
            try:
                os.remove(input_data)
            except:
                pass

st.divider()

# Footer
st.markdown("""
---
**Made with ❤️ using Streamlit and Sunbird AI**
[📖 Documentation](https://docs.sunbird.ai) | [🌐 Sunbird AI](https://sunbird.ai)
""")

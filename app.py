import streamlit as st
import os
import base64
from backend.pipeline import ProcessingPipeline
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Sunbird Echo AI",
    page_icon="🐦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── Session State ─────────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "results" not in st.session_state:
    st.session_state.results = None

def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

def clear_results():
    st.session_state.results = None

# ── Theme ─────────────────────────────────────────────────────────────────────
if st.session_state.dark_mode:
    bg         = "#0E0C0A"
    surface    = "#1C1814"
    surface2   = "#252118"
    border     = "#352F27"
    text_c     = "#F0EAE0"
    muted      = "#9A8F82"
    accent     = "#F2A950"
    accent_dim = "#2C1E0F"
    success_bg = "#0C1E10"
    success_fg = "#4ADE80"
    error_bg   = "#1E0C0C"
    error_fg   = "#F87171"
    info_bg    = "#0C141E"
    info_fg    = "#60A5FA"
    shadow     = "rgba(0,0,0,0.4)"
else:
    bg         = "#FAF7F2"
    surface    = "#FFFFFF"
    surface2   = "#F5F0E8"
    border     = "#E8DDD0"
    text_c     = "#2C1E0F"
    muted      = "#7A6A5A"
    accent     = "#D97706"
    accent_dim = "#FEF3C7"
    success_bg = "#F0FDF4"
    success_fg = "#15803D"
    error_bg   = "#FEF2F2"
    error_fg   = "#DC2626"
    info_bg    = "#EFF6FF"
    info_fg    = "#2563EB"
    shadow     = "rgba(0,0,0,0.06)"

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

#MainMenu, header, footer {{ visibility: hidden; }}
html, body, [class*="st-"] {{ font-family: 'Sora', sans-serif !important; box-sizing: border-box; }}
.stApp {{ background-color: {bg} !important; }}

@keyframes fadeUp {{
  from {{ opacity: 0; transform: translateY(14px); }}
  to   {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes pulseGlow {{
  0%,100% {{ box-shadow: 0 4px 16px rgba(217,119,6,.3); }}
  50%      {{ box-shadow: 0 4px 28px rgba(217,119,6,.6); }}
}}
.fu  {{ animation: fadeUp .5s cubic-bezier(.22,.68,0,1.2) both; }}
.fu1 {{ animation-delay:.04s; }}
.fu2 {{ animation-delay:.10s; }}
.fu3 {{ animation-delay:.17s; }}
.fu4 {{ animation-delay:.24s; }}
.fu5 {{ animation-delay:.31s; }}

.block-container {{ max-width:740px !important; padding:32px 20px 80px 20px !important; }}

/* Header */
.top-bar {{
  display:flex; align-items:center; justify-content:space-between;
  padding-bottom:24px; border-bottom:1px solid {border}; margin-bottom:36px;
}}
.brand {{ display:flex; align-items:center; gap:10px; }}
.brand-icon {{
  width:34px; height:34px;
  background:linear-gradient(135deg,{accent},#FBBF24);
  border-radius:8px; display:flex; align-items:center; justify-content:center;
  font-size:16px; box-shadow:0 3px 10px rgba(217,119,6,.3); flex-shrink:0;
}}
.brand-name {{ font-size:1rem; font-weight:700; color:{text_c}; letter-spacing:-.2px; line-height:1.1; }}
.brand-sub  {{ font-size:0.7rem; color:{muted}; }}
.pill-row {{ display:flex; gap:5px; }}
.pill {{
  background:{accent_dim}; color:{accent};
  font-size:0.6rem; font-weight:700;
  padding:3px 8px; border-radius:100px;
  letter-spacing:.5px; text-transform:uppercase;
}}

/* Hero */
.hero {{ margin-bottom:32px; }}
.eyebrow {{
  display:inline-flex; align-items:center; gap:5px;
  font-size:0.62rem; font-weight:700; letter-spacing:1.5px; text-transform:uppercase;
  color:{accent}; background:{accent_dim};
  padding:4px 10px; border-radius:100px; margin-bottom:12px;
}}
.hero-h {{
  font-size:2.1rem; font-weight:800; color:{text_c};
  line-height:1.1; letter-spacing:-1px; margin-bottom:10px;
}}
.hero-h em {{ font-style:normal; color:{accent}; }}
.hero-p {{ font-size:0.88rem; color:{muted}; line-height:1.65; margin-bottom:18px; }}
.chips {{ display:flex; flex-wrap:wrap; gap:6px; }}
.chip {{
  background:{surface}; border:1px solid {border};
  color:{muted}; font-size:0.72rem; font-weight:500;
  padding:5px 10px; border-radius:7px;
}}

/* Card */
.card {{
  background:{surface}; border:1px solid {border};
  border-radius:15px; padding:22px;
  margin-bottom:12px; box-shadow:0 2px 10px {shadow};
}}

/* Step header inside card */
.step-row {{ display:flex; align-items:center; gap:9px; margin-bottom:6px; }}
.step-num {{
  width:22px; height:22px; border-radius:50%;
  background:{accent}; color:#fff;
  font-size:0.62rem; font-weight:800;
  display:flex; align-items:center; justify-content:center; flex-shrink:0;
}}
.step-title {{ font-size:0.88rem; font-weight:700; color:{text_c}; }}
.step-desc  {{ font-size:0.76rem; color:{muted}; line-height:1.5; margin-bottom:12px; margin-left:31px; }}

/* Hint */
.hint {{
  background:{info_bg}; border-left:3px solid {info_fg};
  border-radius:0 8px 8px 0;
  padding:8px 12px; font-size:0.76rem;
  color:{info_fg}; font-weight:500; margin-bottom:12px;
}}
.ok-box {{
  background:{success_bg}; border-left:3px solid {success_fg};
  border-radius:0 8px 8px 0;
  padding:8px 12px; font-size:0.76rem;
  color:{success_fg}; font-weight:500; margin-top:8px;
}}
.err-box {{
  background:{error_bg}; border-left:3px solid {error_fg};
  border-radius:0 8px 8px 0;
  padding:8px 12px; font-size:0.76rem;
  color:{error_fg}; font-weight:500; margin-top:8px;
}}

/* Widgets */
/* Widgets */
.stRadio > div[role="radiogroup"] {{
  display:flex !important; gap:6px !important;
  background:{surface2} !important;
  border-radius:10px !important; padding:4px !important;
}}
.stRadio > div[role="radiogroup"] > label {{
  flex:1 !important; border-radius:7px !important;
  padding:10px 0 !important; text-align:center !important;
  justify-content:center !important; align-items:center !important;
  margin:0 !important; background:transparent !important; border:none !important;
  cursor:pointer !important; transition:background .15s !important;
}}
/* Hide the native radio circles to make them look like clean pills */
.stRadio > div[role="radiogroup"] > label > div:first-child {{
  display: none !important;
}}
.stRadio > div[role="radiogroup"] > label[data-checked="true"] {{
  background:{surface} !important; box-shadow:0 1px 4px {shadow} !important;
}}
.stRadio > div[role="radiogroup"] > label[data-checked="true"] p {{
  color:{text_c} !important; font-weight:700 !important;
}}
.stRadio > div[role="radiogroup"] > label p {{
  color:{muted} !important; font-size:0.83rem !important; margin:0 !important;
  width:100% !important; text-align:center !important;
}}

.stTextArea textarea {{
  background:{surface2} !important; border:1.5px solid {border} !important;
  border-radius:10px !important; color:{text_c} !important;
  font-family:'Sora',sans-serif !important; font-size:0.86rem !important;
  padding:12px !important; transition:border-color .15s !important;
}}
.stTextArea textarea:focus {{
  border-color:{accent} !important; box-shadow:0 0 0 3px {accent_dim} !important;
  outline:none !important;
}}
.stTextArea textarea::placeholder {{ color:{muted} !important; opacity:.6; }}
.stTextArea label {{ display:none !important; }}

.stSelectbox > div > div {{
  background:{surface2} !important; border:1.5px solid {border} !important;
  border-radius:10px !important; color:{text_c} !important;
}}
.stSelectbox label {{ display:none !important; }}

[data-testid="stFileUploader"] {{
  background:{surface2} !important; border:1.5px dashed {border} !important;
  border-radius:11px !important; transition:border-color .15s !important;
}}
[data-testid="stFileUploader"] section {{
  padding: 24px !important;
}}
[data-testid="stFileUploader"]:hover {{ border-color:{accent} !important; }}

[data-testid="baseButton-primary"] {{
  background:linear-gradient(135deg,{accent},#FBBF24) !important;
  border:none !important; border-radius:10px !important;
  font-weight:700 !important; font-size:0.9rem !important;
  color:#fff !important; padding:12px 28px !important;
  animation:pulseGlow 2.4s ease-in-out infinite;
  transition:transform .15s !important;
}}
[data-testid="baseButton-primary"]:hover {{ transform:translateY(-2px) !important; }}
[data-testid="baseButton-secondary"] {{
  background:{surface2} !important; border:1.5px solid {border} !important;
  border-radius:10px !important; color:{text_c} !important; font-weight:600 !important;
}}

.stTabs [data-baseweb="tab-list"] {{
  background:{surface2} !important; border-radius:10px !important;
  padding:4px !important; gap:3px !important; border:none !important;
}}
.stTabs [data-baseweb="tab"] {{
  border-radius:7px !important; color:{muted} !important;
  font-weight:500 !important; font-size:0.78rem !important;
  padding:7px 12px !important; border:none !important; background:transparent !important;
}}
.stTabs [aria-selected="true"] {{
  background:{surface} !important; color:{text_c} !important;
  font-weight:700 !important; box-shadow:0 1px 4px {shadow} !important;
}}
.stTabs [data-baseweb="tab-panel"] {{ padding:12px 0 0 0 !important; }}

.res-box {{
  background:{surface2}; border:1px solid {border};
  border-radius:10px; padding:15px 17px;
  color:{text_c}; font-size:0.86rem; line-height:1.7;
}}
.res-meta {{ display:flex; justify-content:space-between; align-items:center; margin-bottom:7px; }}
.res-label {{ font-size:0.6rem; font-weight:700; text-transform:uppercase; letter-spacing:1px; color:{muted}; }}
.res-badge {{
  font-size:0.6rem; font-weight:700;
  background:{accent_dim}; color:{accent};
  padding:2px 7px; border-radius:100px;
}}
.audio-wrap {{
  background:{surface2}; border:1px solid {border};
  border-radius:10px; padding:13px;
}}
audio {{ width:100% !important; border-radius:6px !important; }}
.divider {{ height:1px; background:{border}; margin:28px 0; }}
.wcount {{ text-align:right; font-size:0.66rem; color:{muted}; margin-top:3px; }}
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def get_base64_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

@st.cache_resource
def get_pipeline():
    try:
        return ProcessingPipeline()
    except Exception:
        return None

pipeline  = get_pipeline()
api_token = os.getenv("SUNBIRD_API_TOKEN")

# ── HEADER ────────────────────────────────────────────────────────────────────
logo_b64  = get_base64_image("logo.png")
logo_icon = (
    f'<img src="data:image/png;base64,{logo_b64}" style="width:19px;height:19px;object-fit:contain;">'
    if logo_b64 else "🐦"
)

hdr_l, hdr_r = st.columns([5, 1])
with hdr_l:
    st.markdown(f"""
    <div class="top-bar fu fu1">
      <div class="brand">
        <div class="brand-icon">{logo_icon}</div>
        <div>
          <div class="brand-name">Sunbird Echo AI</div>
          <div class="brand-sub">Voicing Uganda's languages</div>
        </div>
      </div>
      <div class="pill-row">
        <span class="pill">5+ dialects</span>
        <span class="pill">AI voices</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
with hdr_r:
    st.markdown("<div style='padding-top:10px;'>", unsafe_allow_html=True)
    st.button(
        "☀️ Light" if st.session_state.dark_mode else "🌙 Dark",
        on_click=toggle_dark_mode,
        use_container_width=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ── CONFIG GATE ───────────────────────────────────────────────────────────────
if not api_token or pipeline is None:
    st.markdown(f"""
    <div class="card" style="border-color:{error_fg};border-left:4px solid {error_fg};">
      <div style="font-size:1.3rem;margin-bottom:7px;">⚠️</div>
      <div style="font-size:0.95rem;font-weight:700;color:{text_c};margin-bottom:5px;">Configuration Required</div>
      <div style="color:{muted};font-size:0.82rem;line-height:1.6;">
        Add <code style="background:{surface2};padding:2px 5px;border-radius:4px;font-family:'JetBrains Mono',monospace;">SUNBIRD_API_TOKEN</code>
        to your <code style="background:{surface2};padding:2px 5px;border-radius:4px;font-family:'JetBrains Mono',monospace;">.env</code> file and restart.
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero fu fu2">
  <div class="eyebrow">✦ AI-Powered Translation</div>
  <div class="hero-h">Speak in any<br><em>Ugandan</em> dialect.</div>
  <div class="hero-p">
    Upload text or an audio recording — Sunbird transcribes, summarises,
    translates, and synthesises authentic speech in seconds.
  </div>
  <div class="chips">
    <div class="chip">🎙 Voice input</div>
    <div class="chip">📝 Text input</div>
    <div class="chip">🌍 5+ languages</div>
    <div class="chip">⚡ Real-time</div>
    <div class="chip">🔊 Audio output</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── STEP 1 — Input type ───────────────────────────────────────────────────────
st.markdown(f"""
<div class="card fu fu3">
  <div class="step-row">
    <div class="step-num">1</div>
    <div class="step-title">Choose your input type</div>
  </div>
  <div class="step-desc">Select Text to type or paste content, or Voice to upload an audio recording.</div>
</div>
""", unsafe_allow_html=True)

input_type = st.radio("Input type", ["📝 Text", "🎙 Voice"], horizontal=True, label_visibility="collapsed")
is_voice = "Voice" in input_type

# ── STEP 2 — Content ──────────────────────────────────────────────────────────
st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)
input_data = None

if not is_voice:
    st.markdown(f"""
    <div class="card fu fu3">
      <div class="step-row">
        <div class="step-num">2</div>
        <div class="step-title">Enter your content</div>
      </div>
      <div class="step-desc">Type or paste the text you want translated and voiced.</div>
      <div class="hint">💡 This can be an article, message, story, or any content you would like voiced in a Ugandan language.</div>
    </div>
    """, unsafe_allow_html=True)
    input_data = st.text_area("Content", placeholder="Type or paste your content here…", height=155, label_visibility="collapsed")
    if input_data:
        wc = len(input_data.split())
        st.markdown(f"<div class='wcount'>{wc} word{'s' if wc != 1 else ''}</div>", unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="card fu fu3">
      <div class="step-row">
        <div class="step-num">2</div>
        <div class="step-title">Upload a recording</div>
      </div>
      <div class="step-desc">Upload an audio file and Sunbird will transcribe it automatically before translating.</div>
      <div class="hint">💡 Supported: MP3, WAV, M4A, OGG, FLAC — max 50 MB (roughly 5 minutes of audio).</div>
    </div>
    """, unsafe_allow_html=True)
    uploaded = st.file_uploader("Audio file", type=["mp3", "wav", "m4a", "ogg", "flac"], label_visibility="collapsed")
    if uploaded:
        temp_path = f"temp_{uploaded.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded.getbuffer())
        size_mb = os.path.getsize(temp_path) / (1024 * 1024)
        if size_mb > 50:
            st.markdown(f"<div class='err-box'>⚠ File is {size_mb:.1f} MB — please trim or compress it below 50 MB.</div>", unsafe_allow_html=True)
            os.remove(temp_path)
        else:
            input_data = temp_path
            st.markdown(f"<div class='ok-box'>✓ {uploaded.name} uploaded ({size_mb:.1f} MB) — ready to process.</div>", unsafe_allow_html=True)

# ── STEP 3 — Language ─────────────────────────────────────────────────────────
st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)
supported_langs = list(ProcessingPipeline.get_supported_languages().keys())

st.markdown(f"""
<div class="card fu fu4">
  <div class="step-row">
    <div class="step-num">3</div>
    <div class="step-title">Choose output language</div>
  </div>
  <div class="step-desc">The translation and generated speech will be delivered in this language.</div>
</div>
""", unsafe_allow_html=True)

target_language = st.selectbox("Language", supported_langs, label_visibility="collapsed")

# ── GENERATE ──────────────────────────────────────────────────────────────────
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
go = st.button("🎙 Generate Speech", type="primary", use_container_width=True)

if go:
    has_input = input_data and (is_voice or input_data.strip())
    if not has_input:
        st.markdown(f"<div class='err-box'>⚠ Please provide some content before generating.</div>", unsafe_allow_html=True)
    else:
        with st.spinner(f"Translating to {target_language} and synthesising speech — this takes a few seconds…"):
            results = pipeline.run_full_pipeline(
                input_type="audio" if is_voice else "text",
                input_data=input_data,
                target_language=target_language
            )
            if is_voice and input_data and os.path.exists(input_data):
                try:
                    os.remove(input_data)
                except Exception:
                    pass
            results["target_language"] = target_language
            st.session_state.results = results
            st.rerun()

# ── RESULTS ───────────────────────────────────────────────────────────────────
if st.session_state.results is not None:
    res = st.session_state.results
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    if res["success"]:
        st.markdown(f"""
        <div class="ok-box fu fu1" style="margin-bottom:14px;">
          ✓ Done — your content has been translated and voiced successfully.
        </div>
        """, unsafe_allow_html=True)

        tabs = st.tabs(["📄 Original", "🎤 Transcript", "📋 Summary", "🌍 Translation", "🔊 Audio"])

        with tabs[0]:
            st.markdown(f"""
            <div class="res-meta">
              <span class="res-label">Input content</span>
              <span class="res-badge">Original</span>
            </div>
            <div class="res-box">{res['original_text']}</div>
            """, unsafe_allow_html=True)

        with tabs[1]:
            if res.get("transcript"):
                st.markdown(f"""
                <div class="res-meta">
                  <span class="res-label">Voice to text</span>
                  <span class="res-badge">Transcript</span>
                </div>
                <div class="res-box">{res['transcript']}</div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("<div class='hint'>ℹ No transcription needed — text input was used directly.</div>", unsafe_allow_html=True)

        with tabs[2]:
            if res.get("summary"):
                st.markdown(f"""
                <div class="res-meta">
                  <span class="res-label">AI condensed</span>
                  <span class="res-badge">Summary</span>
                </div>
                <div class="res-box">{res['summary']}</div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("<div class='hint'>ℹ Input was too short to summarise.</div>", unsafe_allow_html=True)

        with tabs[3]:
            st.markdown(f"""
            <div class="res-meta">
              <span class="res-label">Translated output</span>
              <span class="res-badge">{res.get('target_language', 'Target')}</span>
            </div>
            <div class="res-box">{res['translation']}</div>
            """, unsafe_allow_html=True)

        with tabs[4]:
            if res.get("audio_file") and os.path.exists(res["audio_file"]):
                st.markdown(f"""
                <div class="res-meta">
                  <span class="res-label">Synthesised speech</span>
                  <span class="res-badge">MP3 · Ready</span>
                </div>
                <div class="audio-wrap">
                """, unsafe_allow_html=True)
                with open(res["audio_file"], "rb") as af:
                    st.audio(af.read(), format="audio/mp3")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='err-box'>⚠ No audio file was generated. Check TTS service logs.</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        st.button("↺ Start over", on_click=clear_results)

    else:
        st.markdown(f"""
        <div class="card" style="border-left:4px solid {error_fg};border-color:{error_fg};">
          <div style="font-weight:700;color:{error_fg};margin-bottom:7px;">Pipeline failed</div>
        """, unsafe_allow_html=True)
        for err in res.get("errors", []):
            st.markdown(f"<div style='font-size:0.8rem;color:{muted};margin-bottom:3px;'>• {err}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.button("↺ Try again", on_click=clear_results)
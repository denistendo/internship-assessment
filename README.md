# Sunbird Echo AI

Sunbird Echo AI is an end-to-end web application that bridges the language gap by translating and voicing text or audio into native Ugandan languages. Built on the Sunbird AI API and Streamlit, the app allows users to input text or upload an audio recording. It instantly transcribes the audio, summarizes the content (if lengthy), translates it into one of five supported Ugandan dialects, and finally synthesizes authentic, high-quality local speech.

## 🏗 Architecture Overview

The application processes user input through a streamlined 4-step pipeline powered by the Sunbird AI REST endpoints:

1. **Input (Text or Voice)**
   - Users can type text or upload an audio file (MP3, WAV, M4A, etc.).
2. **Speech-to-Text (STT)** — `POST /tasks/stt`
   - If an audio file is uploaded, the app transcribes it into text using Sunbird's STT endpoint.
3. **Summarization** — `POST /tasks/sunflower_inference`
   - If the input text is greater than 30 words, it is passed to the Sunflower Chat LLM endpoint with strict system constraints to summarize the text, preventing excessively long audio generation.
4. **Translation** — `POST /tasks/sunflower_inference`
   - The processed text is translated into the target Ugandan language using the Sunflower LLM endpoint acting as a strict translator.
5. **Text-to-Speech (TTS)** — `POST /tasks/tts`
   - The translated text is synthesized into natural-sounding speech in the target dialect, returning an MP3 file that is played directly in the UI.

## 💻 Local Setup

Follow these exact steps to run the application locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd internship-assessment
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   - Copy the example environment file:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and add your Sunbird API token (see below).

5. **Run the app:**
   ```bash
   streamlit run app.py
   ```
   The application will open in your browser at `http://localhost:8501`.

## 🔐 Environment Variables

The application requires the following environment variables to authenticate with Sunbird services. You can copy the provided `.env.example` to create your local `.env` file.

| Variable | Description | Required |
|----------|-------------|----------|
| `SUNBIRD_API_TOKEN` | Your authentication token from the Sunbird AI API portal. Used as a Bearer token in headers for all endpoint requests. | Yes |

## 🚀 Usage Walkthrough

1. **Select Input Type:** Choose between typing text or uploading an audio recording.
2. **Provide Content:** 
   - Type your text into the text area.
   - OR upload a supported audio file (up to 50MB).
3. **Choose Target Language:** Select from Luganda, Runyankole, Ateso, Lugbara, or Acholi.
4. **Generate:** Click the "Generate Speech" button. The app will securely process your content through the Sunbird API.
5. **View Results:** The results panel will dynamically swap in, displaying your original text, transcript (if applicable), AI summary, translated text, and an interactive audio player with the synthesized speech.

## 🌐 Deployed Link

You can try the live, hosted version of the app here:
**[👉 Try Sunbird Echo AI Live on Hugging Face Spaces](https://huggingface.co/spaces/<your-username>/<your-space-name>)** *(Replace with your actual public link after deploying)*

## ⚠️ Known Limitations

- **Audio File Size:** The application currently restricts audio uploads to a maximum of 50 MB (roughly 5 minutes of audio) to prevent API timeouts.
- **Supported Languages:** Translation and TTS are strictly limited to the five dialects explicitly supported by the Sunbird API: Luganda, Runyankole, Ateso, Lugbara, and Acholi.
- **Processing Time:** Translating and synthesizing speech for very long texts can take up to 30-40 seconds due to LLM inference constraints on the Sunbird backend.
- **Audio Generation Failures:** Occasionally, the TTS endpoint may timeout. The application safely handles this by returning the written translation even if the audio generation fails.

---

## ☁ Deployment Instructions (Hugging Face Spaces)

This project is fully ready to be deployed as a Streamlit application on Hugging Face Spaces.

1. **Create an account:** Sign up for free at [https://huggingface.co/join](https://huggingface.co/join).
2. **Create a Space:** Go to [https://huggingface.co/new-space](https://huggingface.co/new-space).
   - Enter a name for your Space.
   - Select **Streamlit** as the Space SDK.
   - Set visibility to **Public**.
3. **Add your API Secret:**
   - Go to your new Space's Settings.
   - Scroll down to **Variables and secrets** -> **New secret**.
   - Name the secret `SUNBIRD_API_TOKEN` and paste your actual token as the value.
4. **Push your code:**
   Execute the following in your local terminal to deploy:
   ```bash
   git remote add space https://huggingface.co/spaces/<your-username>/<your-space-name>
   git push space main
   ```
Hugging Face will automatically install the libraries from `requirements.txt` and launch `app.py`.
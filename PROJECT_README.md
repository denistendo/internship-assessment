# Sunbird AI GenAI Web Application

This project is a small Generative AI web application powered by Sunbird AI's API. It demonstrates a complete language processing pipeline using local Ugandan languages.

## Project Description

The app allows users to input text or upload an audio file. It then runs this input through an AI pipeline that automatically transcribes audio (if provided), summarizes the text, translates the summary into a selected Ugandan local language (such as Luganda, Runyankole, Ateso, Lugbara, or Acholi), and finally synthesizes the translated text back into speech. It provides a clean, user-friendly interface built with Streamlit.

## Architecture Overview

The application utilizes a linear pipeline orchestrated by `backend/pipeline.py` which interfaces with Sunbird API via `backend/sunbird_client.py`.

The flow is as follows:
1. **Input**: Text or Audio (handled by Streamlit frontend)
2. **STT (Speech-to-Text)**: Audio is transcribed using the `/tasks/stt` Sunbird endpoint.
3. **Summarise**: The text (or transcript) is summarized using the `/tasks/sunflower_inference` endpoint.
4. **Translate**: The summary is translated to the chosen local language via the `/tasks/sunflower_inference` endpoint.
5. **TTS (Text-to-Speech)**: The translated summary is converted to audio using the `/tasks/tts` endpoint.
6. **Output**: The frontend displays all intermediate steps and a playable audio file.

## Local Setup

Follow these exact steps to run the application on your local machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/internship-assessment.git
   cd internship-assessment
   ```

2. **Set up a virtual environment:**
   - Linux/Mac: `python -m venv venv && source venv/bin/activate`
   - Windows: `python -m venv venv && venv\Scripts\activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   - Copy the `.env.example` file to create a new `.env` file:
     - Linux/Mac: `cp .env.example .env`
     - Windows: `copy .env.example .env`
   - Open `.env` and replace `your_sunbird_api_token_here` with your actual token from [api.sunbird.ai](https://api.sunbird.ai/).

5. **Run the Application:**
   ```bash
   streamlit run app.py
   ```

## Environment Variables

- `SUNBIRD_API_TOKEN` *(Required)*: Your authentication token used to securely communicate with the Sunbird AI APIs. You must get this from the Sunbird AI API portal.
- `SUNBIRD_API_BASE_URL` *(Optional)*: Base URL for the API. It defaults to `https://api.sunbird.ai` and generally does not need to be changed.

## Usage

1. Open the app in your browser (usually `http://localhost:8501`).
2. **Input Section:** Choose between "Text" or "Audio File".
   - If "Text", type or paste your content.
   - If "Audio", upload a valid file (must be under 5 minutes).
3. **Language Settings:** Choose your desired target language (e.g., Luganda).
4. Click **Run Pipeline**.
5. Once processing is complete, navigate through the **Results tabs** to view the original text, transcript, summary, translation, and play the generated audio!

## Known Limitations

- **Audio Constraint:** Audio file uploads are strictly limited to files shorter than 5 minutes.
- **Supported Languages:** Only translations to Luganda, Runyankole, Ateso, Lugbara, and Acholi are currently supported for synthesis.
- **Missing Token Handling:** The app requires the `SUNBIRD_API_TOKEN` to be correctly configured. It will refuse to run the pipeline if the token is missing.

## Deployed Link

*(Place your deployment link here once deployed to Hugging Face Spaces or Vercel, e.g., https://huggingface.co/spaces/your-username/sunbird-pipeline)*

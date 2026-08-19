# PRJ_495: Mental Health Support Chatbot (Aura AI)
**NLP & Generative AI for UN Sustainable Development Goal 3: Good Health and Well-being**

A full-stack, empathetic mental health guidance companion and emotional well-being platform built with **FastAPI**, **React + Vite + Tailwind CSS**, **NLP Sentiment & Emotion Classifiers**, **Cognitive Behavioral Therapy (CBT) Nudges**, **Standardized Clinical Assessments (PHQ-9 & GAD-7)**, **Paced Box Breathing**, and **24/7 Crisis Safety Interceptors**.

---

## 🌟 Key Features

1. **Empathetic AI Conversational Hub**
   - Active empathetic listening with dual support: **Google Gemini Generative AI** + Built-in **Offline CBT Empathy Engine**.
   - Real-time **Sentiment & Emotion Analysis** (Anxiety, Sadness, Overwhelm, Joy, Calm, Frustration).
   - **Cognitive Distortion Detector** (Catastrophizing, All-or-Nothing thinking, Should statements) with gentle reframing prompts.
   - Built-in **Web Speech Voice Recognition** (speech-to-text) and **Text-to-Speech (TTS)** voice readout.

2. **Standardized Clinical Screenings (PHQ-9 & GAD-7)**
   - Standard 9-item **PHQ-9** (Patient Health Questionnaire for Depression).
   - Standard 7-item **GAD-7** (Generalized Anxiety Disorder Screener).
   - Automated score calculation, severity tiering (Minimal, Mild, Moderate, Moderately Severe, Severe), Item-9 self-harm safety flags, and personalized evidence-based coping advice.
   - Historical records tracker.

3. **Emergency Crisis Interceptor & SOS Directory**
   - High-priority regex and semantic keyword interceptor that detects suicidal ideation or severe distress.
   - Instant de-escalation response and direct 1-click access to verified 24/7 helplines (India KIRAN, Tele-MANAS, US 988, UK Samaritans, Global Befrienders).

4. **Daily Mood & Emotion Journal**
   - 5-point emoji mood scale, energy tracker, multi-select emotion chips, and thought reflection journal.
   - Dynamic visual analytics with average mood calculations and trend history.

5. **Interactive Guided Box Breathing (4-4-4-4 & 4-7-8)**
   - Real-time animated breathing visualizer with dynamic aura scaling.
   - Web Audio API soothing synth tone chimes on phase transitions.
   - Cycle tracking and customizable techniques.

6. **UN SDG 3 Mental Health Resource Hub**
   - Target 3.4 overview: Stigma reduction, accessible digital mental health.
   - Interactive 5-4-3-2-1 sensory grounding checklist.
   - Mental Health Myths vs. Science-backed facts.

---

## ⚡ Quick Run (1-Click Drag & Drop)

### On Windows:
Double-click `start.bat` (or drag & drop the folder into a terminal). It will automatically install requirements, build the frontend, and open:
👉 **http://127.0.0.1:8000**

### On Linux / macOS:
```bash
chmod +x start.sh
./start.sh
```

---

## 🚀 Running via Command Line

### 1. Unified Single-Command Launch (Recommended)
Run the application with the pre-built modern React frontend served directly by FastAPI:
```bash
# 1. Install dependencies
pip install -r backend/requirements.txt
cd frontend && npm install && npm run build && cd ..

# 2. Start Unified Server
python run.py
```
Open your browser at:
- 👉 **http://127.0.0.1:8000** (Full Interactive App)  
- 👉 **http://127.0.0.1:8000/docs** (FastAPI Swagger Interactive Docs)

---

### 2. Development Mode (Hot-Reload)

#### Start Backend:
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

#### Start Frontend:
```bash
cd frontend
npm run dev
```

---

## 🐳 Docker Deployment

Run the complete full-stack container with one command:
```bash
docker compose up --build
```
Access the application at `http://localhost:8000`.

---

## ☁️ Cloud Deployment Guides

### Option A: Deploy on Render.com (1-Click / Free Tier)
1. Push this repository to your GitHub account.
2. In [Render Dashboard](https://dashboard.render.com/), select **New +** → **Web Service** and choose your repository.
3. Configure settings:
   - **Environment**: `Python 3`
   - **Build Command**: `cd frontend && npm install && npm run build && cd ../backend && pip install -r requirements.txt`
   - **Start Command**: `python run.py`
4. Add environment variables:
   - `GEMINI_API_KEY`: *(Optional, your Google Gemini API key)*
   - `PYTHON_VERSION`: `3.11.9`
5. Click **Create Web Service**.

### Option B: Deploy with Docker on Railway / Cloud Run / Fly.io
Deploy directly using the included multi-stage `Dockerfile`.

---

## 🧪 Running Automated Tests

Run backend unit tests for crisis interceptors, sentiment classification, PHQ-9/GAD-7 scoring, and API routes:
```bash
pytest backend/tests/
```

---

## 🔑 Environment Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `GEMINI_API_KEY` | Google Gemini API key from AI Studio | *(Optional - falls back to offline CBT engine)* |
| `HOST` | Server host address | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `DATABASE_URL` | SQLite Database connection string | `sqlite+aiosqlite:///./mental_health.db` |
| `ENVIRONMENT` | Environment mode (`development` or `production`) | `development` |

---

## 🔒 Safety & Ethical Disclaimer
Aura is an AI companion designed for emotional support, psychoeducation, and mindfulness coaching. It is **not a diagnostic tool, clinical medical device, or replacement for professional medical advice**. In case of emergency or severe distress, always contact verified emergency hotlines (e.g., 988, 112, 14416) or a licensed healthcare professional.

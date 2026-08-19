# PRJ_495: Mental Health Support Chatbot (Aura AI)
**NLP & Generative AI for UN Sustainable Development Goal 3: Good Health and Well-being**

A full-stack, empathetic mental health guidance companion and emotional well-being platform built with **FastAPI**, **NLP Sentiment & Emotion Classifiers**, **Cognitive Behavioral Therapy (CBT) Nudges**, **Standardized Clinical Assessments (PHQ-9 & GAD-7)**, **Paced Box Breathing**, and **24/7 Crisis Safety Interceptors**.

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

## 🚀 Quick Start Guide

### 1. Unified Single-Command Launch (Recommended)
Run the application with the pre-built modern React frontend served directly by FastAPI:
```bash
python run.py
```
Open your browser at:
👉 **http://127.0.0.1:8000** (Full Interactive App)  
👉 **http://127.0.0.1:8000/docs** (FastAPI Swagger Interactive Docs)

---

### 2. Development Mode (Separate Frontend & Backend)

#### Start Backend:
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

#### Start Frontend (Vite Hot-Reload):
```bash
cd frontend
npm run dev
```

---

## 🧪 Running Automated Tests

Run backend unit tests for crisis interceptors, sentiment classification, PHQ-9/GAD-7 scoring, and API routes:
```bash
cd backend
python -m pytest tests/
```

---

## 🔒 Safety & Ethical Disclaimer
Aura is an AI companion designed for emotional support, psychoeducation, and mindfulness coaching. It is **not a diagnostic tool, clinical medical device, or replacement for professional medical advice**. In case of emergency or severe distress, always contact verified emergency hotlines (e.g., 988, 112, 14416) or a licensed healthcare professional.

import random
import requests
from typing import Dict, Any, List, Optional
from app.core.config import settings
from app.core.safety import check_crisis_risk
from app.services.nlp_engine import analyze_sentiment

# System prompt used when calling LLMs
CBT_SYSTEM_PROMPT = """You are 'Aura', a compassionate, empathetic AI mental health companion dedicated to supporting emotional well-being (SDG 3: Good Health and Well-being).
Guidelines:
1. Empathy First: Validate feelings with warmth, active listening, and unconditional positive regard.
2. CBT & Grounding: Guide the user gently using Cognitive Behavioral Therapy principles (reframing negative automatic thoughts, finding evidence, breaking tasks down).
3. Mindfulness: Offer calming breathing exercises, grounding techniques (5-4-3-2-1), or journaling prompts when appropriate.
4. Non-Clinical Boundaries: Never diagnose, prescribe medication, or claim to be a doctor. Keep responses supportive, concise, and easy to read with bullet points when offering tips.
5. Always de-escalate anxiety and encourage gentle self-compassion.
"""

OFFLINE_RESPONSES = {
    "anxiety": [
        "I hear how tense and worried you're feeling right now. Anxiety can feel like a heavy storm inside, but remember that thoughts are not facts, and this feeling is temporary.",
        "It sounds like your mind is running fast with worries right now. Let's take a pause together. Would you like to try a quick 4-4-4-4 box breathing exercise or ground your senses?",
        "Feeling anxious is your nervous system trying to protect you, even when there is no immediate danger. You're safe here. Let's break down whatever is on your plate one small step at a time."
    ],
    "sadness": [
        "I'm really sorry you're feeling this weight today. It takes courage to open up when you're feeling down. I'm here with you, and you don't have to carry this alone.",
        "Thank you for sharing how you feel. Sadness can be exhausting, and it is completely okay to feel vulnerable. Please give yourself permission to rest and be gentle with yourself today.",
        "I can sense how painful and draining things feel for you right now. Remember that your feelings are valid. What is one small, comforting thing you can do for yourself today?"
    ],
    "anger": [
        "I hear your frustration, and it is completely understandable why you would feel angry about this. Anger is often a signal that something important to you feels crossed or unfair.",
        "It sounds like you've been pushed to your limit. Let's give that anger some healthy breathing room. Releasing tension through a deep exhale or writing out your unfiltered thoughts can help clear the fog.",
        "Your anger is valid. Before deciding how to respond to what happened, let's take a slow deep breath so you feel grounded and in control of your next step."
    ],
    "overwhelm": [
        "You have so much on your shoulders right now. When everything piles up at once, our brains naturally enter overload. Let's step back and look at just one tiny thing you can control right now.",
        "Feeling overwhelmed is a clear sign that you need to pause and breathe. You don't have to solve everything today. Let's identify just the single next easiest step.",
        "I hear how overloaded you feel. Remember: you are human, and you don't have to do it all at once. What would happen if you put aside non-essential tasks for just the next hour?"
    ],
    "joy": [
        "It is wonderful to hear that! Celebrating these positive moments and noticing gratitude reinforces our resilience and joy. What made this moment so special for you?",
        "I love hearing this positive energy! Savoring these bright moments is a wonderful practice for mental well-being. Keep holding on to that feeling!"
    ],
    "calm": [
        "It's so peaceful to hear you're feeling centered and calm. Enjoying these quiet, restful moments is wonderful for restoring your energy.",
        "A peaceful state of mind is precious. Take a moment to notice how relaxed your body feels right now so you can return to this anchor whenever you need it."
    ],
    "neutral": [
        "Thank you for sharing. I'm here as your supportive companion. Whether you'd like to reflect on your day, explore a thought, or just talk through whatever is on your mind, I'm listening.",
        "I'm listening closely. How has the rest of your day felt for you, or is there something specific you'd like to work through together?"
    ]
}

def generate_offline_cbt_response(user_text: str, nlp_result: Dict[str, Any]) -> str:
    """
    Generates a rich, empathetic CBT-guided response without requiring external API access.
    """
    primary_emotion = nlp_result.get("primary_emotion", "neutral")
    distortions = nlp_result.get("cognitive_distortions", [])
    
    # Pick baseline empathetic response
    options = OFFLINE_RESPONSES.get(primary_emotion, OFFLINE_RESPONSES["neutral"])
    base_response = random.choice(options)
    
    sections = [base_response]
    
    # Add CBT reflection if cognitive distortion is identified
    if distortions:
        d = distortions[0]
        cbt_note = (
            f"\n\n💡 **Gentle CBT Insight ({d['name']}):** "
            f"Notice how your thought might be leaning into *{d['name']}* ({d['description']}). "
            "A helpful exercise here is to ask yourself: *'What is concrete evidence for and against this thought? Is there a kinder, more balanced way to view this?'*"
        )
        sections.append(cbt_note)
    elif primary_emotion in ["anxiety", "overwhelm"]:
        action_tip = (
            "\n\n🌱 **Grounding Exercise (5-4-3-2-1 Technique):**\n"
            "Try scanning your surroundings right now and silently naming:\n"
            "• **5** things you can see\n"
            "• **4** things you can physically touch\n"
            "• **3** things you can hear\n"
            "• **2** things you can smell\n"
            "• **1** thing you can taste or appreciate about yourself"
        )
        sections.append(action_tip)
    elif primary_emotion == "sadness":
        self_care_tip = (
            "\n\n💙 **Gentle Self-Care Step:**\n"
            "• Drink a glass of fresh water.\n"
            "• Unclench your jaw and gently roll your shoulders back.\n"
            "• Place a hand over your heart and take three slow, soothing breaths."
        )
        sections.append(self_care_tip)
        
    return "".join(sections)

def generate_chat_response(
    user_text: str,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    api_key_override: Optional[str] = None
) -> Dict[str, Any]:
    """
    Main dialogue orchestrator:
    1. Safety & Crisis check
    2. Sentiment & Emotion analysis
    3. LLM generation (Gemini / OpenAI if configured) with fallback to Offline CBT engine
    """
    # 1. Check crisis risk
    crisis_check = check_crisis_risk(user_text)
    if crisis_check["is_crisis"]:
        return {
            "response": crisis_check["message"],
            "is_crisis": True,
            "severity": crisis_check["severity"],
            "hotlines": crisis_check["hotlines"],
            "emergency_prompt": crisis_check["emergency_prompt"],
            "nlp": {
                "compound": -0.9,
                "sentiment_label": "Critical Distress",
                "primary_emotion": "crisis",
                "cognitive_distortions": []
            },
            "source": "safety_interceptor"
        }
        
    # 2. NLP & Sentiment analysis
    nlp_result = analyze_sentiment(user_text)
    
    api_key = api_key_override or settings.GEMINI_API_KEY or settings.OPENAI_API_KEY
    
    # 3. Attempt Gemini API if key is present
    if api_key and (api_key.startswith("AIza") or len(api_key) > 20):
        try:
            # Call Gemini REST API directly
            gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            # Format prompt history
            contents = [
                {"role": "user", "parts": [{"text": f"System context:\n{CBT_SYSTEM_PROMPT}\nUser's detected emotion is: {nlp_result['primary_emotion']}"}]}
            ]
            if conversation_history:
                for msg in conversation_history[-4:]:
                    role = "user" if msg.get("role") == "user" else "model"
                    contents.append({"role": role, "parts": [{"text": msg.get("content", "")}]})
                    
            contents.append({"role": "user", "parts": [{"text": user_text}]})
            
            payload = {
                "contents": contents,
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 450,
                    "topP": 0.95
                }
            }
            
            resp = requests.post(gemini_url, json=payload, timeout=6)
            if resp.status_code == 200:
                data = resp.json()
                text_response = data["candidates"][0]["content"]["parts"][0]["text"]
                return {
                    "response": text_response,
                    "is_crisis": False,
                    "severity": "SAFE",
                    "hotlines": [],
                    "nlp": nlp_result,
                    "source": "gemini_ai"
                }
        except Exception:
            # Fallback smoothly to offline CBT engine if network / rate limit issue occurs
            pass

    # 4. Built-in Offline CBT Engine
    offline_reply = generate_offline_cbt_response(user_text, nlp_result)
    return {
        "response": offline_reply,
        "is_crisis": False,
        "severity": "SAFE",
        "hotlines": [],
        "nlp": nlp_result,
        "source": "cbt_empathy_engine"
    }

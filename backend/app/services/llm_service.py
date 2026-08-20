import random
import re
import requests
from typing import Dict, Any, List, Optional
from app.core.config import settings
from app.core.safety import check_crisis_risk
from app.services.nlp_engine import analyze_sentiment

# Base System prompt template used when calling LLMs (Gemini / OpenAI)
CBT_SYSTEM_PROMPT = """You are 'Aura', a compassionate, empathetic AI mental health companion dedicated to supporting emotional well-being (UN SDG 3: Good Health and Well-being).
Core Guidelines:
1. Dynamic Input-Driven Empathy: Always read the user's specific input carefully and respond directly to the exact situation, problem, or question they shared.
2. Cognitive Behavioral Therapy (CBT): Help the user identify unhelpful thought patterns (catastrophizing, all-or-nothing thinking, should statements) and gently reframe them into realistic, balanced perspectives.
3. Actionable & Grounding Techniques: Provide concrete, practical coping steps (e.g. 5-4-3-2-1 sensory grounding, 4-4-4-4 box breathing, task chunking, cognitive journaling prompts) tailored to their context.
4. Professional Boundaries: Maintain a supportive, non-judgmental tone. Never diagnose or prescribe medical treatments. Format responses cleanly with bullet points and bold highlights for readability.
"""

def generate_contextual_offline_response(user_text: str, nlp_result: Dict[str, Any], user_profile: Optional[Dict[str, Any]] = None) -> str:
    """
    Intelligent NLP Response Generator that dynamically constructs targeted responses
    based on the exact subject matter, user intent, detected emotions, and cognitive distortions.
    """
    topics = nlp_result.get("detected_topics", [])
    primary_emotion = nlp_result.get("primary_emotion", "neutral")
    distortions = nlp_result.get("cognitive_distortions", [])
    
    profile = user_profile or {}
    name = profile.get("name", "").strip()
    greeting = f"{name}, " if name else ""
    
    lower_input = user_text.lower().strip()
    
    # 1. Direct Question: What is CBT?
    if "question_cbt" in topics:
        return (
            f"{greeting}**Cognitive Behavioral Therapy (CBT)** is one of the most widely researched and effective psychological approaches for managing stress, anxiety, and depression.\n\n"
            "💡 **How CBT Works:**\n"
            "• **Thoughts:** What we think affects how we feel and act.\n"
            "• **Emotions:** How we feel affects what we think and do.\n"
            "• **Behaviors:** What we do affects how we think and feel.\n\n"
            "Whenever we feel overwhelmed, our brain often jumps into *cognitive distortions* (like predicting the worst or thinking in all-or-nothing extremes). "
            "CBT helps you catch those automatic thoughts, examine the evidence, and choose a more balanced, supportive response.\n\n"
            "Is there a specific thought or situation you'd like to practice reframing together?"
        )
        
    # 2. Direct Question: How to breathe / Grounding exercises?
    if "question_breathing" in topics:
        return (
            f"{greeting}Here are two evidence-based breathing and grounding exercises you can use anytime your nervous system feels activated:\n\n"
            "🌿 **1. Paced Box Breathing (4-4-4-4 Technique):**\n"
            "• **Inhale** slowly through your nose for **4 seconds**\n"
            "• **Hold** that breath gently for **4 seconds**\n"
            "• **Exhale** smoothly through your mouth for **4 seconds**\n"
            "• **Pause** with empty lungs for **4 seconds**\n"
            "*(Repeat 3–4 cycles to activate your calming vagus nerve)*\n\n"
            "🌱 **2. The 5-4-3-2-1 Sensory Grounding Reset:**\n"
            "Look around your room right now and name:\n"
            "• **5** things you can see\n"
            "• **4** things you can physically touch\n"
            "• **3** sounds you can hear\n"
            "• **2** scents you can smell\n"
            "• **1** positive thing you appreciate about yourself\n\n"
            "Would you like to try one of these with me right now?"
        )
        
    # 3. Academic & Exam Pressure
    if "academic" in topics:
        cbt_addon = ""
        if distortions:
            d = distortions[0]
            cbt_addon = f"\n\n💡 **Thought Reframe ({d['name']}):** It's common to think *'{d['description']}'*, but one test or grade does not measure your intelligence, potential, or human worth."
            
        return (
            f"{greeting}I hear how much pressure you are carrying regarding your studies and exams. Academic stress can easily trigger panic, brain fog, and self-doubt.\n\n"
            "Let's break this down into actionable, bite-sized steps:\n"
            "• **The 15-Minute Rule:** Instead of looking at the whole syllabus, pick just one tiny sub-topic and set a timer for 15 minutes of low-stakes reading.\n"
            "• **Active Brain Rest:** Study fatigue sets in quickly. Stand up, stretch your neck and shoulders, and drink a glass of water before continuing.\n"
            "• **Separate Urgency from Panic:** Focus only on what you can control *today*.{cbt_addon}\n\n"
            "What is the single most urgent topic or assignment on your mind right now? Let's take it one piece at a time."
        )
        
    # 4. Workplace, Job & Career Burnout
    if "workplace" in topics:
        return (
            f"{greeting}I hear the exhaustion and tension in what you're sharing about your work. Career demands, deadlines, and workplace dynamics can be deeply draining on your mental energy.\n\n"
            "💼 **Actionable Workplace Self-Care Strategies:**\n"
            "• **Micro-Boundaries:** Give yourself permission to disconnect during your lunch or breaks. Step away from your desk physically.\n"
            "• **Triage Your Tasks:** Categorize your workload into *'Must do today'*, *'Can wait until tomorrow'*, and *'Can be delegated or simplified'*.\n"
            "• **Release Imposter Anxiety:** Remind yourself that you don't have to be superhuman to do a good job. You are allowed to take pauses.\n\n"
            "Is there a specific task, meeting, or person at work that is causing the biggest drain on you right now?"
        )
        
    # 5. Sleep Difficulties & Night-time Racing Thoughts
    if "sleep" in topics:
        return (
            f"{greeting}It is so frustrating and exhausting when your body is tired, but your mind refuses to switch off. Night-time overthinking happens because there are no daytime distractions, so worries bubble up.\n\n"
            "🌙 **Bedtime Calming Steps:**\n"
            "• **The 'Brain Dump' Exercise:** Keep a notepad beside your bed. Write down every lingering worry or to-do list item to tell your brain: *'This is safely recorded, I will solve it tomorrow morning.'*\n"
            "• **4-7-8 Breathing:** Inhale through your nose for 4 seconds, hold for 7 seconds, and exhale slowly with a whoosh for 8 seconds. This lowers your heart rate.\n"
            "• **Get Out of Bed Rule:** If you've been tossing and turning for over 20 minutes, get up and sit in dim light with a book until you feel sleepy. Don't force sleep.\n\n"
            "Would you like to do a quick calming breath together to help you unwind?"
        )
        
    # 6. Relationship, Family or Social Conflict / Loneliness
    if "relationship" in topics:
        return (
            f"{greeting}Interpersonal tension and feeling isolated or misunderstood can cause deep emotional distress. It hurts when communication breaks down with people who matter to us.\n\n"
            "👥 **Constructive Emotional Grounding:**\n"
            "• **Separate Feelings from Assumptions:** Notice where facts end and assumptions about what the other person thinks begin.\n"
            "• **Emotional Space:** When arguments or interactions feel heated, taking a 20-minute pause allows your nervous system to cool down before responding.\n"
            "• **Honor Your Boundaries:** Your feelings, emotional limits, and needs are valid.\n\n"
            "Would you like to talk through what was said, or reflect on what you need most for yourself right now?"
        )
        
    # 7. Panic Attack / Physical Tension / Extreme Anxiety
    if "panic_anxiety" in topics or primary_emotion == "anxiety":
        return (
            f"{greeting}I'm right here with you. Take a slow, gentle breath. What you are experiencing right now is your body's alarm system going into overdrive, but **you are safe, and this physical surge will pass**.\n\n"
            "🌿 **Follow these 3 steps with me right now:**\n"
            "1. **Feel your feet on the ground:** Press your heels firmly into the floor.\n"
            "2. **Slow your exhale:** Inhale slowly through your nose for 4 seconds, and exhale very slowly through pursed lips for 6 seconds.\n"
            "3. **Name 3 physical things:** Look around and name 3 objects you can touch right in front of you.\n\n"
            "Tell me: What is one thing you can see in the room around you right now?"
        )
        
    # 8. Motivation, Procrastination & ADHD Focus
    if "motivation_procrastination" in topics:
        return (
            f"{greeting}Feeling stuck, unmotivated, or caught in procrastination is often a sign of emotional overload or fear of failure, not laziness.\n\n"
            "⚡ **The 5-Minute Micro-Start Rule:**\n"
            "• Pick the single easiest part of what you need to do.\n"
            "• Tell yourself: *'I will work on this for just 5 minutes.'*\n"
            "• If you want to stop after 5 minutes, you can. Overcoming the initial barrier is the hardest part.\n"
            "• Remove all guilt: Beating yourself up burns mental energy without moving you forward.\n\n"
            "What is the one small task you've been putting off? Let's break it down into a tiny 2-minute starting step."
        )
        
    # 9. Low Self-Esteem & Harsh Self-Criticism
    if "self_esteem" in topics:
        return (
            f"{greeting}I hear how fiercely your inner critic is attacking you right now. It takes a heavy toll when you're feeling down on yourself, but please hear this: **Your inner critic is a reaction to stress, not an objective truth about who you are.**\n\n"
            "💡 **CBT Compassion Check:**\n"
            "• If a close friend came to you with this exact mistake or feeling, would you call them a failure? Or would you offer understanding?\n"
            "• You deserve the same kindness and grace you would give to someone you care about.\n"
            "• Perfection is an illusion—everyone is learning and adapting every single day.\n\n"
            "What is one small thing about yourself, your resilience, or your efforts that you can acknowledge today?"
        )
        
    # 10. Gratitude, Wins & Positive Feelings
    if "gratitude_joy" in topics or primary_emotion == "joy":
        return (
            f"{greeting}That is wonderful to hear! 🎉 Celebrating these wins—no matter how big or small—is a powerful way to rewire your brain for resilience and joy.\n\n"
            "• Take a moment to really soak in this positive feeling and acknowledge the effort you put in.\n"
            "• Savoring good moments strengthens our emotional baseline for future challenges.\n\n"
            "What part of this achievement or moment makes you feel most proud?"
        )
        
    # 11. Greetings
    if "greetings" in topics:
        return (
            f"Hello {name + ' ' if name else ''}🌿 I am **Aura**, your empathetic mental health and well-being companion.\n\n"
            "I'm here to listen without judgment, help you explore anxious or overwhelming thoughts, guide you through calming grounding exercises, and support your daily well-being.\n\n"
            "*How are you feeling right in this moment? What is on your mind today?*"
        )
        
    # 12. Contextual Sadness / Emotional Venting
    if primary_emotion == "sadness":
        return (
            f"{greeting}Thank you for trusting me with how you feel. Sadness and emotional heaviness can make everything feel exhausting, and you don't have to carry this alone.\n\n"
            "💙 **A Gentle Reminder for Today:**\n"
            "• Your feelings are completely valid. You do not need to 'fix' everything right now.\n"
            "• Give yourself permission to slow down, rest, and take things moment by moment.\n"
            "• Try drinking a glass of water, relaxing your shoulders, and taking a few deep, comforting breaths.\n\n"
            "I'm listening closely. Would you like to share a little more about what triggered these feelings?"
        )
        
    # 13. General Contextual Fallback based on User's words
    return (
        f"{greeting}I hear what you are saying, and I appreciate you sharing this with me. "
        "It sounds like there is a lot on your mind right now.\n\n"
        "Let's look at this together:\n"
        "• When we talk things through, our thoughts often become clearer and less overwhelming.\n"
        "• What is the most important part of this situation that you'd like to work through or get off your chest?\n\n"
        "I'm right here with you. Tell me more about what's going on."
    )

def generate_chat_response(
    user_text: str,
    conversation_history: Optional[List[Dict[str, str]]] = None,
    api_key_override: Optional[str] = None,
    user_profile: Optional[Dict[str, Any]] = None,
    clinical_context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Main dialogue orchestrator:
    1. Safety & Crisis check
    2. Sentiment & Emotion & Topic analysis
    3. LLM generation (Gemini) with full conversation history and personalized context
    4. Fallback to Dynamic Contextual NLP Engine based directly on user input
    """
    # 1. Safety check
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
                "detected_topics": ["crisis"],
                "cognitive_distortions": []
            },
            "source": "safety_interceptor"
        }
        
    # 2. NLP & Sentiment & Topic analysis
    nlp_result = analyze_sentiment(user_text)
    
    api_key = api_key_override or settings.GEMINI_API_KEY or settings.OPENAI_API_KEY
    
    # 3. Profile details
    profile = user_profile or {}
    user_name = profile.get("name", "").strip() or "Friend"
    focus_area = profile.get("focus_area", "General Well-being & Mindfulness")
    tone_preference = profile.get("tone_preference", "Empathetic & Supportive")
    
    clinical_notes = []
    if clinical_context:
        if clinical_context.get("latest_phq9"):
            clinical_notes.append(f"Recent PHQ-9 Depression Screener: {clinical_context['latest_phq9']}")
        if clinical_context.get("latest_gad7"):
            clinical_notes.append(f"Recent GAD-7 Anxiety Screener: {clinical_context['latest_gad7']}")
        if clinical_context.get("latest_mood"):
            clinical_notes.append(f"Recent Mood Log: {clinical_context['latest_mood']}")

    clinical_str = " | ".join(clinical_notes) if clinical_notes else "None"

    # 4. Attempt Gemini LLM if API Key is configured
    if api_key and (api_key.startswith("AIza") or len(api_key) > 20):
        try:
            gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            system_instruction = (
                f"{CBT_SYSTEM_PROMPT}\n\n"
                f"User Profile: Name: {user_name}, Focus Area: {focus_area}, Preferred Tone: {tone_preference}\n"
                f"Clinical Context: {clinical_str}\n"
                f"Detected Emotions: {nlp_result['primary_emotion']} (Topics: {', '.join(nlp_result.get('detected_topics', []))})\n\n"
                f"Respond directly and specifically to the user's latest input with compassionate CBT techniques and actionable steps."
            )
            
            contents = [
                {"role": "user", "parts": [{"text": f"System Instructions:\n{system_instruction}"}]}
            ]
            if conversation_history:
                for msg in conversation_history[-6:]:
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
            pass

    # 5. Dynamic Contextual NLP Engine (works on the basis of user input)
    contextual_reply = generate_contextual_offline_response(
        user_text=user_text,
        nlp_result=nlp_result,
        user_profile=user_profile
    )
    return {
        "response": contextual_reply,
        "is_crisis": False,
        "severity": "SAFE",
        "hotlines": [],
        "nlp": nlp_result,
        "source": "dynamic_nlp_engine"
    }

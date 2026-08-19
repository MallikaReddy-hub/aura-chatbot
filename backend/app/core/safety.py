import re
from typing import Dict, Any, List, Optional

CRISIS_PATTERNS = [
    r"\b(suicide|suicidal|kill myself|end my life|want to die|take my life|better off dead|hang myself)\b",
    r"\b(self-harm|cut myself|cutting myself|hurting myself|hurt myself|overdose)\b",
    r"\b(can't go on|cannot go on anymore|no reason to live|no point in living|don't want to live)\b",
    r"\b(goodbye cruel world|farewell forever|ready to end it all)\b"
]

CRISIS_HOTLINES = [
    {
        "country": "India",
        "name": "KIRAN Mental Health Helpline",
        "number": "1800-599-0019",
        "description": "24/7 National mental health helpline operated by the Ministry of Social Justice & Empowerment."
    },
    {
        "country": "India",
        "name": "Tele-MANAS",
        "number": "14416 / 1800-891-4416",
        "description": "24/7 Tele-Mental Health Assistance and Networking Across States."
    },
    {
        "country": "India",
        "name": "Vandrevala Foundation",
        "number": "+91 9999 666 555",
        "description": "24/7 Free, confidential mental health and crisis counseling support."
    },
    {
        "country": "United States & Canada",
        "name": "Suicide & Crisis Lifeline",
        "number": "988",
        "description": "Free, confidential 24/7 call or text support for people in suicidal crisis or emotional distress."
    },
    {
        "country": "United States",
        "name": "Crisis Text Line",
        "number": "Text HOME to 741741",
        "description": "24/7 crisis support via text message."
    },
    {
        "country": "United Kingdom",
        "name": "Samaritans",
        "number": "116 123",
        "description": "Free 24-hour emotional support for anyone in distress or struggling to cope."
    },
    {
        "country": "International / Global",
        "name": "Befrienders Worldwide",
        "number": "befrienders.org",
        "description": "Global network of crisis hotlines and emotional support centers."
    },
    {
        "country": "International",
        "name": "Find A Helpline",
        "number": "findahelpline.com",
        "description": "Free, confidential crisis support across 130+ countries."
    }
]

def check_crisis_risk(text: str) -> Dict[str, Any]:
    """
    Evaluates if the user input contains severe distress or crisis indicators.
    Returns whether crisis mode is triggered, matched patterns, and the intervention message.
    """
    clean_text = text.lower().strip()
    
    matches = []
    for pattern in CRISIS_PATTERNS:
        found = re.findall(pattern, clean_text)
        if found:
            matches.extend(found)
            
    is_crisis = len(matches) > 0
    
    if is_crisis:
        safety_message = (
            "I hear how much pain you're going through right now, and I want you to know that you are not alone. "
            "Because I am an AI companion, I cannot provide immediate clinical or emergency assistance. "
            "Please connect with a compassionate professional who can support you right this moment. "
            "Help is available 24/7, completely free and confidential."
        )
        return {
            "is_crisis": True,
            "severity": "CRITICAL",
            "message": safety_message,
            "hotlines": CRISIS_HOTLINES,
            "emergency_prompt": "Please consider reaching out to one of the helplines listed below or contacting your local emergency service (such as 112, 911, or 999)."
        }
        
    return {
        "is_crisis": False,
        "severity": "SAFE",
        "message": None,
        "hotlines": []
    }

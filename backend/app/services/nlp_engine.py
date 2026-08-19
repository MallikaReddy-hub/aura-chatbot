import re
from typing import Dict, Any, List
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

EMOTION_LEXICONS = {
    "anxiety": [
        "anxious", "anxiety", "worried", "worry", "nervous", "panic", "scared", "dread",
        "overthinking", "racing thoughts", "jittery", "tense", "uneasy", "restless", "fearful", "shaking"
    ],
    "sadness": [
        "sad", "depressed", "unhappy", "crying", "heartbroken", "down", "gloomy", "hopeless",
        "lonely", "alone", "empty", "miserable", "grief", "mourning", "worthless", "exhausted"
    ],
    "anger": [
        "angry", "mad", "furious", "irritated", "annoyed", "frustrated", "rage", "pissed",
        "resentful", "hate", "bitter", "snapped", "livid"
    ],
    "overwhelm": [
        "overwhelmed", "drowning", "too much", "burnout", "burnt out", "suffocating",
        "can't handle", "overloaded", "swamped", "breaking point", "pressure"
    ],
    "joy": [
        "happy", "grateful", "joyful", "excited", "blessed", "content", "cheerful", "glad",
        "optimistic", "proud", "delighted", "peaceful", "energized"
    ],
    "calm": [
        "calm", "relaxed", "serene", "tranquil", "composed", "centered", "mindful", "rested"
    ]
}

COGNITIVE_DISTORTIONS = [
    {
        "type": "All-or-Nothing Thinking",
        "patterns": [r"\b(always|never|every time|everyone|nobody|completely useless|total failure)\b"],
        "description": "Viewing things in black-and-white categories without nuance."
    },
    {
        "type": "Catastrophizing",
        "patterns": [r"\b(worst case|disaster|ruined forever|everything is ruined|nightmare|doomed)\b"],
        "description": "Expecting the absolute worst-case scenario to unfold."
    },
    {
        "type": "Should Statements",
        "patterns": [r"\b(i should have|i must|i ought to|i have to be perfect)\b"],
        "description": "Holding rigid rules for yourself that create undue guilt and pressure."
    },
    {
        "type": "Emotional Reasoning",
        "patterns": [r"\b(i feel like a loser|i feel like nobody cares|i feel worthless so i am)\b"],
        "description": "Assuming that because you feel a negative emotion, it must reflect objective reality."
    },
    {
        "type": "Mind Reading / Overgeneralizing",
        "patterns": [r"\b(they all hate me|they think i'm stupid|everyone is judging me)\b"],
        "description": "Assuming you know what other people are thinking negatively about you."
    }
]

def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Computes VADER sentiment, primary/secondary emotions, and cognitive distortion hints.
    """
    if not text.strip():
        return {
            "compound": 0.0,
            "sentiment_label": "Neutral",
            "primary_emotion": "neutral",
            "emotion_scores": {},
            "cognitive_distortions": []
        }
        
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]
    
    if compound >= 0.05:
        sentiment_label = "Positive"
    elif compound <= -0.05:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"
        
    # Analyze emotions
    lower_text = text.lower()
    emotion_hits: Dict[str, int] = {}
    
    for emotion, keywords in EMOTION_LEXICONS.items():
        count = sum(1 for kw in keywords if kw in lower_text)
        if count > 0:
            emotion_hits[emotion] = count
            
    if emotion_hits:
        primary_emotion = max(emotion_hits, key=emotion_hits.get)
    else:
        if compound < -0.3:
            primary_emotion = "sadness"
        elif compound > 0.3:
            primary_emotion = "joy"
        else:
            primary_emotion = "neutral"
            
    # Detect potential cognitive distortions for CBT coaching
    distortions_found = []
    for dist in COGNITIVE_DISTORTIONS:
        for pat in dist["patterns"]:
            if re.search(pat, lower_text):
                distortions_found.append({
                    "name": dist["type"],
                    "description": dist["description"]
                })
                break
                
    return {
        "compound": round(compound, 3),
        "sentiment_label": sentiment_label,
        "positive": round(scores["pos"], 3),
        "negative": round(scores["neg"], 3),
        "neutral": round(scores["neu"], 3),
        "primary_emotion": primary_emotion,
        "detected_emotions": list(emotion_hits.keys()),
        "cognitive_distortions": distortions_found
    }

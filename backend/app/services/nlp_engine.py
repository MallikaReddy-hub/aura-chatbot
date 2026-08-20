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
        "lonely", "alone", "empty", "miserable", "grief", "mourning", "worthless", "exhausted", "hurts"
    ],
    "anger": [
        "angry", "mad", "furious", "irritated", "annoyed", "frustrated", "rage", "pissed",
        "resentful", "hate", "bitter", "snapped", "livid", "unfair"
    ],
    "overwhelm": [
        "overwhelmed", "drowning", "too much", "burnout", "burnt out", "suffocating",
        "can't handle", "overloaded", "swamped", "breaking point", "pressure", "exhausted"
    ],
    "joy": [
        "happy", "grateful", "joyful", "excited", "blessed", "content", "cheerful", "glad",
        "optimistic", "proud", "delighted", "peaceful", "energized", "celebrate", "won"
    ],
    "calm": [
        "calm", "relaxed", "serene", "tranquil", "composed", "centered", "mindful", "rested"
    ]
}

TOPIC_PATTERNS = {
    "academic": [
        r"\b(exam|exams|test|tests|study|studying|studied|marks|grades|gpa|college|school|university|assignment|homework|professor|teacher|class|syllabus)\b"
    ],
    "workplace": [
        r"\b(job|work|working|boss|manager|office|career|coworker|colleague|salary|interview|fired|promotion|workload|client|meeting|corporate)\b"
    ],
    "sleep": [
        r"\b(sleep|sleeping|insomnia|tired|bed|night|awake|can't sleep|nightmare|restless|exhausted|waking up|nap)\b"
    ],
    "relationship": [
        r"\b(mom|dad|mother|father|parents|family|friend|friends|boyfriend|girlfriend|partner|husband|wife|fight|argued|argument|breakup|divorce|lonely|alone|rejected|dating)\b"
    ],
    "panic_anxiety": [
        r"\b(panic attack|chest tight|heart racing|can't breathe|shaking|hyperventilating|dizzy|terrified|doom|trembling)\b"
    ],
    "motivation_procrastination": [
        r"\b(lazy|procrastinate|procrastinating|procrastination|no motivation|can't focus|distracted|adhd|stuck|wasting time|unproductive|cant get up)\b"
    ],
    "self_esteem": [
        r"\b(ugly|loser|failure|not good enough|hate myself|worthless|imposter|insecure|unattractive|ashamed|guilt|disappointment|useless)\b"
    ],
    "gratitude_joy": [
        r"\b(celebrate|win|accomplished|proud|good news|passed|got the job|promoted|happy today|grateful for|feeling good)\b"
    ],
    "question_cbt": [
        r"\b(what is cbt|how does cbt work|cognitive distortion|reframe|cognitive behavioral therapy|automatic thoughts)\b"
    ],
    "question_breathing": [
        r"\b(how to breathe|breathing exercise|box breathing|4-7-8|grounding|grounding technique|54321|5-4-3-2-1)\b"
    ],
    "greetings": [
        r"^(hi|hello|hey|greetings|good morning|good evening|good afternoon|namaste|how are you|who are you)\b"
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
        "patterns": [r"\b(worst case|disaster|ruined forever|everything is ruined|nightmare|doomed|end of the world)\b"],
        "description": "Expecting the absolute worst-case scenario to unfold."
    },
    {
        "type": "Should Statements",
        "patterns": [r"\b(i should have|i must|i ought to|i have to be perfect|should be able to)\b"],
        "description": "Holding rigid rules for yourself that create undue guilt and pressure."
    },
    {
        "type": "Emotional Reasoning",
        "patterns": [r"\b(i feel like a loser|i feel like nobody cares|i feel worthless so i am|feel like a failure)\b"],
        "description": "Assuming that because you feel a negative emotion, it must reflect objective reality."
    },
    {
        "type": "Mind Reading / Overgeneralizing",
        "patterns": [r"\b(they all hate me|they think i'm stupid|everyone is judging me|they must think)\b"],
        "description": "Assuming you know what other people are thinking negatively about you."
    }
]

def analyze_sentiment(text: str) -> Dict[str, Any]:
    """
    Computes VADER sentiment, primary/secondary emotions, detected topics, and cognitive distortion hints.
    """
    if not text.strip():
        return {
            "compound": 0.0,
            "sentiment_label": "Neutral",
            "primary_emotion": "neutral",
            "detected_topics": [],
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
        
    lower_text = text.lower()
    
    # 1. Analyze emotions
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
            
    # 2. Analyze Topics
    detected_topics = []
    for topic, patterns in TOPIC_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, lower_text):
                detected_topics.append(topic)
                break
                
    # 3. Detect cognitive distortions
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
        "detected_topics": detected_topics,
        "cognitive_distortions": distortions_found
    }

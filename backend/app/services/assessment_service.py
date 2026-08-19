from typing import Dict, Any, List

PHQ9_QUESTIONS = [
    {"id": 1, "text": "Little interest or pleasure in doing things"},
    {"id": 2, "text": "Feeling down, depressed, or hopeless"},
    {"id": 3, "text": "Trouble falling or staying asleep, or sleeping too much"},
    {"id": 4, "text": "Feeling tired or having little energy"},
    {"id": 5, "text": "Poor appetite or overeating"},
    {"id": 6, "text": "Feeling bad about yourself — or that you are a failure or have let yourself or your family down"},
    {"id": 7, "text": "Trouble concentrating on things, such as reading the newspaper or watching television"},
    {"id": 8, "text": "Moving or speaking so slowly that other people could have noticed, or being fidgety/restless"},
    {"id": 9, "text": "Thoughts that you would be better off dead, or of hurting yourself in some way"}
]

GAD7_QUESTIONS = [
    {"id": 1, "text": "Feeling nervous, anxious, or on edge"},
    {"id": 2, "text": "Not being able to stop or control worrying"},
    {"id": 3, "text": "Worrying too much about different things"},
    {"id": 4, "text": "Trouble relaxing"},
    {"id": 5, "text": "Being so restless that it is hard to sit still"},
    {"id": 6, "text": "Becoming easily annoyed or irritable"},
    {"id": 7, "text": "Feeling afraid, as if something awful might happen"}
]

ANSWER_OPTIONS = [
    {"value": 0, "label": "Not at all"},
    {"value": 1, "label": "Several days"},
    {"value": 2, "label": "More than half the days"},
    {"value": 3, "label": "Nearly every day"}
]

def score_phq9(answers: List[int]) -> Dict[str, Any]:
    """
    Computes PHQ-9 score, severity, risk flags, and clinical recommendations.
    """
    total_score = sum(answers)
    
    if total_score <= 4:
        severity = "Minimal or None"
        badge_color = "emerald"
        interpretation = "Your responses suggest minimal or no depressive symptoms at this time."
        recommendations = [
            "Continue maintaining balanced daily habits, regular sleep patterns, and physical activity.",
            "Practice regular mindfulness and gratitude to sustain your emotional resilience.",
            "Stay socially connected with loved ones and friends."
        ]
    elif total_score <= 9:
        severity = "Mild Depression"
        badge_color = "blue"
        interpretation = "Your responses indicate mild depressive symptoms that may periodically impact your mood."
        recommendations = [
            "Incorporate gentle daily physical activity like walking in nature or stretching.",
            "Use mood journaling to identify triggers and notice positive daily moments.",
            "Maintain consistent sleep hygiene and limit late-night screen time."
        ]
    elif total_score <= 14:
        severity = "Moderate Depression"
        badge_color = "amber"
        interpretation = "Your responses indicate moderate depressive symptoms that may be affecting your daily routines and energy."
        recommendations = [
            "Consider speaking with a licensed therapist, counselor, or mental health professional.",
            "Practice structured Cognitive Behavioral Therapy (CBT) exercises to gently challenge unhelpful thoughts.",
            "Break your daily responsibilities into manageable bite-sized micro-goals."
        ]
    elif total_score <= 19:
        severity = "Moderately Severe Depression"
        badge_color = "orange"
        interpretation = "Your responses suggest moderately severe depressive symptoms. Daily functioning may feel very challenging."
        recommendations = [
            "We strongly recommend consulting a healthcare provider, psychologist, or psychiatrist for a comprehensive assessment.",
            "Reach out to a trusted loved one or friend and share what you are experiencing.",
            "Prioritize basic self-care: adequate nutrition, hydration, and gentle rest without self-blame."
        ]
    else:
        severity = "Severe Depression"
        badge_color = "red"
        interpretation = "Your responses indicate severe depressive symptoms. Please know that support is readily available."
        recommendations = [
            "Immediate consultation with a medical or mental health professional is strongly advised.",
            "If you ever feel unsafe or overwhelmed, please reach out to crisis helplines (e.g., 988 or local services) immediately.",
            "Involve a trusted support person in your healthcare appointments."
        ]
        
    # Check item 9 for self-harm risk
    has_self_harm_risk = len(answers) >= 9 and answers[8] > 0
    
    return {
        "assessment_type": "PHQ-9 (Depression Screening)",
        "total_score": total_score,
        "max_score": 27,
        "severity": severity,
        "badge_color": badge_color,
        "interpretation": interpretation,
        "recommendations": recommendations,
        "has_self_harm_risk": has_self_harm_risk
    }

def score_gad7(answers: List[int]) -> Dict[str, Any]:
    """
    Computes GAD-7 score, severity, and evidence-based anxiety management tips.
    """
    total_score = sum(answers)
    
    if total_score <= 4:
        severity = "Minimal Anxiety"
        badge_color = "emerald"
        interpretation = "Your responses indicate minimal anxiety levels within the normal range."
        recommendations = [
            "Continue proactive wellness practices such as balanced diet, exercise, and hobbies.",
            "Practice occasional box breathing or mindfulness meditation to stay centered."
        ]
    elif total_score <= 9:
        severity = "Mild Anxiety"
        badge_color = "blue"
        interpretation = "Your responses suggest mild anxiety that may cause occasional worry or tension."
        recommendations = [
            "Try guided 4-7-8 breathing exercises when feeling nervous or before sleep.",
            "Limit excessive caffeine and screen time, particularly before bed.",
            "Write down worries in a journal to give your mind a structured release."
        ]
    elif total_score <= 14:
        severity = "Moderate Anxiety"
        badge_color = "amber"
        interpretation = "Your responses indicate moderate anxiety that may interfere with work, sleep, or focus."
        recommendations = [
            "Consider consulting a mental health professional or counselor for CBT-based anxiety tools.",
            "Practice progressive muscle relaxation (PMR) and somatic grounding techniques.",
            "Set aside a dedicated 15-minute 'worry time' each day to prevent thoughts from spilling into other hours."
        ]
    else:
        severity = "Severe Anxiety"
        badge_color = "red"
        interpretation = "Your responses suggest severe anxiety symptoms that significantly disrupt daily life."
        recommendations = [
            "We strongly encourage speaking with a licensed mental health clinician or doctor.",
            "Explore structured therapies such as CBT and mindfulness-based stress reduction (MBSR).",
            "Remember that panic and intense worry are biological stress reactions that can be effectively treated."
        ]
        
    return {
        "assessment_type": "GAD-7 (Anxiety Screening)",
        "total_score": total_score,
        "max_score": 21,
        "severity": severity,
        "badge_color": badge_color,
        "interpretation": interpretation,
        "recommendations": recommendations,
        "has_self_harm_risk": False
    }

def get_assessment_schema(assessment_type: str) -> Dict[str, Any]:
    if assessment_type.upper() == "PHQ-9":
        return {
            "type": "PHQ-9",
            "title": "PHQ-9 (Patient Health Questionnaire)",
            "subtitle": "Screening for depressive symptoms over the last 2 weeks",
            "questions": PHQ9_QUESTIONS,
            "options": ANSWER_OPTIONS,
            "max_score": 27
        }
    else:
        return {
            "type": "GAD-7",
            "title": "GAD-7 (Generalized Anxiety Disorder)",
            "subtitle": "Screening for anxiety symptoms over the last 2 weeks",
            "questions": GAD7_QUESTIONS,
            "options": ANSWER_OPTIONS,
            "max_score": 21
        }

import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database.db import get_db
from app.database.models import ChatMessage, MoodLog, AssessmentRecord
from app.core.safety import CRISIS_HOTLINES
from app.services.nlp_engine import analyze_sentiment
from app.services.llm_service import generate_chat_response
from app.services.assessment_service import get_assessment_schema, score_phq9, score_gad7

router = APIRouter()

# --- Pydantic Request/Response Models ---
class UserProfile(BaseModel):
    name: Optional[str] = ""
    focus_area: Optional[str] = "General Well-being & Mindfulness"
    tone_preference: Optional[str] = "Empathetic & Supportive"
    custom_goal: Optional[str] = ""

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default_user"
    api_key: Optional[str] = None
    user_profile: Optional[UserProfile] = None

class MoodRequest(BaseModel):
    session_id: Optional[str] = "default_user"
    mood_score: int
    energy_level: Optional[int] = 3
    emotion_tags: Optional[str] = ""
    notes: Optional[str] = ""

class AssessmentRequest(BaseModel):
    session_id: Optional[str] = "default_user"
    assessment_type: str  # "PHQ-9" or "GAD-7"
    answers: List[int]

# --- Routes ---

@router.post("/chat")
async def chat_endpoint(req: ChatRequest, db: AsyncSession = Depends(get_db)):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
        
    # Retrieve recent history for context
    stmt = (
        select(ChatMessage)
        .where(ChatMessage.session_id == req.session_id)
        .order_by(ChatMessage.created_at.desc())
        .limit(6)
    )
    result = await db.execute(stmt)
    history_records = result.scalars().all()
    history_records.reverse()
    
    formatted_history = [
        {"role": rec.role, "content": rec.content}
        for rec in history_records
    ]
    
    # Retrieve latest assessment and mood for clinical context
    clinical_ctx = {}
    try:
        stmt_phq = (
            select(AssessmentRecord)
            .where(AssessmentRecord.session_id == req.session_id, AssessmentRecord.assessment_type == "PHQ-9")
            .order_by(AssessmentRecord.created_at.desc())
            .limit(1)
        )
        res_phq = await db.execute(stmt_phq)
        latest_phq = res_phq.scalar_one_or_none()
        if latest_phq:
            clinical_ctx["latest_phq9"] = f"{latest_phq.severity} (Score: {latest_phq.total_score})"

        stmt_gad = (
            select(AssessmentRecord)
            .where(AssessmentRecord.session_id == req.session_id, AssessmentRecord.assessment_type == "GAD-7")
            .order_by(AssessmentRecord.created_at.desc())
            .limit(1)
        )
        res_gad = await db.execute(stmt_gad)
        latest_gad = res_gad.scalar_one_or_none()
        if latest_gad:
            clinical_ctx["latest_gad7"] = f"{latest_gad.severity} (Score: {latest_gad.total_score})"

        stmt_mood = (
            select(MoodLog)
            .where(MoodLog.session_id == req.session_id)
            .order_by(MoodLog.created_at.desc())
            .limit(1)
        )
        res_mood = await db.execute(stmt_mood)
        latest_mood = res_mood.scalar_one_or_none()
        if latest_mood:
            clinical_ctx["latest_mood"] = f"Mood score {latest_mood.mood_score}/5, Energy {latest_mood.energy_level}/5, Tags: {latest_mood.emotion_tags}"
    except Exception:
        pass

    # Generate chat response based directly on user input
    user_prof_dict = req.user_profile.dict() if req.user_profile else None
    response_data = generate_chat_response(
        user_text=req.message,
        conversation_history=formatted_history,
        api_key_override=req.api_key,
        user_profile=user_prof_dict,
        clinical_context=clinical_ctx
    )
    
    # Save user message
    user_msg = ChatMessage(
        session_id=req.session_id,
        role="user",
        content=req.message,
        sentiment=response_data["nlp"]["sentiment_label"],
        emotion=response_data["nlp"]["primary_emotion"],
        is_crisis=response_data["is_crisis"]
    )
    db.add(user_msg)
    
    # Save assistant message
    asst_msg = ChatMessage(
        session_id=req.session_id,
        role="assistant",
        content=response_data["response"],
        sentiment="Supportive",
        emotion="empathy",
        is_crisis=response_data["is_crisis"]
    )
    db.add(asst_msg)
    await db.commit()
    
    return {
        "reply": response_data["response"],
        "is_crisis": response_data["is_crisis"],
        "severity": response_data["severity"],
        "hotlines": response_data["hotlines"],
        "nlp": response_data["nlp"],
        "source": response_data["source"]
    }

@router.get("/chat/history/{session_id}")
async def get_chat_history(session_id: str = "default_user", db: AsyncSession = Depends(get_db)):
    stmt = (
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
        .limit(100)
    )
    result = await db.execute(stmt)
    records = result.scalars().all()
    
    return [
        {
            "id": r.id,
            "role": r.role,
            "content": r.content,
            "sentiment": r.sentiment,
            "emotion": r.emotion,
            "is_crisis": r.is_crisis,
            "created_at": r.created_at.isoformat() if r.created_at else None
        }
        for r in records
    ]

@router.post("/moods")
async def record_mood(req: MoodRequest, db: AsyncSession = Depends(get_db)):
    if req.mood_score < 1 or req.mood_score > 5:
        raise HTTPException(status_code=400, detail="Mood score must be between 1 and 5.")
        
    mood_entry = MoodLog(
        session_id=req.session_id,
        mood_score=req.mood_score,
        energy_level=req.energy_level or 3,
        emotion_tags=req.emotion_tags or "",
        notes=req.notes or ""
    )
    db.add(mood_entry)
    await db.commit()
    await db.refresh(mood_entry)
    
    return {
        "status": "success",
        "id": mood_entry.id,
        "mood_score": mood_entry.mood_score,
        "energy_level": mood_entry.energy_level,
        "emotion_tags": mood_entry.emotion_tags,
        "notes": mood_entry.notes,
        "created_at": mood_entry.created_at.isoformat() if mood_entry.created_at else None
    }

@router.get("/moods/{session_id}")
async def get_mood_logs(session_id: str = "default_user", db: AsyncSession = Depends(get_db)):
    stmt = (
        select(MoodLog)
        .where(MoodLog.session_id == session_id)
        .order_by(MoodLog.created_at.desc())
        .limit(30)
    )
    result = await db.execute(stmt)
    logs = result.scalars().all()
    
    if not logs:
        return {"logs": [], "stats": {"average_mood": 0, "total_entries": 0, "average_energy": 0}}
        
    avg_mood = sum(l.mood_score for l in logs) / len(logs)
    avg_energy = sum(l.energy_level for l in logs) / len(logs)
    
    return {
        "logs": [
            {
                "id": l.id,
                "mood_score": l.mood_score,
                "energy_level": l.energy_level,
                "emotion_tags": [tag.strip() for tag in l.emotion_tags.split(",") if tag.strip()] if l.emotion_tags else [],
                "notes": l.notes,
                "created_at": l.created_at.isoformat() if l.created_at else None
            }
            for l in logs
        ],
        "stats": {
            "average_mood": round(avg_mood, 2),
            "average_energy": round(avg_energy, 2),
            "total_entries": len(logs)
        }
    }

@router.get("/assessments/schema/{assessment_type}")
async def get_assessment_questions(assessment_type: str):
    schema = get_assessment_schema(assessment_type)
    return schema

@router.post("/assessments")
async def submit_assessment(req: AssessmentRequest, db: AsyncSession = Depends(get_db)):
    atype = req.assessment_type.upper()
    if atype == "PHQ-9":
        if len(req.answers) != 9:
            raise HTTPException(status_code=400, detail="PHQ-9 requires exactly 9 responses.")
        score_result = score_phq9(req.answers)
    elif atype == "GAD-7":
        if len(req.answers) != 7:
            raise HTTPException(status_code=400, detail="GAD-7 requires exactly 7 responses.")
        score_result = score_gad7(req.answers)
    else:
        raise HTTPException(status_code=400, detail="Unknown assessment type. Choose 'PHQ-9' or 'GAD-7'.")
        
    record = AssessmentRecord(
        session_id=req.session_id,
        assessment_type=req.assessment_type,
        total_score=score_result["total_score"],
        severity=score_result["severity"],
        answers_json=json.dumps(req.answers),
        recommendations_json=json.dumps(score_result["recommendations"]),
        has_self_harm_risk=score_result.get("has_self_harm_risk", False)
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    
    return {
        "id": record.id,
        **score_result
    }

@router.get("/assessments/{session_id}")
async def get_user_assessments(session_id: str = "default_user", db: AsyncSession = Depends(get_db)):
    stmt = (
        select(AssessmentRecord)
        .where(AssessmentRecord.session_id == session_id)
        .order_by(AssessmentRecord.created_at.desc())
        .limit(20)
    )
    result = await db.execute(stmt)
    records = result.scalars().all()
    
    return [
        {
            "id": r.id,
            "assessment_type": r.assessment_type,
            "total_score": r.total_score,
            "severity": r.severity,
            "answers": json.loads(r.answers_json),
            "recommendations": json.loads(r.recommendations_json),
            "has_self_harm_risk": r.has_self_harm_risk,
            "created_at": r.created_at.isoformat() if r.created_at else None
        }
        for r in records
    ]

@router.get("/resources")
async def get_resources():
    return {
        "sdg_info": {
            "title": "UN Sustainable Development Goal 3 (SDG 3)",
            "subtitle": "Good Health and Well-being",
            "target": "Target 3.4: Promote mental health and well-being through prevention, treatment, and accessible digital wellness support.",
            "description": "Mental health is an integral foundation of overall human health and societal flourishing. Digital AI companions reduce stigma, democratize access to evidence-based coping tools, and guide individuals to professional care when needed."
        },
        "grounding_techniques": [
            {
                "title": "5-4-3-2-1 Sensory Grounding",
                "category": "Anxiety & Panic Relief",
                "summary": "An evidence-based mindfulness technique that anchors your active awareness in the physical environment.",
                "steps": [
                    "Acknowledge 5 things you see around you.",
                    "Acknowledge 4 things you can touch or feel with your skin.",
                    "Acknowledge 3 distinct sounds you hear.",
                    "Acknowledge 2 things you can smell.",
                    "Acknowledge 1 thing you can taste or one positive thought about yourself."
                ]
            },
            {
                "title": "4-4-4-4 Box Breathing (Square Breathing)",
                "category": "Stress & Autonomic Nervous System Regulation",
                "summary": "Used by first responders and clinicians to calm heart rate and trigger parasympathetic relaxation.",
                "steps": [
                    "Inhale smoothly through your nose for 4 seconds.",
                    "Hold your breath gently for 4 seconds.",
                    "Exhale slowly and completely through your mouth for 4 seconds.",
                    "Hold empty for 4 seconds.",
                    "Repeat cycle 4 to 6 times."
                ]
            },
            {
                "title": "Cognitive Reframing (CBT 3-Column Method)",
                "category": "Depressive & Anxious Thoughts",
                "summary": "Transforms automatic negative thoughts (ANTs) into balanced, realistic perspectives.",
                "steps": [
                    "Identify the automatic thought (e.g. 'I will fail this presentation').",
                    "Identify the cognitive distortion (e.g. Catastrophizing / Fortune Telling).",
                    "Formulate a rational, balanced replacement (e.g. 'I have prepared well, and even if I make a minor slip, I can handle it gracefully')."
                ]
            },
            {
                "title": "Progressive Muscle Relaxation (PMR)",
                "category": "Somatic Tension & Sleep Support",
                "summary": "Systematically tenses and releases muscle groups to discharge physical stress from the body.",
                "steps": [
                    "Start with your feet: curl your toes tightly for 5 seconds, then release completely.",
                    "Move upward: tense your calves, thighs, abdomen, chest, shoulders, hands, and face.",
                    "Notice the profound warmth and relaxation after each release."
                ]
            }
        ],
        "helplines": CRISIS_HOTLINES
    }

@router.get("/crisis-hotlines")
async def get_crisis_hotlines():
    return CRISIS_HOTLINES

import datetime
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(64), index=True, default="default_user")
    role = Column(String(16))  # "user" or "assistant"
    content = Column(Text, nullable=False)
    sentiment = Column(String(32), nullable=True)
    emotion = Column(String(32), nullable=True)
    is_crisis = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class MoodLog(Base):
    __tablename__ = "mood_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(64), index=True, default="default_user")
    mood_score = Column(Integer, nullable=False)  # 1 (very sad) to 5 (great)
    energy_level = Column(Integer, default=3)      # 1 to 5
    emotion_tags = Column(String(256), default="")  # e.g., "Calm, Grateful, Anxious"
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AssessmentRecord(Base):
    __tablename__ = "assessment_records"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(64), index=True, default="default_user")
    assessment_type = Column(String(32), nullable=False)  # "PHQ-9" or "GAD-7"
    total_score = Column(Integer, nullable=False)
    severity = Column(String(64), nullable=False)
    answers_json = Column(Text, nullable=False)
    recommendations_json = Column(Text, nullable=False)
    has_self_harm_risk = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

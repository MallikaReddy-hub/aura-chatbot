import pytest
from app.core.safety import check_crisis_risk
from app.services.nlp_engine import analyze_sentiment
from app.services.assessment_service import score_phq9, score_gad7
from app.services.llm_service import generate_chat_response
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_crisis_interceptor_triggers():
    # Suicidal ideation triggers
    res1 = check_crisis_risk("I feel like I want to end my life, please help")
    assert res1["is_crisis"] is True
    assert res1["severity"] == "CRITICAL"
    assert len(res1["hotlines"]) > 0
    assert "988" in [h["number"] for h in res1["hotlines"]]

    # Self harm triggers
    res2 = check_crisis_risk("I am thinking about cutting myself today")
    assert res2["is_crisis"] is True

    # Safe text does not trigger crisis mode
    res3 = check_crisis_risk("I had a stressful day at work and need to talk")
    assert res3["is_crisis"] is False
    assert res3["severity"] == "SAFE"

def test_sentiment_and_emotion_analysis():
    # Anxiety text
    nlp_anx = analyze_sentiment("I am extremely anxious and nervous about my exam tomorrow")
    assert nlp_anx["primary_emotion"] == "anxiety"
    
    # Sadness text
    nlp_sad = analyze_sentiment("I feel lonely and depressed, crying all evening")
    assert nlp_sad["primary_emotion"] == "sadness"
    assert nlp_sad["compound"] < 0
    
    # Joy text
    nlp_joy = analyze_sentiment("I had a wonderful day and I feel very happy and grateful!")
    assert nlp_joy["primary_emotion"] == "joy"
    assert nlp_joy["compound"] > 0

    # Cognitive distortion detection (Catastrophizing)
    nlp_dist = analyze_sentiment("Everything is ruined forever and it is a total disaster")
    distortions = [d["name"] for d in nlp_dist["cognitive_distortions"]]
    assert "Catastrophizing" in distortions or "All-or-Nothing Thinking" in distortions

def test_phq9_scoring():
    # All zeros -> Minimal
    res_min = score_phq9([0]*9)
    assert res_min["total_score"] == 0
    assert "Minimal" in res_min["severity"]
    assert res_min["has_self_harm_risk"] is False

    # Moderate score
    res_mod = score_phq9([1, 2, 1, 2, 1, 2, 1, 1, 0])
    assert res_mod["total_score"] == 11
    assert "Moderate" in res_mod["severity"]

    # Question 9 trigger (self harm flag)
    res_q9 = score_phq9([0, 0, 0, 0, 0, 0, 0, 0, 2])
    assert res_q9["has_self_harm_risk"] is True

def test_gad7_scoring():
    # Minimal
    res_min = score_gad7([0]*7)
    assert res_min["total_score"] == 0
    assert "Minimal" in res_min["severity"]

    # Severe
    res_sev = score_gad7([3]*7)
    assert res_sev["total_score"] == 21
    assert "Severe" in res_sev["severity"]

def test_chat_generation_flow():
    # Safe message response
    res = generate_chat_response("I have been feeling stressed lately.")
    assert res["is_crisis"] is False
    assert len(res["response"]) > 20
    assert res["source"] in ["cbt_empathy_engine", "gemini_ai"]

    # Crisis message response
    res_crisis = generate_chat_response("I want to commit suicide")
    assert res_crisis["is_crisis"] is True
    assert len(res_crisis["hotlines"]) > 0

def test_api_endpoints():
    # Health check
    r_health = client.get("/health")
    assert r_health.status_code == 200
    assert r_health.json()["status"] == "healthy"

    # API Info
    r_info = client.get("/api/info")
    assert r_info.status_code == 200
    assert "PRJ_495" in r_info.json()["code"]

    # Resources
    r_res = client.get("/api/resources")
    assert r_res.status_code == 200
    assert "grounding_techniques" in r_res.json()

    # Crisis hotlines
    r_hotlines = client.get("/api/crisis-hotlines")
    assert r_hotlines.status_code == 200
    assert len(r_hotlines.json()) > 0

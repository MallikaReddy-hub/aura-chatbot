import os
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "Mental Health Support Chatbot"
    PROJECT_CODE: str = "PRJ_495"
    SDG_GOAL: str = "SDG 3: Good Health and Well-being"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    DATABASE_URL: str = "sqlite+aiosqlite:///./mental_health.db"
    
settings = Settings()

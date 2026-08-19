import uvicorn
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(backend_dir))

if __name__ == "__main__":
    print("==================================================================")
    print("🌱 Aura - AI Mental Health Support Companion (PRJ_495 | SDG 3)")
    print("🚀 Starting Unified Server at: http://127.0.0.1:8000")
    print("📖 API Documentation at: http://127.0.0.1:8000/docs")
    print("==================================================================")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True, app_dir=str(backend_dir))

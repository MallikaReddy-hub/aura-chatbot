import os
import sys
from pathlib import Path
import uvicorn

# Ensure UTF-8 stdout/stderr for cross-platform compatibility
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(backend_dir))

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    is_prod = os.getenv("ENVIRONMENT", "").lower() == "production" or os.getenv("RENDER") or os.getenv("RAILWAY_ENVIRONMENT")

    print("==================================================================")
    print("  Aura - AI Mental Health Support Companion (PRJ_495 | SDG 3)")
    print(f"  Starting Unified Server at: http://{host}:{port}")
    print(f"  API Documentation at: http://{host}:{port}/docs")
    print("==================================================================")
    uvicorn.run("app.main:app", host=host, port=port, reload=not is_prod, app_dir=str(backend_dir))


import os
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.core.config import settings
from app.database.db import init_db
from app.api.routes import router as api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database tables
    await init_db()
    yield

app = FastAPI(
    title=f"{settings.PROJECT_CODE} - {settings.PROJECT_NAME}",
    description="Empathetic AI Mental Health Companion for SDG 3 (Good Health and Well-being).",
    version=settings.VERSION,
    lifespan=lifespan
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(api_router, prefix="/api")

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/info")
async def api_info():
    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "code": settings.PROJECT_CODE,
        "sdg": settings.SDG_GOAL,
        "version": settings.VERSION,
        "docs": "/docs"
    }

# Serve frontend build if exists
dist_dir = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if dist_dir.exists() and (dist_dir / "index.html").exists():
    app.mount("/assets", StaticFiles(directory=str(dist_dir / "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path.startswith("api/") or full_path == "api" or full_path.startswith("health") or full_path.startswith("docs") or full_path.startswith("openapi.json"):
            return None
        file_path = dist_dir / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(dist_dir / "index.html")
else:
    @app.get("/")
    async def root():
        return {
            "status": "online",
            "project": settings.PROJECT_NAME,
            "code": settings.PROJECT_CODE,
            "sdg": settings.SDG_GOAL,
            "version": settings.VERSION,
            "docs": "/docs"
        }

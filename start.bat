@echo off
title Aura Mental Health Chatbot
echo ==================================================================
echo   Aura - AI Mental Health Support Companion (PRJ_495)
echo ==================================================================
echo.

cd /d "%~dp0"

echo [1/3] Checking Node.js and building frontend...
cd frontend
call npm install
call npm run build
if %ERRORLEVEL% NEQ 0 (
    echo Warning: Frontend build failed. Starting backend anyway...
)
cd ..

echo.
echo [2/3] Installing Python dependencies...
python -m pip install -r backend/requirements.txt

echo.
echo [3/3] Launching unified server at http://127.0.0.1:8000...
echo Open your browser at: http://127.0.0.1:8000
echo.
python run.py

pause

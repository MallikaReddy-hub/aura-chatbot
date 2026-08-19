#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "=================================================================="
echo "  Aura - AI Mental Health Support Companion (PRJ_495)"
echo "=================================================================="
echo ""

echo "[1/3] Building frontend..."
cd frontend
npm install
npm run build
cd ..

echo "[2/3] Installing backend dependencies..."
pip install -r backend/requirements.txt

echo "[3/3] Launching unified server..."
python run.py

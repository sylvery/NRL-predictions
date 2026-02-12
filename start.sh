#!/bin/bash
# Railway deployment start script

set -e  # Exit on error

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Starting NRL Predictions API..."
exec python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT

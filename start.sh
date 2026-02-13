#!/bin/bash
# Railway deployment start script - auto-fetches fixtures from nrl.com

set -e  # Exit on error

echo "🚀 Starting NRL Predictions..."

# Install dependencies (if not already installed)
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Fetch fixtures from nrl.com
echo "🔄 Fetching fixtures from nrl.com..."
python3 scripts/fetch_fixtures.py

echo "✅ Fixtures updated successfully!"

# Start the FastAPI application
echo "🌐 Starting web server..."
exec python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT

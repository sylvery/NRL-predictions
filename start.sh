#!/bin/bash
# Railpack start script for Railway deployment
# Updated: 2026-02-12

# Install dependencies
pip install --upgrade pip
pip install -r requirements-web.txt

# Start the FastAPI application using python -m
exec python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT

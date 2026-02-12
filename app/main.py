"""
NRL Predictions FastAPI Application

A web application for NRL match predictions using ML.
"""

import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import logging

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create templates directory
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
os.makedirs(templates_dir, exist_ok=True)

# Create static directory
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)

# Initialize templates
templates = Jinja2Templates(directory=templates_dir)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("🚀 NRL Predictions API starting...")
    logger.info("📅 Loading ML models...")
    yield
    # Shutdown
    logger.info("👋 NRL Predictions API shutting down...")


# Create FastAPI app
app = FastAPI(
    title="NRL Predictions API",
    description="Get ML-powered predictions for NRL matches",
    version="1.0.0",
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")


# Import routes after app creation to avoid circular imports
from app.routes import predictions, fixtures


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page."""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "NRL Predictions"
    })


@app.get("/api")
async def api_root():
    """API root with available endpoints."""
    return {
        "name": "NRL Predictions API",
        "version": "1.0.0",
        "endpoints": {
            "predictions": "/api/predictions",
            "fixtures": "/api/fixtures",
            "health": "/api/health"
        },
        "documentation": "/docs"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "nrl-predictions-api"}


def main():
    """Run the application using uvicorn."""
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()

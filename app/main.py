"""
NRL Predictions FastAPI Application
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI(
    title="NRL Predictions API",
    description="NRL Match Predictions and Try Scorer Probabilities",
    version="1.0.0"
)

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Mount templates
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)


@app.get("/")
async def home():
    """Home page"""
    return {
        "message": "NRL Predictions API",
        "version": "1.0.0",
        "endpoints": {
            "predictions": "/api/predictions",
            "fixtures": "/api/fixtures",
            "health": "/api/health"
        }
    }


@app.get("/api/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


# Import routes
from app.routes import predictions, fixtures


@app.get("/api/predictions")
async def get_predictions():
    """Get match predictions"""
    return predictions.get_predictions()


@app.get("/api/fixtures")
async def get_fixtures():
    """Get upcoming fixtures"""
    return fixtures.get_fixtures()


@app.get("/try-scorers")
async def try_scorers_page():
    """Try scorer predictions page"""
    return templates.TemplateResponse("try_scorers.html", {"request": {}})


@app.get("/fixtures")
async def fixtures_page():
    """Fixtures page"""
    return templates.TemplateResponse("fixtures.html", {"request": {}})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

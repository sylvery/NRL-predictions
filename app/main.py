"""
NRL Predictions FastAPI Application
Fetches real data from nrl.com
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

app = FastAPI(
    title="NRL Predictions API",
    description="NRL Match Predictions and Try Scorer Probabilities - Real-time data from nrl.com",
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
async def home(request: Request):
    """Home page with current fixtures"""
    return templates.TemplateResponse("index.html", {"request": request})


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
async def get_fixtures(round_num: int = None):
    """Get fixtures - all or specific round from nrl.com"""
    if round_num:
        return fixtures.get_round_fixtures(round_num)
    return fixtures.get_fixtures()


@app.get("/fixtures")
async def fixtures_page(request: Request):
    """Fixtures page"""
    return templates.TemplateResponse("fixtures.html", {"request": request})


@app.get("/try-scorers")
async def try_scorers_page(request: Request):
    """Try scorer predictions page"""
    return templates.TemplateResponse("try_scorers.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

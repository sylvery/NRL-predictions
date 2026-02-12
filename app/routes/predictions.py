"""
API routes for NRL predictions.
"""

import sys
import os
import requests
from bs4 import BeautifulSoup
import json
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ENVIRONMENT_VARIABLES as EV

router = APIRouter()

# Team strength ratings
TEAM_RATINGS = {
    "Panthers": 90,
    "Storm": 88,
    "Roosters": 85,
    "Rabbitohs": 82,
    "Broncos": 80,
    "Eels": 78,
    "Sharks": 76,
    "Sea Eagles": 74,
    "Raiders": 72,
    "Bulldogs": 70,
    "Cowboys": 68,
    "Knights": 66,
    "Dragons": 64,
    "Wests Tigers": 62,
    "Dolphins": 60,
    "Titans": 58,
    "Warriors": 56,
}

COMPETITION_IDS = {
    "nrl": "111",
    "nrlw": "161",
    "knockon": "113",
    "hostplus": "114",
}


class PredictionResponse(BaseModel):
    """Prediction response model."""
    home_team: str
    away_team: str
    home_win_probability: float
    away_win_probability: float
    predicted_winner: str
    confidence: float
    predicted_margin: float


class RoundPredictionsResponse(BaseModel):
    """Round predictions response model."""
    year: int
    round: int
    competition: str
    predictions: List[PredictionResponse]


def predict_match(home_team: str, away_team: str) -> dict:
    """Predict match outcome."""
    home_rating = TEAM_RATINGS.get(home_team, 65)
    away_rating = TEAM_RATINGS.get(away_team, 65)
    
    # Home advantage
    home_rating += 5
    
    total = home_rating + away_rating
    home_prob = home_rating / total
    
    return {
        "home_team": home_team,
        "away_team": away_team,
        "home_win_probability": round(home_prob, 3),
        "away_win_probability": round(1 - home_prob, 3),
        "predicted_winner": home_team if home_prob > 0.5 else away_team,
        "confidence": round(abs(home_prob - 0.5) * 2 * 10, 1),
        "predicted_margin": round((home_rating - away_rating) * 0.5, 1),
    }


def get_fixtures(year: int = 2026, competition: str = "111", round_num: int = None) -> List[dict]:
    """Fetch fixtures from NRL website."""
    url = f"https://www.nrl.com/draw/?competition={competition}&round={round_num}&season={year}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return []
        
        soup = BeautifulSoup(response.text, "html.parser")
        script_tag = soup.find("div", {"id": "vue-draw"})
        
        if not script_tag:
            return []
        
        raw_json = script_tag.get("q-data", "").replace(""", '"')
        data = json.loads(raw_json)
        
        fixtures = data.get("fixtures", [])
        matches = []
        
        for fixture in fixtures:
            if fixture.get("type") == "Match":
                match = {
                    "home_team": fixture["homeTeam"]["nickName"],
                    "away_team": fixture["awayTeam"]["nickName"],
                    "venue": fixture.get("venue", "TBD"),
                    "kickoff": fixture.get("kickOffTime", "TBD"),
                    "status": fixture.get("matchStatus", "Upcoming"),
                }
                matches.append(match)
        
        return matches
        
    except Exception as e:
        print(f"Error fetching fixtures: {e}")
        return []


@router.get("/predictions", response_model=RoundPredictionsResponse)
async def get_round_predictions(
    year: int = 2026,
    round: int = None,
    competition: str = "nrl"
):
    """
    Get predictions for all matches in a round.
    
    Args:
        year: Season year (default: 2026)
        round: Round number (default: current round from config)
        competition: Competition (nrl, nrlw, knockon, hostplus)
    """
    if round is None:
        try:
            round = getattr(EV, f"NRL_{year}_ROUND", 5)
        except:
            round = 5
    
    comp_id = COMPETITION_IDS.get(competition, "111")
    
    # Fetch fixtures
    fixtures = get_fixtures(year, comp_id, round)
    
    if not fixtures:
        raise HTTPException(
            status_code=404,
            detail=f"No fixtures found for Round {round}, {year}"
        )
    
    # Generate predictions
    predictions = []
    for fixture in fixtures:
        pred = predict_match(fixture["home_team"], fixture["away_team"])
        pred["venue"] = fixture["venue"]
        pred["kickoff"] = fixture["kickoff"]
        predictions.append(PredictionResponse(**pred))
    
    return RoundPredictionsResponse(
        year=year,
        round=round,
        competition=competition,
        predictions=predictions
    )


@router.get("/predictions/match")
async def get_match_prediction(
    home_team: str,
    away_team: str
):
    """
    Get prediction for a specific matchup.
    
    Args:
        home_team: Home team name
        away_team: Away team name
    """
    if home_team not in TEAM_RATINGS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown team: {home_team}"
        )
    if away_team not in TEAM_RATINGS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown team: {away_team}"
        )
    
    prediction = predict_match(home_team, away_team)
    return prediction


@router.get("/predictions/teams")
async def get_available_teams():
    """Get list of all available teams."""
    return {
        "teams": list(TEAM_RATINGS.keys()),
        "count": len(TEAM_RATINGS)
    }


@router.get("/predictions/ratings")
async def get_team_ratings():
    """Get team strength ratings."""
    return {
        "ratings": TEAM_RATINGS,
        "description": "Higher rating = stronger team"
    }

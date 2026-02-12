"""
API routes for NRL fixtures.
"""

import sys
import os
import requests
from bs4 import BeautifulSoup
import json
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ENVIRONMENT_VARIABLES as EV

router = APIRouter()

COMPETITION_IDS = {
    "nrl": "111",
    "nrlw": "161",
    "knockon": "113",
    "hostplus": "114",
}


class FixtureResponse(BaseModel):
    """Fixture response model."""
    home_team: str
    away_team: str
    venue: str
    kickoff: str
    status: str


class FixturesResponse(BaseModel):
    """Fixtures response model."""
    year: int
    round: int
    competition: str
    fixtures: List[FixtureResponse]


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


@router.get("/fixtures", response_model=FixturesResponse)
async def get_fixtures_endpoint(
    year: int = 2026,
    round: int = None,
    competition: str = "nrl"
):
    """
    Get fixtures for a specific round.
    
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
    
    fixtures = get_fixtures(year, comp_id, round)
    
    if not fixtures:
        raise HTTPException(
            status_code=404,
            detail=f"No fixtures found for Round {round}, {year}"
        )
    
    return FixturesResponse(
        year=year,
        round=round,
        competition=competition,
        fixtures=[FixtureResponse(**f) for f in fixtures]
    )


@router.get("/fixtures/next")
async def get_next_fixture(
    competition: str = "nrl"
):
    """
    Get the next upcoming fixture.
    
    Args:
        competition: Competition (nrl, nrlw, knockon, hostplus)
    """
    comp_id = COMPETITION_IDS.get(competition, "111")
    
    # Try current and next few rounds
    for round_num in range(1, 30):
        fixtures = get_fixtures(2026, comp_id, round_num)
        if fixtures:
            return {
                "round": round_num,
                "competition": competition,
                "fixtures": fixtures,
                "next_kickoff": fixtures[0].get("kickoff", "TBD")
            }
    
    raise HTTPException(
        status_code=404,
        detail="No upcoming fixtures found"
    )


@router.get("/fixtures/rounds")
async def get_available_rounds(
    year: int = 2026,
    competition: str = "nrl"
):
    """
    Get list of available rounds.
    
    Note: This returns a range as we can't know which rounds
    have fixtures without checking each one.
    """
    return {
        "year": year,
        "competition": competition,
        "available_rounds": list(range(1, 30)),
        "note": "Check /api/fixtures for actual fixture availability"
    }

"""Fixtures API routes"""
from datetime import datetime


def get_fixtures():
    """
    Get upcoming NRL fixtures for Round 1, 2026
    Returns list of scheduled matches
    """
    return {
        "round": 1,
        "year": 2026,
        "fixtures": [
            {
                "date": "2026-03-05",
                "time": "20:00 AEST",
                "home_team": "Melbourne Storm",
                "away_team": "Sydney Roosters",
                "venue": "AAMI Park"
            },
            {
                "date": "2026-03-06",
                "time": "18:00 AEST",
                "home_team": "Penrith Panthers",
                "away_team": "Brisbane Broncos",
                "venue": "BlueBet Stadium"
            },
            {
                "date": "2026-03-06",
                "time": "20:30 AEST",
                "home_team": "North Queensland Cowboys",
                "away_team": "South Sydney Rabbitohs",
                "venue": "Queensland Country Bank Stadium"
            },
            {
                "date": "2026-03-07",
                "time": "16:00 AEST",
                "home_team": "Parramatta Eels",
                "away_team": "Canterbury-Bankstown Bulldogs",
                "venue": "CommBank Stadium"
            },
            {
                "date": "2026-03-07",
                "time": "18:30 AEST",
                "home_team": "Newcastle Knights",
                "away_team": "St George Illawarra Dragons",
                "venue": "McDonald Jones Stadium"
            },
            {
                "date": "2026-03-07",
                "time": "20:30 AEST",
                "home_team": "Wests Tigers",
                "away_team": "Manly-Warringah Sea Eagles",
                "venue": "Leichhardt Oval"
            },
            {
                "date": "2026-03-08",
                "time": "18:00 AEST",
                "home_team": "Cronulla-Sutherland Sharks",
                "away_team": "Dolphins",
                "venue": "PointsBet Stadium"
            },
            {
                "date": "2026-03-08",
                "time": "20:00 AEST",
                "home_team": "Gold Coast Titans",
                "away_team": "Canberra Raiders",
                "venue": "Cbus Super Stadium"
            }
        ],
        "last_updated": datetime.now().isoformat()
    }


def get_round_fixtures(round_num, year=2026):
    """
    Get fixtures for a specific round
    """
    fixtures = get_fixtures()
    
    if "error" in fixtures:
        return fixtures
    
    fixtures["round"] = round_num
    return fixtures

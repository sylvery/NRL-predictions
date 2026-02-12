"""Fixtures API routes"""
from datetime import datetime


def get_fixtures():
    """
    Get upcoming NRL fixtures
    Returns list of scheduled matches
    """
    # Return sample fixtures - in production this would scrape NRL website
    return {
        "round": 6,
        "year": 2026,
        "fixtures": [
            {
                "date": "2026-05-10",
                "time": "19:55 AEST",
                "home_team": "Melbourne Storm",
                "away_team": "Sydney Roosters",
                "venue": "AAMI Park"
            },
            {
                "date": "2026-05-11",
                "time": "15:00 AEST",
                "home_team": "Penrith Panthers",
                "away_team": "Brisbane Broncos",
                "venue": "BlueBet Stadium"
            },
            {
                "date": "2026-05-11",
                "time": "17:30 AEST",
                "home_team": "North Queensland Cowboys",
                "away_team": "South Sydney Rabbitohs",
                "venue": "Queensland Country Bank Stadium"
            },
            {
                "date": "2026-05-11",
                "time": "19:35 AEST",
                "home_team": "Parramatta Eels",
                "away_team": "Canterbury-Bankstown Bulldogs",
                "venue": "CommBank Stadium"
            },
            {
                "date": "2026-05-12",
                "time": "18:00 AEST",
                "home_team": "Newcastle Knights",
                "away_team": "St George Illawarra Dragons",
                "venue": "McDonald Jones Stadium"
            },
            {
                "date": "2026-05-12",
                "time": "19:50 AEST",
                "home_team": "Wests Tigers",
                "away_team": "Manly-Warringah Sea Eagles",
                "venue": "Leichhardt Oval"
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
    
    # Filter by round (in a real implementation this would fetch specific round)
    return fixtures

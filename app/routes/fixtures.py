"""Fixtures API routes - NRL 2026 fixtures"""
import json
import os
from datetime import datetime

# Path to cached fixtures
CACHED_FIXTURES_PATH = os.path.join(
    os.path.dirname(__file__), 
    "..", 
    "data", 
    "fixtures_2026.json"
)


def load_cached_fixtures():
    """Load fixtures from local cached JSON file"""
    try:
        if os.path.exists(CACHED_FIXTURES_PATH):
            with open(CACHED_FIXTURES_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
    except Exception as e:
        print(f"Error loading cached fixtures: {e}")
    return None


def get_all_fixtures():
    """
    Get all NRL 2026 fixtures from cached JSON
    Falls back to empty structure if not available
    """
    data = load_cached_fixtures()
    
    if data and data.get("fixtures"):
        return data
    
    return {
        "competition": "NRL Premiership",
        "year": 2026,
        "competition_id": "111",
        "fixtures": {},
        "note": "Run 'python scripts/fetch_fixtures.py' to fetch from nrl.com",
        "generated_at": None,
        "source": "cached"
    }


def get_round_fixtures(round_num):
    """
    Get fixtures for a specific round
    """
    data = load_cached_fixtures()
    
    if data and data.get("fixtures"):
        round_str = str(round_num)
        matches = data["fixtures"].get(round_str, [])
        
        if matches:
            return {
                "round": round_num,
                "year": 2026,
                "fixtures": matches,
                "source": data.get("source", "cached"),
                "generated_at": data.get("generated_at"),
                "last_updated": datetime.now().isoformat()
            }
    
    # No fixtures found
    return {
        "round": round_num,
        "year": 2026,
        "fixtures": [],
        "note": f"Round {round_num} fixtures not found. Run 'python scripts/fetch_fixtures.py' to fetch from nrl.com",
        "last_updated": datetime.now().isoformat()
    }


def get_fixtures():
    """
    Get all fixtures - returns all rounds from cached data
    """
    data = load_cached_fixtures()
    
    if data and data.get("fixtures"):
        return {
            "year": data.get("year", 2026),
            "competition": data.get("competition", "NRL Premiership"),
            "fixtures": data.get("fixtures", {}),
            "source": data.get("source", "cached"),
            "generated_at": data.get("generated_at"),
            "last_updated": datetime.now().isoformat()
        }
    
    return {
        "year": 2026,
        "competition": "NRL Premiership",
        "fixtures": {},
        "note": "No fixtures cached. Run 'python scripts/fetch_fixtures.py' to fetch from nrl.com",
        "last_updated": datetime.now().isoformat()
    }

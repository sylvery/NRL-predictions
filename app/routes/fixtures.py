"""Fixtures API routes - Real-time NRL data"""
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime


def get_fixtures_from_nrl(year=2026, competition='111'):
    """
    Fetch real fixtures from nrl.com
    competition='111' is NRL Premiership
    """
    url = f"https://www.nrl.com/draw/?competition={competition}&season={year}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find Vue data container
        script_tag = soup.find("div", {"id": "vue-draw"})
        if not script_tag:
            return None
        
        # Extract JSON data
        raw_json = script_tag.get("q-data", "")
        if not raw_json:
            return None
        
        raw_json = raw_json.replace(""", '"')
        
        try:
            data = json.loads(raw_json)
        except json.JSONDecodeError:
            return None
        
        fixtures = data.get("fixtures", [])
        
        matches = []
        for fixture in fixtures:
            if fixture.get("type") == "Match":
                # Parse kickoff time
                kickoff_long = fixture.get("clock", {}).get("kickOffTimeLong", "")
                
                # Format the match data
                match = {
                    "date": datetime.fromtimestamp(kickoff_long/1000).strftime("%Y-%m-%d") if kickoff_long else "",
                    "time": datetime.fromtimestamp(kickoff_long/1000).strftime("%H:%M AEST") if kickoff_long else "",
                    "home_team": fixture.get("homeTeam", {}).get("nickName", "TBD"),
                    "away_team": fixture.get("awayTeam", {}).get("nickName", "TBD"),
                    "venue": fixture.get("venue", "TBD"),
                    "round": fixture.get("roundTitle", "Round TBD")
                }
                matches.append(match)
        
        return {
            "fixtures": matches,
            "year": year,
            "source": "nrl.com",
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Error fetching NRL fixtures: {e}")
        return None


def get_fixtures():
    """
    Get NRL fixtures - fetches real data from nrl.com
    Falls back to sample data if fetch fails
    """
    # Try to fetch real data from NRL
    nrl_data = get_fixtures_from_nrl(year=2026)
    
    if nrl_data and nrl_data.get("fixtures"):
        return nrl_data
    
    # Fallback - sample data (this shouldn't happen if NRL site is up)
    return {
        "round": 1,
        "year": 2026,
        "fixtures": [],
        "error": "Could not fetch from nrl.com - using placeholder data",
        "last_updated": datetime.now().isoformat()
    }


def get_round_fixtures(round_num, year=2026):
    """
    Get fixtures for a specific round from nrl.com
    """
    # NRL.com uses round filtering via URL parameters
    url = f"https://www.nrl.com/draw/?competition=111&round={round_num}&season={year}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            return get_fixtures()
        
        soup = BeautifulSoup(response.text, "html.parser")
        script_tag = soup.find("div", {"id": "vue-draw"})
        
        if not script_tag:
            return get_fixtures()
        
        raw_json = script_tag.get("q-data", "").replace(""", '"')
        
        try:
            data = json.loads(raw_json)
        except json.JSONDecodeError:
            return get_fixtures()
        
        fixtures = data.get("fixtures", [])
        matches = []
        
        for fixture in fixtures:
            if fixture.get("type") == "Match":
                kickoff_long = fixture.get("clock", {}).get("kickOffTimeLong", "")
                match = {
                    "date": datetime.fromtimestamp(kickoff_long/1000).strftime("%Y-%m-%d") if kickoff_long else "",
                    "time": datetime.fromtimestamp(kickoff_long/1000).strftime("%H:%M AEST") if kickoff_long else "",
                    "home_team": fixture.get("homeTeam", {}).get("nickName", "TBD"),
                    "away_team": fixture.get("awayTeam", {}).get("nickName", "TBD"),
                    "venue": fixture.get("venue", "TBD"),
                    "round": fixture.get("roundTitle", f"Round {round_num}")
                }
                matches.append(match)
        
        return {
            "round": round_num,
            "year": year,
            "fixtures": matches,
            "source": "nrl.com",
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Error fetching round {round_num} fixtures: {e}")
        return get_fixtures()

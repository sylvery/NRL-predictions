"""Fixtures API routes - Real-time NRL data"""
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

# Try to import from parent project, otherwise use hardcoded values
try:
    sys.path.append("..")
    import ENVIRONMENT_VARIABLES as EV
    DATA_WEBSITE = getattr(EV, 'DATA_WEBSITE', 'https://geo145327-staging.s3.ap-southeast-2.amazonaws.com/public/')
except:
    DATA_WEBSITE = 'https://geo145327-staging.s3.ap-southeast-2.amazonaws.com/public/'


def get_fixtures_from_s3(year=2026, competition='HOSTPLUS'):
    """
    Try to fetch fixtures from pre-built S3 JSON files
    This is more reliable than scraping nrl.com
    """
    filename = f"{competition}_data_{year}.json"
    url = f"{DATA_WEBSITE}{competition}/{year}/{filename}"
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            
            # Parse the data into our format
            fixtures = []
            for competition_data in data.get(competition, []):
                year_data = competition_data.get(str(year), [])
                for round_data in year_data:
                    if round_data:
                        for match in round_data.values():
                            if isinstance(match, list):
                                for m in match:
                                    fixtures.append({
                                        "date": "",
                                        "time": "",
                                        "home_team": m.get("Home", "TBD"),
                                        "away_team": m.get("Away", "TBD"),
                                        "venue": m.get("Venue", "TBD"),
                                        "round": m.get("Round", "Round TBD")
                                    })
            
            return {
                "fixtures": fixtures,
                "year": year,
                "source": "S3 Data Store",
                "last_updated": datetime.now().isoformat()
            }
    except Exception as e:
        print(f"S3 fetch error: {e}")
    
    return None


def get_fixtures_from_nrl(year=2026, competition='111'):
    """
    Fetch fixtures from nrl.com using their Vue.js data
    Note: This may not work if nrl.com has changed their website structure
    """
    url = f"https://www.nrl.com/draw/?competition={competition}&season={year}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Try multiple methods to find fixture data
        methods = [
            # Method 1: vue-draw div with q-data
            lambda: soup.find("div", {"id": "vue-draw"}),
            # Method 2: Look for script tags with JSON
            lambda: soup.find("script", {"type": "application/ld+json"}),
            # Method 3: Look for any script with fixture data
            lambda: soup.find("script", string=lambda x: x and "fixtures" in x.lower() if x else False),
        ]
        
        for i, method in enumerate(methods):
            try:
                tag = method()
                if tag:
                    if tag.name == "div":
                        raw_json = tag.get("q-data", "")
                    elif tag.name == "script" and tag.get("type") == "application/ld+json":
                        raw_json = tag.string or ""
                    else:
                        raw_json = tag.string or ""
                    
                    if raw_json:
                        from html import unescape
                        raw_json = unescape(raw_json)
                        
                        try:
                            data = json.loads(raw_json)
                        except json.JSONDecodeError:
                            continue
                        
                        # Handle different data structures
                        fixtures_data = data.get("fixtures", data.get("data", []))
                        
                        matches = []
                        for fixture in fixtures_data:
                            if isinstance(fixture, dict) and fixture.get("type") == "Match":
                                kickoff_long = fixture.get("clock", {}).get("kickOffTimeLong", "")
                                match = {
                                    "date": datetime.fromtimestamp(kickoff_long/1000).strftime("%Y-%m-%d") if kickoff_long else "",
                                    "time": datetime.fromtimestamp(kickoff_long/1000).strftime("%H:%M AEST") if kickoff_long else "",
                                    "home_team": fixture.get("homeTeam", {}).get("nickName", "TBD"),
                                    "away_team": fixture.get("awayTeam", {}).get("nickName", "TBD"),
                                    "venue": fixture.get("venue", "TBD"),
                                    "round": fixture.get("roundTitle", "Round TBD")
                                }
                                matches.append(match)
                        
                        if matches:
                            return {
                                "fixtures": matches,
                                "year": year,
                                "source": f"nrl.com (method {i+1})",
                                "last_updated": datetime.now().isoformat()
                            }
            except Exception as e:
                print(f"Method {i+1} failed: {e}")
                continue
        
        return None
        
    except Exception as e:
        print(f"NRL fetch error: {e}")
        return None


def get_fixtures():
    """
    Get NRL fixtures - tries multiple sources in order:
    1. S3 data store (most reliable)
    2. nrl.com scraping
    3. Placeholder data with explanation
    """
    # Try S3 first
    s3_data = get_fixtures_from_s3(year=2026, competition='HOSTPLUS')
    if s3_data and s3_data.get("fixtures"):
        return s3_data
    
    # Try NRL.com
    nrl_data = get_fixtures_from_nrl(year=2026)
    if nrl_data and nrl_data.get("fixtures"):
        return nrl_data
    
    # Return informative message
    return {
        "round": 1,
        "year": 2026,
        "fixtures": [],
        "note": "2026 NRL fixtures are not yet available. The season typically starts in March.",
        "sources_tried": ["S3 Data Store", "nrl.com"],
        "last_updated": datetime.now().isoformat()
    }


def get_round_fixtures(round_num, year=2026):
    """
    Get fixtures for a specific round
    """
    # Try S3
    s3_data = get_fixtures_from_s3(year=year, competition='HOSTPLUS')
    if s3_data and s3_data.get("fixtures"):
        # Filter by round
        round_fixtures = [f for f in s3_data["fixtures"] if str(round_num) in str(f.get("round", ""))]
        if round_fixtures:
            return {
                "round": round_num,
                "year": year,
                "fixtures": round_fixtures,
                "source": "S3 Data Store",
                "last_updated": datetime.now().isoformat()
            }
    
    # Try NRL.com
    nrl_data = get_fixtures_from_nrl(year=year)
    if nrl_data and nrl_data.get("fixtures"):
        round_fixtures = [f for f in nrl_data["fixtures"] if str(round_num) in str(f.get("round", ""))]
        if round_fixtures:
            return {
                "round": round_num,
                "year": year,
                "fixtures": round_fixtures,
                "source": "nrl.com",
                "last_updated": datetime.now().isoformat()
            }
    
    return {
        "round": round_num,
        "year": year,
        "fixtures": [],
        "note": f"Round {round_num} fixtures not available. 2026 season may not be published yet.",
        "last_updated": datetime.now().isoformat()
    }

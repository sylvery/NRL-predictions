#!/usr/bin/env python3
"""
Fetch all NRL 2026 fixtures from nrl.com and store in JSON
Usage: python scripts/fetch_fixtures.py
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

def fetch_round_fixtures(round_num, year=2026, competition='111'):
    """Fetch fixtures for a specific round from nrl.com"""
    url = f"https://www.nrl.com/draw/?competition={competition}&round={round_num}&season={year}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    
    print(f"Fetching Round {round_num}...")
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            print(f"  ❌ Failed to fetch round {round_num}: Status {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find Vue data container
        script_tag = soup.find("div", {"id": "vue-draw"})
        if not script_tag:
            print(f"  ❌ Could not find vue-draw container for round {round_num}")
            return None
        
        raw_json = script_tag.get("q-data", "")
        if not raw_json:
            print(f"  ❌ No q-data found for round {round_num}")
            return None
        
        # Parse JSON
        from html import unescape
        raw_json = unescape(raw_json)
        
        try:
            data = json.loads(raw_json)
        except json.JSONDecodeError as e:
            print(f"  ❌ JSON decode error for round {round_num}: {e}")
            return None
        
        fixtures = data.get("fixtures", [])
        
        matches = []
        for fixture in fixtures:
            if fixture.get("type") == "Match":
                kickoff_long = fixture.get("clock", {}).get("kickOffTimeLong", "")
                match = {
                    "round": fixture.get("roundTitle", f"Round {round_num}"),
                    "date": datetime.fromtimestamp(kickoff_long/1000).strftime("%Y-%m-%d") if kickoff_long else "",
                    "time": datetime.fromtimestamp(kickoff_long/1000).strftime("%H:%M AEST") if kickoff_long else "",
                    "home_team": fixture.get("homeTeam", {}).get("nickName", "TBD"),
                    "away_team": fixture.get("awayTeam", {}).get("nickName", "TBD"),
                    "venue": fixture.get("venue", "TBD"),
                    "home_team_full": fixture.get("homeTeam", {}).get("name", "TBD"),
                    "away_team_full": fixture.get("awayTeam", {}).get("name", "TBD"),
                }
                matches.append(match)
        
        if matches:
            print(f"  ✅ Found {len(matches)} matches for Round {round_num}")
        else:
            print(f"  ⚠️ No matches found for Round {round_num}")
        
        return matches
        
    except Exception as e:
        print(f"  ❌ Error fetching round {round_num}: {e}")
        return None


def fetch_all_fixtures():
    """Fetch fixtures for all rounds (1-26)"""
    all_fixtures = {}
    
    print("=" * 50)
    print("NRL 2026 Fixture Fetcher")
    print("=" * 50)
    
    for round_num in range(1, 27):  # NRL has 26 rounds + finals
        matches = fetch_round_fixtures(round_num)
        if matches:
            all_fixtures[round_num] = matches
    
    return all_fixtures


def save_fixtures(fixtures, filepath="app/data/fixtures_2026.json"):
    """Save fixtures to JSON file"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    output = {
        "competition": "NRL Premiership",
        "year": 2026,
        "competition_id": "111",
        "fixtures": fixtures,
        "generated_at": datetime.now().isoformat(),
        "source": "nrl.com"
    }
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Saved fixtures to {filepath}")
    print(f"📊 Total matches: {sum(len(matches) for matches in fixtures.values())}")


if __name__ == "__main__":
    fixtures = fetch_all_fixtures()
    if fixtures:
        save_fixtures(fixtures)
    else:
        print("\n❌ No fixtures fetched. Check nrl.com manually.")

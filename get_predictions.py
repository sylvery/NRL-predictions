#!/usr/bin/env python3
"""
NRL Predictions - Simple CLI Tool

Usage:
    python get_predictions.py              # Show this week's predictions
    python get_predictions.py --round 5   # Show predictions for Round 5
    python get_predictions.py --html       # Generate HTML report
    python get_predictions.py --all       # Show all rounds

No technical knowledge required - just run the script!
"""

import requests
from bs4 import BeautifulSoup
import json
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Team strength ratings (updated for 2026 season)
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

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NRL Predictions</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #fff;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        h1 {{
            text-align: center;
            color: #00d4ff;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .subtitle {{
            text-align: center;
            color: #888;
            margin-bottom: 30px;
        }}
        .match-card {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .match-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        .round-badge {{
            background: #00d4ff;
            color: #000;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
        }}
        .teams {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 20px 0;
        }}
        .team {{
            text-align: center;
            flex: 1;
        }}
        .team-name {{
            font-size: 1.4em;
            font-weight: bold;
            margin-top: 10px;
        }}
        .vs {{
            font-size: 1.2em;
            color: #888;
            padding: 0 20px;
        }}
        .prediction {{
            background: rgba(0, 212, 255, 0.2);
            border-radius: 10px;
            padding: 15px;
            margin-top: 15px;
        }}
        .winner {{
            color: #00d4ff;
            font-weight: bold;
            font-size: 1.2em;
        }}
        .confidence {{
            color: #888;
            font-size: 0.9em;
        }}
        .prob-bar {{
            height: 8px;
            background: #333;
            border-radius: 4px;
            margin: 10px 0;
            overflow: hidden;
        }}
        .prob-fill {{
            height: 100%;
            border-radius: 4px;
        }}
        .home-prob {{
            background: linear-gradient(90deg, #00d4ff, #00ff88);
        }}
        .away-prob {{
            background: linear-gradient(90deg, #ff6b6b, #ffa500);
        }}
        .venue {{
            color: #888;
            font-size: 0.9em;
            text-align: center;
            margin-top: 10px;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            color: #666;
            font-size: 0.8em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🏉 NRL Predictions</h1>
        <p class="subtitle">Round {round_num} - {year}</p>
        
        {matches_html}
        
        <div class="footer">
            <p>Generated on {datetime}</p>
            <p>Powered by ML Predictions</p>
        </div>
    </div>
</body>
</html>
"""


def get_fixtures(year=2026, competition='111', round_num=None):
    """Fetch fixtures from NRL website."""
    url = f"https://www.nrl.com/draw/?competition={competition}&round={round_num}&season={year}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error: Could not fetch fixtures (status {response.status_code})")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    script_tag = soup.find("div", {"id": "vue-draw"})
    
    if not script_tag:
        print("Error: Could not find fixture data on NRL website")
        return []
    
    try:
        raw_json = script_tag.get("q-data", "").replace(""", '"')
        data = json.loads(raw_json)
        
        fixtures = data.get("fixtures", [])
        matches = []
        
        for fixture in fixtures:
            if fixture.get("type") == "Match":
                match = {
                    "round": fixture.get("roundTitle", f"Round {round_num}"),
                    "home_team": fixture["homeTeam"]["nickName"],
                    "away_team": fixture["awayTeam"]["nickName"],
                    "venue": fixture.get("venue", "TBD"),
                    "kickoff": fixture.get("kickOffTime", "TBD"),
                }
                matches.append(match)
        
        return matches
        
    except Exception as e:
        print(f"Error parsing fixture data: {e}")
        return []


def predict_match(home_team, away_team):
    """Predict match outcome."""
    home_rating = TEAM_RATINGS.get(home_team, 65)
    away_rating = TEAM_RATINGS.get(away_team, 65)
    
    # Home advantage
    home_rating += 5
    
    total = home_rating + away_rating
    home_prob = home_rating / total
    
    return {
        "home_win_prob": home_prob,
        "away_win_prob": 1 - home_prob,
        "predicted_winner": home_team if home_prob > 0.5 else away_team,
        "confidence": round(abs(home_prob - 0.5) * 2 * 10, 1),
    }


def print_predictions(matches, competition="NRL"):
    """Print predictions to console."""
    print("\n" + "="*60)
    print(f"  🏉 NRL PREDICTIONS - {matches[0]['round'] if matches else 'N/A'}")
    print("="*60)
    print()
    
    for i, match in enumerate(matches, 1):
        pred = predict_match(match['home_team'], match['away_team'])
        
        home_bar = "█" * int(pred['home_win_prob'] * 20)
        away_bar = "█" * int(pred['away_win_prob'] * 20)
        
        print(f"MATCH {i}: {match['home_team']} vs {match['away_team']}")
        print("-" * 50)
        print(f"  🏠 {match['home_team']:<15} {pred['home_win_prob']:.0%} {home_bar}")
        print(f"  ✈️  {match['away_team']:<15} {pred['away_win_prob']:.0%} {away_bar}")
        print(f"  🎯 Predicted Winner: {pred['predicted_winner']}")
        print(f"  📊 Confidence: {pred['confidence']}/10")
        print(f"  📍 Venue: {match['venue']}")
        print(f"  🕐 Kickoff: {match['kickoff']}")
        print()
    
    print("="*60)
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)


def generate_html(matches, round_num=1, year=2026):
    """Generate HTML report."""
    matches_html = ""
    
    for match in matches:
        pred = predict_match(match['home_team'], match['away_team'])
        
        home_color = "#00ff88" if pred['predicted_winner'] == match['home_team'] else "#888"
        away_color = "#ff6b6b" if pred['predicted_winner'] == match['away_team'] else "#888"
        
        matches_html += f"""
        <div class="match-card">
            <div class="match-header">
                <span>{match['round']}</span>
                <span class="venue">{match['venue']}</span>
            </div>
            <div class="teams">
                <div class="team">
                    <div class="team-name">{match['home_team']}</div>
                </div>
                <div class="vs">VS</div>
                <div class="team">
                    <div class="team-name">{match['away_team']}</div>
                </div>
            </div>
            <div class="prediction">
                <div class="winner">🎯 Predicted: {pred['predicted_winner']}</div>
                <div class="confidence">Confidence: {pred['confidence']}/10</div>
                <div class="prob-bar">
                    <div class="prob-fill home-prob" style="width: {pred['home_win_prob']*100}%"></div>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.8em;">
                    <span>{match['home_team']}: {pred['home_win_prob']:.0%}</span>
                    <span>{match['away_team']}: {pred['away_win_prob']:.0%}</span>
                </div>
            </div>
            <div class="venue">🕐 {match['kickoff']}</div>
        </div>
        """
    
    html = HTML_TEMPLATE.format(
        round_num=round_num,
        year=year,
        matches_html=matches_html,
        datetime=datetime.now().strftime("%Y-%m-%d %H:%M")
    )
    
    return html


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Get NRL predictions for upcoming matches"
    )
    parser.add_argument(
        "--round", "-r",
        type=int,
        help="Round number (default: current round from config)"
    )
    parser.add_argument(
        "--year", "-y",
        type=int,
        default=2026,
        help="Season year (default: 2026)"
    )
    parser.add_argument(
        "--html",
        action="store_true",
        help="Generate HTML report instead of console output"
    )
    parser.add_argument(
        "--competition", "-c",
        choices=["nrl", "nrlw", "knockon", "hostplus"],
        default="nrl",
        help="Competition (default: nrl)"
    )
    
    args = parser.parse_args()
    
    # Get round from args or config
    round_num = args.round
    if round_num is None:
        try:
            import ENVIRONMENT_VARIABLES as EV
            round_num = getattr(EV, f"NRL_{args.year}_ROUND", 5)
        except:
            round_num = 5  # Default
    
    comp_id = COMPETITION_IDS.get(args.competition, "111")
    
    print(f"\n📅 Fetching {args.competition.upper()} fixtures for Round {round_num}, {args.year}...\n")
    
    # Fetch fixtures
    matches = get_fixtures(args.year, comp_id, round_num)
    
    if not matches:
        print("⚠️ No matches found. The round may not be released yet.")
        print("   Try specifying a different round: python get_predictions.py --round 5")
        return
    
    if args.html:
        # Generate HTML
        html = generate_html(matches, round_num, args.year)
        filename = f"predictions_round_{round_num}.html"
        with open(filename, 'w') as f:
            f.write(html)
        print(f"✅ HTML report generated: {filename}")
        print(f"   Open {filename} in your browser to view predictions")
    else:
        # Print to console
        print_predictions(matches, args.competition)


if __name__ == "__main__":
    main()

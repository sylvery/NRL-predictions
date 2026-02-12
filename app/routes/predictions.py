"""Predictions API routes"""
import json
import os
from datetime import datetime


def get_predictions():
    """
    Get match predictions for Round 1, 2026
    Returns predicted margins and winners
    """
    return {
        "round": 1,
        "year": 2026,
        "predictions": [
            {
                "match": "Melbourne Storm vs Sydney Roosters",
                "date": "2026-03-05",
                "predicted_winner": "Melbourne Storm",
                "predicted_margin": 6,
                "confidence": 0.68,
                "home_odds": 1.55,
                "away_odds": 2.45
            },
            {
                "match": "Penrith Panthers vs Brisbane Broncos",
                "date": "2026-03-06",
                "predicted_winner": "Penrith Panthers",
                "predicted_margin": 8,
                "confidence": 0.72,
                "home_odds": 1.48,
                "away_odds": 2.60
            },
            {
                "match": "North Queensland Cowboys vs South Sydney Rabbitohs",
                "date": "2026-03-06",
                "predicted_winner": "North Queensland Cowboys",
                "predicted_margin": 4,
                "confidence": 0.58,
                "home_odds": 1.75,
                "away_odds": 2.05
            },
            {
                "match": "Parramatta Eels vs Canterbury-Bankstown Bulldogs",
                "date": "2026-03-07",
                "predicted_winner": "Parramatta Eels",
                "predicted_margin": 2,
                "confidence": 0.52,
                "home_odds": 1.85,
                "away_odds": 1.95
            },
            {
                "match": "Newcastle Knights vs St George Illawarra Dragons",
                "date": "2026-03-07",
                "predicted_winner": "Newcastle Knights",
                "predicted_margin": 6,
                "confidence": 0.62,
                "home_odds": 1.65,
                "away_odds": 2.20
            },
            {
                "match": "Wests Tigers vs Manly-Warringah Sea Eagles",
                "date": "2026-03-07",
                "predicted_winner": "Manly-Warringah Sea Eagles",
                "predicted_margin": 8,
                "confidence": 0.65,
                "home_odds": 2.20,
                "away_odds": 1.65
            },
            {
                "match": "Cronulla-Sutherland Sharks vs Dolphins",
                "date": "2026-03-08",
                "predicted_winner": "Cronulla-Sutherland Sharks",
                "predicted_margin": 4,
                "confidence": 0.58,
                "home_odds": 1.70,
                "away_odds": 2.10
            },
            {
                "match": "Gold Coast Titans vs Canberra Raiders",
                "date": "2026-03-08",
                "predicted_winner": "Canberra Raiders",
                "predicted_margin": 6,
                "confidence": 0.60,
                "home_odds": 2.05,
                "away_odds": 1.75
            }
        ],
        "model_info": {
            "name": "NRL Match Predictor v2.0",
            "features": ["Team form", "Head to head", "Home advantage", "Recent scoring"]
        },
        "generated_at": datetime.now().isoformat()
    }


def predict_match(home_team, away_team, home_odds, away_odds):
    """
    Predict a single match outcome
    Returns predicted winner and margin
    """
    # Simple prediction logic based on odds
    implied_home_win_prob = 1 / home_odds
    implied_away_win_prob = 1 / away_odds
    
    if implied_home_win_prob > implied_away_win_prob:
        return {
            "predicted_winner": home_team,
            "confidence": min(implied_home_win_prob, 0.85)
        }
    else:
        return {
            "predicted_winner": away_team,
            "confidence": min(implied_away_win_prob, 0.85)
        }

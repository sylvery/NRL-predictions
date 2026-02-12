"""Predictions API routes"""
import json
import os
from datetime import datetime


def get_predictions():
    """
    Get match predictions for upcoming rounds
    Returns predicted margins and winners
    """
    try:
        predictions_file = os.path.join(
            os.path.dirname(__file__), 
            "..", 
            "data", 
            "predictions.json"
        )
        
        if os.path.exists(predictions_file):
            with open(predictions_file, 'r') as f:
                return json.load(f)
        
        # Return sample predictions if no file exists
        return {
            "round": 6,
            "year": 2026,
            "predictions": [
                {
                    "match": "Melbourne Storm vs Sydney Roosters",
                    "predicted_winner": "Melbourne Storm",
                    "predicted_margin": 8,
                    "confidence": 0.72
                },
                {
                    "match": "Penrith Panthers vs Brisbane Broncos",
                    "predicted_winner": "Penrith Panthers",
                    "predicted_margin": 12,
                    "confidence": 0.78
                }
            ],
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}


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

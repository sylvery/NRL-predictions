"""
Match Data to Text Converter

Converts NRL match JSON data to human-readable text format.
"""

import json
import os
import logging
from typing import List, Dict, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MatchToTxtConverter:
    """Convert NRL match data from JSON to formatted text."""
    
    def __init__(self, years: List[int], output_dir: str = "../data/txt/matches"):
        """
        Initialize the converter.
        
        Args:
            years: List of years to convert
            output_dir: Directory to save text files
        """
        self.years = years
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Initialized MatchToTxtConverter for years: {years}")
    
    def load_json_data(self, year: int) -> Optional[Dict]:
        """Load match data for a specific year."""
        filename = f"../data/nrl_data_{year}.json"
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            logger.info(f"✅ Loaded {filename}")
            return data
        except FileNotFoundError:
            logger.warning(f"⚠️ File not found: {filename}")
            return None
    
    def format_match(self, match_data: Dict, round_num: int) -> str:
        """
        Format a single match into text.
        
        Args:
            match_data: Match information dictionary
            round_num: Round number
            
        Returns:
            Formatted match string
        """
        lines = []
        lines.append("=" * 60)
        lines.append(f"NRL MATCH REPORT")
        lines.append("=" * 60)
        lines.append(f"Round: {round_num}")
        lines.append("")
        
        # Home team
        home = match_data.get('Home', 'Unknown')
        home_score = match_data.get('Home_Score', '0')
        lines.append(f"HOME TEAM: {home}")
        lines.append(f"Score: {home_score}")
        lines.append("")
        
        # Away team
        away = match_data.get('Away', 'Unknown')
        away_score = match_data.get('Away_Score', '0')
        lines.append(f"AWAY TEAM: {away}")
        lines.append(f"Score: {away_score}")
        lines.append("")
        
        # Result
        try:
            h_score = int(home_score)
            a_score = int(away_score)
            if h_score > a_score:
                winner = home
            elif a_score > h_score:
                winner = away
            else:
                winner = "DRAW"
            margin = abs(h_score - a_score)
            lines.append(f"RESULT: {winner} by {margin} points")
        except ValueError:
            lines.append("RESULT: Unknown")
        
        lines.append("")
        
        # Additional info
        if 'Date' in match_data:
            lines.append(f"Date: {match_data['Date']}")
        if 'Venue' in match_data:
            lines.append(f"Venue: {match_data['Venue']}")
        if 'Details' in match_data:
            lines.append(f"Details: {match_data['Details']}")
        
        lines.append("=" * 60)
        lines.append("")
        
        return "\n".join(lines)
    
    def format_round(self, round_data: Dict, year: int, round_num: int) -> str:
        """
        Format all matches in a round.
        
        Args:
            round_data: Round data dictionary
            year: Season year
            round_num: Round number
            
        Returns:
            Formatted round string
        """
        lines = []
        lines.append("")
        lines.append("#" * 70)
        lines.append(f"# NRL ROUND {round_num} - {year}")
        lines.append("#" * 70)
        lines.append("")
        
        for match_key, match_info in round_data.items():
            lines.append(self.format_match(match_info, round_num))
        
        return "\n".join(lines)
    
    def format_season(self, year_data: Dict, year: int) -> str:
        """
        Format all rounds in a season.
        
        Args:
            year_data: Season data dictionary
            year: Season year
            
        Returns:
            Formatted season string
        """
        lines = []
        lines.append("")
        lines.append("*" * 70)
        lines.append(f"* NRL SEASON {year}")
        lines.append("*" * 70)
        lines.append("")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        # Process each round
        for round_num in range(len(year_data)):
            if str(round_num + 1) in year_data[round_num]:
                round_str = year_data[round_num][str(round_num + 1)]
                lines.append(self.format_round(round_str, year, round_num + 1))
        
        return "\n".join(lines)
    
    def convert_year(self, year: int) -> str:
        """
        Convert a single year's data to text.
        
        Args:
            year: Year to convert
            
        Returns:
            Path to output file
        """
        data = self.load_json_data(year)
        if not data:
            return None
        
        output_file = os.path.join(self.output_dir, f"nrl_matches_{year}.txt")
        
        if 'NRL' in data:
            content = self.format_season(data['NRL'], year)
        else:
            logger.warning(f"No NRL data found for {year}")
            return None
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"✅ Saved: {output_file}")
        return output_file
    
    def convert_all(self) -> List[str]:
        """
        Convert all configured years to text.
        
        Returns:
            List of output file paths
        """
        output_files = []
        for year in self.years:
            output_file = self.convert_year(year)
            if output_file:
                output_files.append(output_file)
        
        logger.info(f"📊 Converted {len(output_files)} years of match data")
        return output_files


def main():
    """Run the converter for all configured years."""
    import sys
    sys.path.append('..')
    import ENVIRONMENT_VARIABLES as EV
    
    # Convert all years from 2001 to 2026
    years = list(range(2001, 2027))
    
    converter = MatchToTxtConverter(years)
    converter.convert_all()


if __name__ == "__main__":
    main()

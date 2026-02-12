"""
Player Data to Text Converter

Converts NRL player statistics JSON data to human-readable text format.
"""

import json
import os
import logging
from typing import List, Dict, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class PlayerToTxtConverter:
    """Convert NRL player statistics from JSON to formatted text."""
    
    def __init__(self, years: List[int], output_dir: str = "../data/txt/players"):
        """
        Initialize the converter.
        
        Args:
            years: List of years to convert
            output_dir: Directory to save text files
        """
        self.years = years
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Initialized PlayerToTxtConverter for years: {years}")
    
    def load_json_data(self, year: int) -> Optional[Dict]:
        """Load player data for a specific year."""
        filename = f"../data/nrl_player_statistics_{year}.json"
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            logger.info(f"✅ Loaded {filename}")
            return data
        except FileNotFoundError:
            logger.warning(f"⚠️ File not found: {filename}")
            return None
    
    def format_player_stats(self, player_data: Dict) -> str:
        """
        Format a single player's statistics into text.
        
        Args:
            player_data: Player statistics dictionary
            
        Returns:
            Formatted player string
        """
        lines = []
        lines.append("-" * 50)
        
        # Player name
        name = player_data.get('Name', 'Unknown')
        lines.append(f"Player: {name}")
        
        # Key stats
        key_stats = [
            ('Team', 'Team'),
            ('Position', 'Position'),
            ('Games', 'Games'),
            ('Tries', 'Tries'),
            ('Points', 'Points'),
            ('Line Breaks', 'Line Breaks'),
            ('Try Assists', 'Try Assists'),
            ('All Run Metres', 'All Run Metres'),
            ('Tackles Made', 'Tackles Made'),
        ]
        
        for label, key in key_stats:
            if key in player_data:
                lines.append(f"{label}: {player_data[key]}")
        
        # Additional stats if available
        additional = [
            ('Conversions', 'Conversions'),
            ('Penalty Goals', 'Penalty Goals'),
            ('Offloads', 'Offloads'),
            ('Tackle Breaks', 'Tackle Breaks'),
            ('Average Play The Ball Speed', 'Average Play The Ball Speed'),
        ]
        
        for label, key in additional:
            if key in player_data:
                lines.append(f"{label}: {player_data[key]}")
        
        lines.append("-" * 50)
        
        return "\n".join(lines)
    
    def format_team_players(self, team_data: Dict, team_name: str) -> str:
        """
        Format all players for a team.
        
        Args:
            team_data: Team player data
            team_name: Name of the team
            
        Returns:
            Formatted team string
        """
        lines = []
        lines.append("")
        lines.append("=" * 60)
        lines.append(f"TEAM: {team_name.upper()}")
        lines.append("=" * 60)
        lines.append("")
        
        for player_name, player_stats in team_data.items():
            lines.append(self.format_player_stats(player_stats))
        
        return "\n".join(lines)
    
    def format_season(self, year_data: Dict, year: int) -> str:
        """
        Format all players in a season.
        
        Args:
            year_data: Season data dictionary
            year: Season year
            
        Returns:
            Formatted season string
        """
        lines = []
        lines.append("")
        lines.append("*" * 70)
        lines.append(f"* NRL PLAYER STATISTICS - {year}")
        lines.append("*" * 70)
        lines.append("")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        if 'PlayerStats' in year_data:
            for team_data in year_data['PlayerStats']:
                if isinstance(team_data, dict):
                    for team_name, players in team_data.items():
                        if isinstance(players, list):
                            for player in players:
                                if isinstance(player, dict):
                                    lines.append(self.format_player_stats(player))
        
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
        
        output_file = os.path.join(self.output_dir, f"nrl_players_{year}.txt")
        
        content = self.format_season(data, year)
        
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
        
        logger.info(f"📊 Converted {len(output_files)} years of player data")
        return output_files


def main():
    """Run the converter for all configured years."""
    import sys
    sys.path.append('..')
    import ENVIRONMENT_VARIABLES as EV
    
    # Convert all years from 2001 to 2026
    years = list(range(2001, 2027))
    
    converter = PlayerToTxtConverter(years)
    converter.convert_all()


if __name__ == "__main__":
    main()

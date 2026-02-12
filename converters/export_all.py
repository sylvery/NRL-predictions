"""
Batch Export Script

Exports all NRL data (matches, players, detailed stats) to text format.

Usage:
    python export_all.py
"""

import os
import sys
import logging
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def export_matches():
    """Export all match data to text."""
    from match_to_txt import MatchToTxtConverter
    
    logger.info("=" * 60)
    logger.info("EXPORTING MATCH DATA")
    logger.info("=" * 60)
    
    years = list(range(2001, 2027))
    converter = MatchToTxtConverter(years)
    files = converter.convert_all()
    
    logger.info(f"✅ Exported {len(files)} match files")
    return files


def export_players():
    """Export all player data to text."""
    from player_to_txt import PlayerToTxtConverter
    
    logger.info("=" * 60)
    logger.info("EXPORTING PLAYER DATA")
    logger.info("=" * 60)
    
    years = list(range(2001, 2027))
    converter = PlayerToTxtConverter(years)
    files = converter.convert_all()
    
    logger.info(f"✅ Exported {len(files)} player files")
    return files


def export_detailed_stats():
    """Export detailed match statistics to text."""
    logger.info("=" * 60)
    logger.info("EXPORTING DETAILED MATCH STATISTICS")
    logger.info("=" * 60)
    
    years = list(range(2001, 2027))
    output_dir = "../data/txt/detailed"
    os.makedirs(output_dir, exist_ok=True)
    
    files_exported = 0
    
    for year in years:
        input_file = f"../data/nrl_detailed_match_data_{year}.json"
        output_file = f"{output_dir}/nrl_detailed_{year}.txt"
        
        if os.path.exists(input_file):
            try:
                with open(input_file, 'r') as f:
                    data = json.load(f)
                
                with open(output_file, 'w') as f:
                    f.write(f"NRL DETAILED MATCH STATISTICS - {year}\n")
                    f.write(f"Generated: {datetime.now()}\n")
                    f.write("=" * 60 + "\n\n")
                    
                    if 'NRL' in data:
                        for round_data in data['NRL']:
                            for match_name, match_info in round_data.items():
                                f.write(f"\nMATCH: {match_name}\n")
                                f.write("-" * 40 + "\n")
                                f.write(json.dumps(match_info, indent=2))
                                f.write("\n")
                    
                    files_exported += 1
                    logger.info(f"✅ Exported: {output_file}")
            except Exception as e:
                logger.error(f"❌ Error exporting {year}: {e}")
    
    logger.info(f"✅ Exported {files_exported} detailed match files")
    return files_exported


def main():
    """Run all exports."""
    logger.info("=" * 60)
    logger.info("NRL DATA EXPORT - TEXT FORMAT")
    logger.info(f"Started: {datetime.now()}")
    logger.info("=" * 60)
    
    total_files = 0
    
    # Export all data types
    total_files += len(export_matches())
    total_files += len(export_players())
    total_files += export_detailed_stats()
    
    logger.info("=" * 60)
    logger.info(f"EXPORT COMPLETE")
    logger.info(f"Total files exported: {total_files}")
    logger.info(f"Finished: {datetime.now()}")
    logger.info("=" * 60)


if __name__ == "__main__":
    import json
    main()

"""
Script to run the data scraper for match and player data.
"""

import os
import logging
from typing import List

from match_data_select import match_data_select
from match_data_detailed_select import match_data_detailed_select
from player_data_select import player_data_select

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the selection type for the dataset
# Options: 'NRL', 'NRLW', 'HOSTPLUS', 'KNOCKON'
SELECTION_TYPE = 'NRL'

# Define the years to fetch data for (dynamic generation)
# Update START_YEAR to add more historical data
START_YEAR = 2001
END_YEAR = 2026  # Include 2026 data
SELECT_YEARS = list(range(START_YEAR, END_YEAR + 1))

# Default rounds per year - can be customized per year if needed
DEFAULT_ROUND = 33  # Assuming 33 rounds for a full season
SELECT_ROUNDS = [DEFAULT_ROUND] * len(SELECT_YEARS)

# Loop through each year and its respective round
for year, rounds in zip(SELECT_YEARS, SELECT_ROUNDS):
    print(f"Starting data collection for Year: {year}, Round: {rounds}")

    # Define the directory path for storing scraped data
    directory_path = f"../data/{SELECTION_TYPE}/{year}/"

    # Ensure the directory exists; create it if it doesn't
    os.makedirs(directory_path, exist_ok=True)

    # Call functions to scrape and process match and player data
    match_data_select(year, rounds, SELECTION_TYPE)            # Basic match data
    match_data_detailed_select(year, rounds, SELECTION_TYPE)   # Detailed match data
    player_data_select(year, rounds, SELECTION_TYPE)           # Player statistics

print("Data scraping process completed successfully.")

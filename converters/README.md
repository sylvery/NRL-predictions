# NRL Data Converters

Converters to transform NRL JSON data into human-readable text format.

## Overview

This module provides tools to convert JSON data exports into plain text format for:
- Match reports
- Player statistics
- Detailed match statistics

## Usage

### Individual Converters

#### Match Data Export
```bash
cd converters
python match_to_txt.py
```
Exports match data to `../data/txt/matches/nrl_matches_{year}.txt`

#### Player Data Export
```bash
cd converters
python player_to_txt.py
```
Exports player data to `../data/txt/players/nrl_players_{year}.txt`

#### Batch Export
```bash
cd converters
python export_all.py
```
Exports all data types (matches, players, detailed stats) to text format.

### Programmatic Usage

#### Match Converter
```python
from match_to_txt import MatchToTxtConverter

# Initialize for specific years
converter = MatchToTxtConverter(years=[2024, 2025, 2026])

# Convert single year
converter.convert_year(2026)

# Convert all configured years
converter.convert_all()
```

#### Player Converter
```python
from player_to_txt import PlayerToTxtConverter

# Initialize for specific years
converter = PlayerToTxtConverter(years=[2024, 2025, 2026])

# Convert single year
converter.convert_year(2026)

# Convert all configured years
converter.convert_all()
```

## Output Files

### Match Data
```
data/txt/matches/nrl_matches_{year}.txt
```
Format:
```
NRL SEASON 2026
============================================================

NRL ROUND 1 - 2026
============================================================

============================================================
NRL MATCH REPORT
============================================================
Round: 1

HOME TEAM: Panthers
Score: 24

AWAY TEAM: Storm
Score: 12

RESULT: Panthers by 12 points

Date: 2026-03-05
Venue: BlueBet Stadium
============================================================
```

### Player Data
```
data/txt/players/nrl_players_{year}.txt
```
Format:
```
NRL PLAYER STATISTICS - 2026
============================================================

============================================================
TEAM: PANTHERS
============================================================

--------------------------------------------------
Player: Nathan Cleary
--------------------------------------------------
Team: Panthers
Position: Halfback
Games: 24
Tries: 8
Points: 100
Line Breaks: 12
Try Assists: 15
All Run Metres: 1200
Tackles Made: 450
--------------------------------------------------
```

### Detailed Stats
```
data/txt/detailed/nrl_detailed_{year}.txt
```
Contains complete JSON dump of detailed match statistics.

## Supported Years

All converters support data from 2001 to 2026 (subject to data availability).

## Requirements

- Python 3.7+
- No additional dependencies (uses standard library only)

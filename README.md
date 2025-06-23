# FIRMS Availability Scraper

Securely fetches fire data-availability metadata from NASA’s FIRMS API and saves it to JSON and SQLite formats for easy integration.

## Overview

This scraper retrieves **data availability** CSV metadata for the VIIRS sensors `VIIRS_NOAA20_NRT` and `VIIRS_NOAA21_NRT`. The outputs include:

- `data/fires.json` — human-readable JSON  
- `db/fires.db` — SQLite database with table `fire_availability`

The design ensures **idempotent execution** — JSON and DB overwrite previous runs cleanly.

---

## Features

- ✅ Securely loads `NASA_KEY` via `.env` using `python-dotenv`  
- ✅ Fetches CSV data for both VIIRS sensors  
- ✅ Parses data using `pandas`, adds a `sensor` column  
- ✅ Writes pretty-printed JSON (`indent=2`, `orient="records"`)  
- ✅ Persists data to SQLite with SQLAlchemy (`if_exists="replace"`)  
- ✅ Includes a smoke test verifying behavior with invalid API keys

---

## Prerequisites

- Python 3.9 or higher  
- Virtual environment support (`venv`)  
- Internet access (required for API)

---

## Installation

```bash
git clone "https://github.com/nofilsiddiqui-2000/space-concordia-data-scrape"
cd firms-scraper
python -m venv .venv

# Activate the environment:
# macOS/Linux:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\activate

pip install -r requirements.txt
```

---

## Configuration

Copy the example and add your key:

```bash
cp .env.example .env
```

Then edit `.env` to include:

```
NASA_KEY=YOUR_NASA_FIRMS_API_KEY
```

---

## Usage

```bash
python -m src.firms_scraper
```

Expected console output:

```
✔ Wrote 2 rows → data/fires.json
✔ Table [fire_availability] refreshed in db/fires.db
```

---

## Output Files

* **`data/fires.json`**: JSON array including `source`, `area_coordinates`, `day_range`, `date`, and `sensor`.
* **`db/fires.db`**: SQLite database containing table `fire_availability`; it's fully refreshed each run to avoid duplicates.

---

## Testing

Run:

```bash
pytest
```

The smoke test verifies the script exits cleanly when provided with an invalid or missing API key.

---

## Notes & Best Practices

* 🔒 **API rate limit**: 5,000 calls per 10 minutes; this script uses just 2.
* 🎯 **Exact sensor names required**: `VIIRS_NOAA20_NRT` and `VIIRS_NOAA21_NRT`—any variations result in empty CSVs.
* ⏱️ **Network timeout**: Each request includes a 30-second timeout.
* 🔁 **Idempotent writes**: JSON and DB are overwritten to ensure no duplicates.

---


#!/usr/bin/env python3
"""
firms_scraper.py – fetch NASA FIRMS data-availability CSV rows for
VIIRS_NOAA20_NRT + VIIRS_NOAA21_NRT and dump them to JSON & SQLite.

Run:
    python -m src.firms_scraper
Env:
    NASA_KEY – set in .env or exported in your shell
"""

from __future__ import annotations

import io, os, sys, pathlib
from typing import Final

import pandas as pd
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine  # uses builtin sqlite3 driver

# ------------------------------------------------------------------ #
SENSORS: Final[list[str]] = ["VIIRS_NOAA20_NRT", "VIIRS_NOAA21_NRT"]  # official codes:contentReference[oaicite:4]{index=4}
API_TMPL: Final[str] = (
    "https://firms.modaps.eosdis.nasa.gov/api/data_availability/csv/"
    "{key}/{sensor}"
)
OUT_JSON = pathlib.Path("data/fires.json")
OUT_DB = pathlib.Path("db/fires.db")
TABLE = "fire_availability"

# ------------------------------------------------------------------ #
def fetch_csv(map_key: str, sensor: str) -> pd.DataFrame:
    """Download one CSV and return a DataFrame with an extra `sensor` column."""
    url = API_TMPL.format(key=map_key, sensor=sensor)
    r = requests.get(url, timeout=30)  # 30-second hard stop:contentReference[oaicite:5]{index=5}
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    df["sensor"] = sensor
    return df


def main() -> None:
    # 1  Load credentials
    load_dotenv()                        # pulls from .env automatically:contentReference[oaicite:6]{index=6}
    map_key = os.getenv("NASA_KEY")
    if not map_key:
        sys.exit("NASA_KEY missing – add it to .env or export it")

    # 2  Fetch rows for both sensors
    frames = [fetch_csv(map_key, s) for s in SENSORS]
    df_all = pd.concat(frames, ignore_index=True)  # rows: source, area_coordinates, day_range, date, sensor:contentReference[oaicite:7]{index=7}

    if df_all.empty:
        sys.exit("FIRMS returned zero rows – check key or sensor list")

    # 3  Persist – JSON (human friendly)
    OUT_JSON.parent.mkdir(exist_ok=True)
    df_all.to_json(OUT_JSON, orient="records", indent=2)  # json array of objects:contentReference[oaicite:8]{index=8}

    # 4  Persist – SQLite (idempotent)
    OUT_DB.parent.mkdir(exist_ok=True)
    eng = create_engine(f"sqlite:///{OUT_DB}")            # three slashes → relative path:contentReference[oaicite:9]{index=9}
    df_all.to_sql(TABLE, eng, if_exists="replace", index=False)  # drop-and-recreate:contentReference[oaicite:10]{index=10}

    # 5  Log summary
    print(f"✔ Wrote {len(df_all)} rows → {OUT_JSON}")
    print(f"✔ Table [{TABLE}] refreshed in {OUT_DB}")


if __name__ == "__main__":
    main()

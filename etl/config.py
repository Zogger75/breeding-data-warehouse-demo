"""
Configuration settings for the Breeding Data Warehouse Demo ETL pipeline.

This module centralizes file paths and database connection settings so the
pipeline can be run consistently across local development environments.
"""

from pathlib import Path
import os
from dotenv import load_dotenv


# Load environment variables from .env if present.
load_dotenv()

# Project root is one level above the etl/ folder.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/breeding_dw_demo",
)

SOURCE_FILES = {
    "locations": RAW_DATA_DIR / "locations.csv",
    "germplasm": RAW_DATA_DIR / "germplasm.csv",
    "traits": RAW_DATA_DIR / "traits.csv",
    "trials": RAW_DATA_DIR / "trials.csv",
    "observations": RAW_DATA_DIR / "observations.csv",
}
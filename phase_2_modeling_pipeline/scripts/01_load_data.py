# phase_2_modeling_pipeline/scripts/01_load_data.py

"""
01_load_data.py
----------------
Loads raw energy and weather data from CSV and returns a cleaned DataFrame.
Reads Phase 1 output and stores cleaned data for Phase 2 modeling.

Author: Mantas Valantinavicius
Date: 2025-05-16
"""

import pandas as pd
import logging
from pathlib import Path
import yaml

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def load_config(config_path=None):
    """Load YAML config with absolute path resolution."""
    if config_path is None:
        script_dir = Path(__file__).resolve().parent
        config_path = script_dir.parent / "config" / "phase2_config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"❌ Config file not found: {config_path}")

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    logging.info(f"🛠️  Loaded config from: {config_path}")
    return config


def load_data(config):
    """Load raw data from CSV."""
    source_type = config["data_source"]["type"]
    file_path = Path(config["data_source"]["path"]).resolve()

    if source_type != "csv":
        raise ValueError("Only 'csv' data source is currently supported.")

    if not file_path.exists():
        raise FileNotFoundError(f"❌ Data file not found: {file_path}")

    logging.info(f"📥 Loading data from CSV: {file_path}")
    df = pd.read_csv(file_path)
    logging.info(f"✅ Loaded {len(df)} rows and {df.shape[1]} columns.")
    return df


def clean_data(df):
    """Clean the data: drop missing values, format timestamp."""
    logging.info("🧹 Cleaning data...")

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # Drop rows with any missing values
    df = df.dropna().reset_index(drop=True)

    logging.info(f"✅ Cleaned data shape: {df.shape}")
    return df


if __name__ == "__main__":
    config = load_config()
    df_raw = load_data(config)
    df_cleaned = clean_data(df_raw)

    # Save cleaned file
    output_path = Path(config["data_output"]["cleaned_path"]).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_cleaned.to_csv(output_path, index=False)

    logging.info(f"💾 Cleaned data saved to: {output_path}")

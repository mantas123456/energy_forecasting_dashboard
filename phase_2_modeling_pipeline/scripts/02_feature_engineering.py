# phase_2_modeling_pipeline/scripts/02_feature_engineering.py

"""
02_feature_engineering.py
--------------------------
Adds time-based, cyclical, lag, and rolling features to the cleaned dataset.
Saves the processed feature set for modeling.

Author: Mantas Valantinavicius
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def run(df: pd.DataFrame, variant: str = "mixed") -> pd.DataFrame:
    logging.info(f"🚀 Running feature engineering for variant: {variant}")

    # Validate required column
    if "energy_kWh" not in df.columns:
        raise ValueError(f"'energy_kWh' column not found. Available columns: {df.columns.tolist()}")

    # Ensure timestamp format and sort
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    # Time-based features
    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek
    df["month"] = df["timestamp"].dt.month
    df["is_weekend"] = df["day_of_week"] >= 5

    # Cyclical encodings
    df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
    df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)
    df["dow_sin"] = np.sin(2 * np.pi * df["day_of_week"] / 7)
    df["dow_cos"] = np.cos(2 * np.pi * df["day_of_week"] / 7)

    # Lag features
    df["lag_1h"] = df["energy_kWh"].shift(1)
    df["lag_24h"] = df["energy_kWh"].shift(24)

    # Rolling average
    df["roll_mean_24h"] = df["energy_kWh"].rolling(window=24).mean()

    # Drop NaNs from lag/rolling
    df = df.dropna().reset_index(drop=True)

    logging.info(f"✅ Feature engineering complete. Final shape: {df.shape}")
    return df


if __name__ == "__main__":
    input_path = Path("phase_2_modeling_pipeline/data/processed/cleaned_energy_data.csv")
    output_path = Path("phase_2_modeling_pipeline/data/processed/feature_engineered_mixed.csv")
    variant = "mixed"

    if not input_path.exists():
        logging.error(f"❌ Input file not found: {input_path.resolve()}")
        exit(1)

    df_cleaned = pd.read_csv(input_path)
    df_fe = run(df_cleaned, variant=variant)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_fe.to_csv(output_path, index=False)
    logging.info(f"💾 Feature-engineered data saved to: {output_path.resolve()}")

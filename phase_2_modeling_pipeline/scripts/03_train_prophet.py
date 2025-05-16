# phase_2_modeling_pipeline/scripts/03_train_prophet.py

"""
03_train_prophet.py
--------------------
Trains a Prophet model using the timestamp and energy_kWh columns.
Saves model and forecast output.

Author: Mantas Valantinavicius
"""

import pandas as pd
from prophet import Prophet
from pathlib import Path
import pickle
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def run(df: pd.DataFrame, variant: str = "mixed") -> Prophet:
    logging.info(f"🔮 Training Prophet model for variant: {variant}")

    # Check columns
    if "timestamp" not in df.columns or "energy_kWh" not in df.columns:
        raise ValueError("Missing required columns: 'timestamp' or 'energy_kWh'")

    # Prepare data
    prophet_df = df[["timestamp", "energy_kWh"]].rename(columns={"timestamp": "ds", "energy_kWh": "y"})

    # Initialize model
    model = Prophet(
        daily_seasonality=True,
        weekly_seasonality=True,
        yearly_seasonality=True
    )

    # Fit model
    model.fit(prophet_df)

    # Forecast same length as training set
    future = model.make_future_dataframe(periods=0, freq="H")
    forecast = model.predict(future)

    # Save model
    model_path = Path(f"phase_2_modeling_pipeline/models/prophet_model_{variant}.pkl")
    model_path.parent.mkdir(parents=True, exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    logging.info(f"✅ Model saved to: {model_path.resolve()}")

    # Save forecast
    forecast_path = Path(f"phase_2_modeling_pipeline/results/predictions/prophet_forecast_{variant}.csv")
    forecast_path.parent.mkdir(parents=True, exist_ok=True)
    forecast.to_csv(forecast_path, index=False)
    logging.info(f"📈 Forecast saved to: {forecast_path.resolve()}")

    return model


# Entry point to run standalone
if __name__ == "__main__":
    input_path = Path("phase_2_modeling_pipeline/data/processed/feature_engineered_mixed.csv")
    variant = "mixed"

    if not input_path.exists():
        logging.error(f"❌ Feature-engineered file not found: {input_path.resolve()}")
        exit(1)

    df_fe = pd.read_csv(input_path)
    model = run(df_fe, variant=variant)

# phase_2_modeling_pipeline/scripts/05_train_linear.py

"""
05_train_linear.py
-------------------
Trains a Linear Regression model on feature-engineered data.
Saves model and predictions (with timestamp).

Author: Mantas Valantinavicius
"""

import pandas as pd
import logging
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from math import sqrt
import pickle

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run(df: pd.DataFrame, variant: str = "mixed") -> LinearRegression:
    logging.info(f"📐 Training Linear Regression model for variant: {variant}")

    target_col = "energy_kWh"
    feature_cols = [
        'hour', 'day_of_week', 'month', 'is_weekend',
        'hour_sin', 'hour_cos', 'dow_sin', 'dow_cos',
        'temperature_C', 'lag_1h', 'lag_24h', 'roll_mean_24h'
    ]

    df = df.dropna(subset=feature_cols + [target_col])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    X = df[feature_cols]
    y = df[target_col]
    timestamps = df["timestamp"]

    X_train, X_test, y_train, y_test, ts_train, ts_test = train_test_split(
        X, y, timestamps, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    rmse = sqrt(mean_squared_error(y_test, y_pred))
    logging.info(f"📉 Linear Regression RMSE: {rmse:.4f}")

    model_path = Path(f"phase_2_modeling_pipeline/models/linear_model_{variant}.pkl")
    model_path.parent.mkdir(parents=True, exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    logging.info(f"✅ Model saved to: {model_path.resolve()}")

    pred_path = Path(f"phase_2_modeling_pipeline/results/predictions/linear_predictions_{variant}.csv")
    pred_df = pd.DataFrame({
        "timestamp": ts_test.values,
        "actual": y_test.values,
        "predicted": y_pred
    }).sort_values("timestamp")
    pred_df.to_csv(pred_path, index=False)
    logging.info(f"📈 Predictions saved to: {pred_path.resolve()}")

    return model


if __name__ == "__main__":
    input_path = Path("phase_2_modeling_pipeline/data/processed/feature_engineered_mixed.csv")
    variant = "mixed"

    if not input_path.exists():
        logging.error(f"❌ Feature-engineered file not found: {input_path.resolve()}")
        exit(1)

    df_fe = pd.read_csv(input_path)
    model = run(df_fe, variant=variant)

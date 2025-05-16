# phase_2_modeling_pipeline/scripts/04_train_xgboost.py

"""
04_train_xgboost.py
--------------------
Trains an XGBoost regression model on feature-engineered data.
Saves model and predictions (with timestamp).

Author: Mantas Valantinavicius
"""

import pandas as pd
import logging
from pathlib import Path
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from math import sqrt

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run(df: pd.DataFrame, variant: str = "mixed") -> xgb.XGBRegressor:
    logging.info(f"⚙️  Training XGBoost model for variant: {variant}")

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

    model = xgb.XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    rmse = sqrt(mean_squared_error(y_test, y_pred))
    logging.info(f"📉 XGBoost RMSE: {rmse:.4f}")

    model_path = Path(f"phase_2_modeling_pipeline/models/xgboost_model_{variant}.json")
    model_path.parent.mkdir(parents=True, exist_ok=True)
    model.save_model(model_path)
    logging.info(f"✅ Model saved to: {model_path.resolve()}")

    pred_path = Path(f"phase_2_modeling_pipeline/results/predictions/xgboost_predictions_{variant}.csv")
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

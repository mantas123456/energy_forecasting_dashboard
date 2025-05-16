# phase_2_modeling_pipeline/deployment_ready/predict_from_input.py

"""
predict_from_input.py
----------------------
Loads the trained XGBoost model and performs predictions on new input data.

Author: Mantas Valantinavicius
"""

import pandas as pd
import xgboost as xgb
import json
from pathlib import Path

# === CONFIG ===
MODEL_PATH = Path(__file__).parent / "xgboost_model_mixed.json"
FEATURES_PATH = Path(__file__).parent / "feature_columns.json"


def load_model_and_features():
    model = xgb.XGBRegressor()
    model.load_model(MODEL_PATH)

    with open(FEATURES_PATH, "r") as f:
        features = json.load(f)

    return model, features

def predict_from_csv(csv_path):
    model, features = load_model_and_features()

    df = pd.read_csv(csv_path)
    if not all(f in df.columns for f in features):
        raise ValueError("❌ Input CSV must contain all required features!")

    df_input = df[features]
    predictions = model.predict(df_input)
    df["prediction_kWh"] = predictions

    return df

def predict_from_dict_list(data: list[dict]) -> pd.DataFrame:
    """
    Accepts a list of dictionaries as input and returns a DataFrame with predictions.
    Each dict must contain all required feature keys.
    """
    model, features = load_model_and_features()

    df = pd.DataFrame(data)
    if not all(f in df.columns for f in features):
        raise ValueError("❌ Missing features in input data")

    df_input = df[features]
    df["prediction_kWh"] = model.predict(df_input)

    return df


# === USAGE EXAMPLES ===
if __name__ == "__main__":
    # Predict from CSV
    test_csv = Path("sample_input.csv")  # ← create a test file with feature columns
    if test_csv.exists():
        result = predict_from_csv(test_csv)
        print(result[["prediction_kWh"]].head())
    else:
        # Example: Predict from dict
        test_data = [{
            "hour": 14,
            "day_of_week": 2,
            "month": 5,
            "is_weekend": 0,
            "hour_sin": 0.99,
            "hour_cos": -0.12,
            "dow_sin": 0.78,
            "dow_cos": 0.62,
            "temperature_C": 23.5,
            "lag_1h": 0.8,
            "lag_24h": 0.75,
            "roll_mean_24h": 0.72
        }]
        df_result = predict_from_dict_list(test_data)
        print(df_result)

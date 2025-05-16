# phase_2_modeling_pipeline/scripts/06_evaluate_models.py

"""
06_evaluate_models.py
----------------------
Evaluates Prophet, XGBoost, and Linear models using RMSE, MAE, MAPE.
Saves summary CSV and shows a comparison plot.

Author: Mantas Valantinavicius
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_predictions():
    base = Path("phase_2_modeling_pipeline/results/predictions")

    # Prophet (needs reformat)
    prophet_path = base / "prophet_forecast_mixed.csv"
    prophet_df = pd.read_csv(prophet_path)
    prophet_df = prophet_df[["ds", "yhat"]].rename(columns={"ds": "timestamp", "yhat": "predicted"})
    prophet_df["model"] = "Prophet"

    # XGBoost
    xgb_path = base / "xgboost_predictions_mixed.csv"
    xgb_df = pd.read_csv(xgb_path)
    xgb_df["model"] = "XGBoost"

    # Linear
    linear_path = base / "linear_predictions_mixed.csv"
    lin_df = pd.read_csv(linear_path)
    lin_df["model"] = "Linear"

    return prophet_df, xgb_df, lin_df


def evaluate(y_true, y_pred):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)

    # Filter out zero values to avoid division by zero in MAPE
    non_zero_mask = y_true != 0
    if non_zero_mask.sum() == 0:
        mape = np.nan  # or 0.0
    else:
        mape = np.mean(np.abs((y_true[non_zero_mask] - y_pred[non_zero_mask]) / y_true[non_zero_mask])) * 100

    return rmse, mae, mape



def run_evaluation():
    logging.info("🔎 Evaluating all models...")

    prophet_df, xgb_df, lin_df = load_predictions()

    results = []

    # Prophet: we can’t compare directly unless we have ground truth
    prophet_truth = pd.read_csv("phase_2_modeling_pipeline/data/processed/feature_engineered_mixed.csv")
    prophet_truth = prophet_truth[["timestamp", "energy_kWh"]].rename(columns={"energy_kWh": "actual"})
    merged_prophet = pd.merge(prophet_df, prophet_truth, on="timestamp", how="inner")

    for name, df in [("Prophet", merged_prophet), ("XGBoost", xgb_df), ("Linear", lin_df)]:
        y_true = df["actual"]
        y_pred = df["predicted"]
        rmse, mae, mape = evaluate(y_true, y_pred)
        results.append({"model": name, "RMSE": rmse, "MAE": mae, "MAPE": mape})

    # Save results
    results_df = pd.DataFrame(results)
    output_path = Path("phase_2_modeling_pipeline/results/model_evaluation_summary.csv")
    results_df.to_csv(output_path, index=False)
    logging.info(f"📄 Evaluation summary saved: {output_path.resolve()}")

    # Plot bar chart
    results_df.set_index("model")[["RMSE", "MAE", "MAPE"]].plot.bar(figsize=(10, 5))
    plt.title("Model Comparison: RMSE, MAE, MAPE")
    plt.ylabel("Error")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("phase_2_modeling_pipeline/results/model_comparison_chart.png")
    plt.show()

    return results_df


if __name__ == "__main__":
    run_evaluation()

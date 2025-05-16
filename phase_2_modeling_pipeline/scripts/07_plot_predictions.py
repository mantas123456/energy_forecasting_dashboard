# phase_2_modeling_pipeline/scripts/07_plot_predictions.py

"""
07_plot_predictions.py
-----------------------
Plots actual vs predicted energy usage for Prophet, XGBoost, and Linear models.
Outputs separate PNG plots for a fixed 1-week window.

Author: Mantas Valantinavicius
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

PLOT_DIR = Path("phase_2_modeling_pipeline/results/plots/")
PLOT_DIR.mkdir(parents=True, exist_ok=True)

# Load actual values
actual_df = pd.read_csv("phase_2_modeling_pipeline/data/processed/feature_engineered_mixed.csv")
actual_df = actual_df[["timestamp", "energy_kWh"]]
actual_df["timestamp"] = pd.to_datetime(actual_df["timestamp"])
actual_df = actual_df.set_index("timestamp")

# Use a 1-week slice for clarity
week_slice = actual_df.iloc[500:668]  # 168 hours = 1 week
y_true = week_slice["energy_kWh"]

def plot_predictions(pred_file: str, model_name: str, predicted_col="predicted"):
    logging.info(f"📈 Plotting {model_name} predictions...")
    
    # Load predictions
    pred_path = Path(f"phase_2_modeling_pipeline/results/predictions/{pred_file}")
    pred_df = pd.read_csv(pred_path)
    
    if model_name == "Prophet":
        pred_df = pd.read_csv(pred_path)[["ds", "yhat"]].rename(columns={"ds": "timestamp", "yhat": "predicted"})
    
    pred_df["timestamp"] = pd.to_datetime(pred_df["timestamp"])
    pred_df = pred_df.set_index("timestamp")
    
    # Align with actual values
    aligned = pred_df.join(y_true, how="inner").rename(columns={"energy_kWh": "actual"})

    # Plot
    plt.figure(figsize=(12, 5))
    plt.plot(aligned.index, aligned["actual"], label="Actual", color="black", linewidth=2)
    plt.plot(aligned.index, aligned["predicted"], label="Predicted", linestyle="--")
    plt.title(f"{model_name} - Actual vs Predicted (1 Week)")
    plt.xlabel("Timestamp")
    plt.ylabel("Energy (kWh)")
    plt.legend()
    plt.tight_layout()

    # Save plot
    out_path = PLOT_DIR / f"{model_name.lower()}_prediction_plot.png"
    plt.savefig(out_path)
    logging.info(f"🖼 Saved plot: {out_path.resolve()}")
    plt.close()


if __name__ == "__main__":
    plot_predictions("prophet_forecast_mixed.csv", model_name="Prophet")
    plot_predictions("xgboost_predictions_mixed.csv", model_name="XGBoost")
    plot_predictions("linear_predictions_mixed.csv", model_name="Linear")
    logging.info("✅ All plots generated.")

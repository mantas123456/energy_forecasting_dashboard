# phase_2_modeling_pipeline/scripts/08b_prophet_components_plot.py

"""
08b_prophet_components_plot.py
-------------------------------
Plots the trend and seasonality components of the Prophet model.

Author: Mantas Valantinavicius
"""

import pickle
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

MODEL_PATH = Path("phase_2_modeling_pipeline/models/prophet_model_mixed.pkl")
FORECAST_PATH = Path("phase_2_modeling_pipeline/results/predictions/prophet_forecast_mixed.csv")
PLOT_PATH = Path("phase_2_modeling_pipeline/results/plots/prophet_components_plot.png")

def plot_components():
    logging.info("📊 Plotting Prophet model components...")

    if not MODEL_PATH.exists() or not FORECAST_PATH.exists():
        logging.error("❌ Model or forecast file not found.")
        return

    # Load model
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    # Load forecast data
    forecast = pd.read_csv(FORECAST_PATH)
    forecast["ds"] = pd.to_datetime(forecast["ds"])

    # Plot components
    fig = model.plot_components(forecast)
    fig.set_size_inches(10, 6)

    # Save plot
    PLOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PLOT_PATH)
    logging.info(f"🖼 Prophet components plot saved to: {PLOT_PATH.resolve()}")
    plt.show()

if __name__ == "__main__":
    plot_components()

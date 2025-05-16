# phase_2_modeling_pipeline/scripts/08_linear_feature_coefficients.py

"""
08_linear_feature_coefficients.py
----------------------------------
Visualizes feature coefficients from the trained Linear Regression model.

Author: Mantas Valantinavicius
"""

import pandas as pd
import matplotlib.pyplot as plt
import pickle
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Feature order used in training
FEATURES = [
    'hour', 'day_of_week', 'month', 'is_weekend',
    'hour_sin', 'hour_cos', 'dow_sin', 'dow_cos',
    'temperature_C', 'lag_1h', 'lag_24h', 'roll_mean_24h'
]

def plot_linear_coefficients(model_path, features, variant="mixed"):
    logging.info("📐 Plotting Linear Regression feature coefficients...")

    # Load model
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    coeffs = model.coef_

    # Create DataFrame
    df = pd.DataFrame({
        "feature": features,
        "coefficient": coeffs
    }).sort_values("coefficient", ascending=True)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.barh(df["feature"], df["coefficient"], color="orange")
    plt.axvline(0, color="black", linewidth=1)
    plt.title("Linear Regression Feature Coefficients")
    plt.xlabel("Coefficient Value")
    plt.tight_layout()

    # Save plot
    plot_path = Path("phase_2_modeling_pipeline/results/plots/linear_feature_coefficients.png")
    plot_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(plot_path)
    logging.info(f"🖼 Feature coefficients plot saved to: {plot_path.resolve()}")
    plt.show()


if __name__ == "__main__":
    model_file = Path("phase_2_modeling_pipeline/models/linear_model_mixed.pkl")

    if not model_file.exists():
        logging.error(f"❌ Linear model not found: {model_file.resolve()}")
        exit(1)

    plot_linear_coefficients(model_file, FEATURES)

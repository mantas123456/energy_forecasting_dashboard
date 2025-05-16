# phase_2_modeling_pipeline/scripts/08_xgboost_feature_importance.py

"""
08_xgboost_feature_importance.py
---------------------------------
Displays and saves a bar chart of XGBoost feature importances.

Author: Mantas Valantinavicius
"""

import xgboost as xgb
import matplotlib.pyplot as plt
from pathlib import Path
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Feature list (must match training)
FEATURES = [
    'hour', 'day_of_week', 'month', 'is_weekend',
    'hour_sin', 'hour_cos', 'dow_sin', 'dow_cos',
    'temperature_C', 'lag_1h', 'lag_24h', 'roll_mean_24h'
]

def plot_feature_importance(model_path, features, variant="mixed"):
    logging.info("📊 Generating feature importance plot...")

    # Load trained model
    model = xgb.XGBRegressor()
    model.load_model(model_path)

    importances = model.feature_importances_

    # Pair with feature names
    fi_df = pd.DataFrame({
        "feature": features,
        "importance": importances
    }).sort_values("importance", ascending=True)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.barh(fi_df["feature"], fi_df["importance"], color="skyblue")
    plt.xlabel("Importance Score")
    plt.title("XGBoost Feature Importance")
    plt.tight_layout()

    # Save
    plot_path = Path("phase_2_modeling_pipeline/results/plots/xgboost_feature_importance.png")
    plot_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(plot_path)
    logging.info(f"🖼 Feature importance plot saved to: {plot_path.resolve()}")
    plt.show()


if __name__ == "__main__":
    model_file = Path("phase_2_modeling_pipeline/models/xgboost_model_mixed.json")

    if not model_file.exists():
        logging.error(f"❌ XGBoost model not found: {model_file.resolve()}")
        exit(1)

    plot_feature_importance(model_file, FEATURES)

# phase_2_modeling_pipeline/scripts/10_export_production_bundle.py

"""
10_export_production_bundle.py
-------------------------------
Packages production-ready XGBoost model and assets into `deployment_ready/`.

Author: Mantas Valantinavicius
"""

import shutil
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

VARIANT = "mixed"
DEPLOY_DIR = Path("phase_2_modeling_pipeline/deployment_ready")
DEPLOY_DIR.mkdir(parents=True, exist_ok=True)

# Define paths
model_src = Path(f"phase_2_modeling_pipeline/models/xgboost_model_{VARIANT}.json")
pred_src = Path(f"phase_2_modeling_pipeline/results/predictions/xgboost_predictions_{VARIANT}.csv")
eval_src = Path("phase_2_modeling_pipeline/results/model_evaluation_summary.csv")

model_dst = DEPLOY_DIR / model_src.name
pred_dst = DEPLOY_DIR / pred_src.name
eval_dst = DEPLOY_DIR / eval_src.name

# Feature list (used during training)
FEATURE_COLUMNS = [
    'hour', 'day_of_week', 'month', 'is_weekend',
    'hour_sin', 'hour_cos', 'dow_sin', 'dow_cos',
    'temperature_C', 'lag_1h', 'lag_24h', 'roll_mean_24h'
]

def export_feature_list():
    features_path = DEPLOY_DIR / "feature_columns.json"
    with open(features_path, "w") as f:
        json.dump(FEATURE_COLUMNS, f, indent=2)
    logging.info(f"✅ Saved feature list: {features_path.resolve()}")

def export_requirements():
    req_path = DEPLOY_DIR / "requirements.txt"
    with open(req_path, "w") as f:
        f.write("xgboost\npandas\nnumpy\nscikit-learn\n")
    logging.info(f"📦 Created basic requirements.txt: {req_path.resolve()}")

def run():
    # Copy files
    shutil.copy2(model_src, model_dst)
    shutil.copy2(pred_src, pred_dst)
    shutil.copy2(eval_src, eval_dst)

    export_feature_list()
    export_requirements()

    logging.info("📦 All production assets exported to:")
    logging.info(f"   → {DEPLOY_DIR.resolve()}")


if __name__ == "__main__":
    run()

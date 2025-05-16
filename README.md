# ⚡ Energy Forecasting Dashboard – Phase 1: Synthetic Data Generator

This project module generates **realistic synthetic energy consumption and carbon footprint datasets** for Residential, Commercial, and Mixed-use sectors. It supports time-varying emission factors, temperature sensitivity, holiday flags, and anomaly injection for advanced forecasting and anomaly detection use cases.

---

## ✅ Features

- 🏘️ **Residential, Commercial, and Mixed** profiles (hourly/daily/10-min)
- 🌡️ Simulated **ambient temperature** (monthly averages + sinusoidal daily cycles)
- 📅 **Holiday flagging** for realistic usage suppression or boosts
- ⚠️ **Anomaly injection** (spikes, dropouts, shifts)
- ♻️ **Time-varying emission factors** (simulate carbon grid dynamics)
- 📁 Configurable via a YAML file
- 🔁 CLI-compatible, reproducible, and extendable

---

## 📂 Project Structure (Phase 1)

```
energy_forecasting_dashboard/
│
├── config/
│   └── synthetic_config.yaml         # All generation parameters
│
├── data/
│   └── raw/synthetic/                # Generated CSV files (residential, commercial, mixed)
│
├── scripts/
│   └── synthetic_data_generator_v2.py  # Main generation script
│
├── notebooks/
│   └── 01_visualize_synthetic_data_v2.ipynb  # Anomaly + trend visualizer
│
├── src/
│   └── utils/loader.py               # Reusable file loader
│
├── plots/
│   └── energy_by_sector.png          # Auto-exported plots (optional)
│   └── carbon_by_sector.png
│
└── README.md                         # You are here
```

---

## 🔧 Configuration

All parameters are controlled through `config/synthetic_config.yaml`, including:

- ✅ Simulation length (`start_date`, `days`, `frequency`)
- ✅ Sector-specific demand profiles (hourly, normalized)
- ✅ Temperature profile, comfort deviation slope
- ✅ Carbon emissions (static or hourly dynamic)
- ✅ Anomaly injection settings

```yaml
generate:
  residential: true
  commercial: true
  mixed: true

frequency: "1h"
emissions:
  mode: "dynamic"
  dynamic_by_hour:
    night: 450
    midday: 300
    default: 396
anomalies:
  enabled: true
  types: ["spike", "dropout", "shift"]
  count: 15
```

---

## 🚀 How to Run

### ▶️ Generate Data

```bash
python scripts/synthetic_data_generator_v2.py --config config/synthetic_config.yaml
```

### 📊 Visualize Data

Open in Jupyter or VS Code:

```bash
notebooks/01_visualize_synthetic_data_v2.ipynb
```

- Plots daily average consumption per sector
- Highlights injected anomalies with markers

---

## 📈 Phase 2 – Modeling, Evaluation & Deployment (Energy Forecasting Dashboard)

This phase focuses on training, evaluating, and packaging forecasting models to predict hourly building energy consumption using synthetic data. The goal is to identify the most accurate model and prepare it for deployment or dashboard integration.

---

## ✅ Objectives

- Train multiple forecasting models on engineered features
- Evaluate models using RMSE, MAE, and MAPE
- Visualize prediction accuracy and model internals
- Generate a professional `.docx` report
- Package production-ready model artifacts

---

## 🧠 Models Used

| Model            | Description                              |
|------------------|------------------------------------------|
| XGBoost          | Gradient boosting model (best performer) |
| Prophet          | Trend & seasonality decomposition         |
| Linear Regression| Baseline statistical model               |

---

## 📁 Directory Structure

```
phase_2_modeling_pipeline/
├── models/                   # Trained model files (.json, .pkl)
├── results/
│   ├── predictions/          # Output CSVs from each model
│   ├── plots/                # All evaluation & diagnostic visuals
│   ├── model_evaluation_summary.csv
│   └── Phase2_Model_Evaluation_Report.docx
├── deployment_ready/
│   ├── xgboost_model_mixed.json
│   ├── xgboost_predictions_mixed.csv
│   ├── feature_columns.json
│   ├── requirements.txt
│   └── predict_from_input.py
└── scripts/
    └── (01–10)_*.py         # Training, evaluation, visualization, export
```

---

## 📊 Model Evaluation Summary

| Model            | RMSE     | MAE      | MAPE (%) |
|------------------|----------|----------|-----------|
| **XGBoost**       | *0.0787* | *0.0595* | *12.31*    |
| Prophet          | 0.1036   | 0.0814   | 17.04     |
| Linear Regression| 0.1125   | 0.0866   | 17.81     |

✅ **XGBoost** outperforms all models and is packaged for deployment.

---

## 🛠 How to Run Prediction

```bash
cd phase_2_modeling_pipeline/deployment_ready

# Predict from a CSV file with all features
python predict_from_input.py

# OR use the function directly in Python:
from predict_from_input import predict_from_dict_list

sample = [{
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

predict_from_dict_list(sample)
```

---

## 📦 Deployment Bundle Includes

- ✅ `xgboost_model_mixed.json`
- ✅ `feature_columns.json`
- ✅ `xgboost_predictions_mixed.csv`
- ✅ `requirements.txt`
- ✅ `predict_from_input.py`

---

## 📄 Report

📄 `Phase2_Model_Evaluation_Report.docx`  
Located in `/results/Phase2_Model_Evaluation_Report.docx`

Includes methodology, model performance, plots, and final recommendations.

---

## 🧪 Requirements

```
xgboost
pandas
numpy
scikit-learn
```

Install with:

```bash
pip install -r deployment_ready/requirements.txt
```

---

## 📍 Git Tag

This phase is archived and reproducible under Git tag: `v2.0`

---

## 🚀 Next Steps (Phase 3)

- Real-time dashboard integration
- Anomaly detection
- Deployment via API or stream

---

**Author:** Mantas Valantinavicius  
**Status:** ✅ Phase 2 complete  

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

## 🧠 Next Phase

**Phase 2** will use this data for:

- Time series forecasting (Prophet, XGBoost)
- Anomaly detection (unsupervised & supervised)
- KPI dashboards and auto-generated reports

---

## 👤 Author

**Mantas Valantinavičius**  
Phase 1 complete ✅ | Energy & Data Science | Malta 🇲🇹

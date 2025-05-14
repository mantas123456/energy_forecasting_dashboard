# 🔮 FUTURE_FEATURES.md

## Synthetic Energy & Carbon Data Generator – Feature Roadmap

This roadmap outlines **planned and potential enhancements** for the synthetic data generation module of the Energy Forecasting Dashboard. These features aim to boost the **realism**, **flexibility**, and **machine learning value** of the synthetic datasets — enabling high-fidelity testing of forecasting algorithms, anomaly detection systems, and carbon reduction strategies.

---

## ✅ Overview of Future Feature Categories

- ⚙️ Realistic behavior modeling  
- 🌍 Environmental + geographic realism  
- ⚠️ Advanced anomaly simulation  
- 🔋 Energy systems & storage  
- 🧠 ML-readiness enhancements  
- 🧰 Configurability & plugin support  
- 📦 Reporting & export tooling  

---

## ⚙️ 1. Behavior & Load Profile Enhancements

| Feature | Description |
|--------|-------------|
| 🔁 Autoregressive Load Feedback | Make current demand depend on past demand (e.g., memory in behavior). |
| 🧱 Building Archetypes | Create load curves for different building types (office, school, supermarket). |
| 👥 Demographic Profiles | Simulate dwellings by household type (elderly, family, single, etc.). |
| 🧩 Inter-Sector Influence | Link residential and commercial loads (e.g., remote work impacts). |

---

## 🌡️ 2. Weather & Environment Integration

| Feature | Description |
|--------|-------------|
| 🌤️ Real-World Weather APIs | Pull actual temperature, humidity, solar radiation via Open-Meteo or Copernicus. |
| ☀️ Solar PV Effects | Reduce grid demand based on irradiance for buildings with solar panels. |
| 💧 Humidity-Adjusted HVAC Loads | Increase realism in cooling demand using dew point / humidity index. |
| 🌍 Regional Parameters | Load climate, holiday calendar, and grid emission mix by geographic location. |

---

## ⚠️ 3. Advanced Anomaly Injection

| Feature | Description |
|--------|-------------|
| 💣 Fault Injection (Realistic) | Simulate equipment failure, sensor glitches, night spikes, etc. |
| 🐢 Gradual Degradation | Inject slow drifts (e.g., insulation wear, sensor drift). |
| 🧠 LLM-Driven Anomalies | Use GPT-style models to generate scenario-driven anomalies. |
| 📌 Anomaly Metadata | Store type, severity, duration, and injection cause per anomaly point. |

---

## 🔋 4. Smart Grid, EV, and Storage Simulation

| Feature | Description |
|--------|-------------|
| 🔌 Appliance-Level Energy Use | Split load into lighting, HVAC, plug loads, refrigeration, etc. |
| 🚗 EV Charging Logic | Simulate after-work charging, fast charging at peak hours, etc. |
| 🔋 Battery Storage & TOU Logic | Charge/discharge logic tied to grid price and peak shaving. |
| ⚠️ Demand Curtailment | Model load shedding or blackouts triggered by grid signals. |

---

## 🧠 5. ML-Ready Dataset Improvements

| Feature | Description |
|--------|-------------|
| ⏱️ Time Feature Engineering | Auto-add hour, day of week, month, holiday, weekend, season. |
| 🧪 Forecast Baseline Columns | Include moving average or naïve forecasts as ML training targets. |
| 🧠 Scenario Labels | Tag datapoints with context like `holiday`, `anomaly`, `heatwave`, etc. |
| 📚 Train/Test Splits | Flag or export reproducible data splits for ML experimentation. |

---

## 🧰 6. Configuration & Extensibility

| Feature | Description |
|--------|-------------|
| 🔌 Plugin Hook Architecture | Allow external functions for anomalies, emissions, or appliances. |
| 🗂️ Scenario Registry | Save config hash, seed, and metadata with each dataset for auditability. |
| 🧠 Config Wizards | CLI or GUI for easier YAML configuration building. |
| 🧱 Modular Component Overwrites | Plug-and-play architecture for extending energy logic or weather engines. |

---

## 📦 7. Post-Processing & Reporting

| Feature | Description |
|--------|-------------|
| 📊 Auto-Generated Reports | Markdown or PDF summary reports with plots and stats. |
| 📁 Dataset Packager | Zip dataset + config + plots + README for each synthetic run. |
| 📓 Notebook Generator | Generate visualization notebooks like `01_visualize_<run_id>.ipynb`. |

---

## 🛣️ Implementation Phases

### 🔹 Short-Term (v2.5 – v3.0)
- Regional emissions & weather
- Battery + PV effects
- Enhanced anomaly metadata

### 🔹 Mid-Term
- Appliance split modeling
- LLM anomaly descriptions
- Train/test flag injection

### 🔹 Long-Term
- GUI wizard & dashboard export
- Plugin system for user-defined events
- Scenario registry + reproducible pipelines

---

## 👤 Maintainer Notes

If you use this generator for:
- ⚗️ ML benchmarking — improve realism with feature enrichment
- 🌍 Climate scenarios — add grid emission variability
- 🏢 Building automation — simulate appliance-level response

This roadmap ensures your synthetic engine is **production-grade and research-ready**.

---

🧾 Last updated: 2025-05  
Author: **Mantas Valantinavičius**

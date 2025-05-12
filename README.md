# 🔋 Forecasting Building Energy Consumption & Carbon Impact Dashboard

This project forecasts building energy consumption, detects anomalies, and translates inefficiencies into actionable carbon impact estimates. It includes synthetic data generation, forecasting models (Prophet, XGBoost, etc.), anomaly detection, and a user-facing dashboard.

---

## 📁 Project Structure

```
energy_forecasting_dashboard/
├── data/                  # Raw, processed, and synthetic data
├── src/                   # Source code (data, models, utils)
├── dashboard/             # Interactive dashboard (Dash/Plotly)
├── notebooks/             # Jupyter notebooks for EDA & testing
├── tests/                 # Unit tests
├── logs/                  # Runtime logs
├── environment.yml        # Conda environment definition
├── config.ini             # Project config
└── README.md              # Project overview (this file)
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/energy_forecasting_dashboard.git
cd energy_forecasting_dashboard
```

### 2. Create and activate the environment

```bash
conda env create -f environment.yml
conda activate energy_env
```

### 3. Run a test script

```bash
python src/test_setup.py
```

---

## 📦 Key Tools & Technologies

| Category              | Tools & Libraries                                  |
|----------------------|----------------------------------------------------|
| **Languages**         | Python 3.10                                        |
| **Data Analysis**     | Pandas, NumPy, Scikit-learn                        |
| **Forecasting**       | Prophet, XGBoost, Statsmodels                     |
| **Anomaly Detection** | Isolation Forest, Thresholding, Custom Logic      |
| **Visualization**     | Plotly, Dash, Seaborn, Matplotlib                  |
| **Dashboarding**      | Plotly Dash                                        |
| **DevOps & Testing**  | Conda, pip, configparser, logging, pytest         |

---

## 🧱 Phase 0: Environment Setup

- ✅ Created modular project structure
- ✅ Set up Conda environment (`energy_env`)
- ✅ Installed required dependencies
- ✅ Verified setup with test script
- ✅ Exported clean `environment.yml`

---

## 🧭 Next Steps

Proceed to **Phase 1**:
- Generate synthetic energy & temperature data
- Introduce realistic usage patterns and anomalies
- Store output in SQLite and CSV for modeling

---

## 👤 Author

Mantas Valantinavičius  
[LinkedIn](https://www.linkedin.com/in/mantas-valantinavicius/) · mantas.valantinavicius@gmail.com

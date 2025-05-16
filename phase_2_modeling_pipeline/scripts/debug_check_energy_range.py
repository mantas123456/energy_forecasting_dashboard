import pandas as pd
from pathlib import Path

file_path = Path("phase_2_modeling_pipeline/data/processed/feature_engineered_mixed.csv")

if not file_path.exists():
    print(f"❌ File not found: {file_path.resolve()}")
    exit(1)

df = pd.read_csv(file_path)

# Show column names to confirm
print("\n🧾 Columns:", df.columns.tolist())

# Check if energy column exists
if "energy_kWh" not in df.columns:
    print("❌ 'energy_kWh' column not found!")
    exit(1)

# Show descriptive stats
print("\n📊 Descriptive statistics for energy_kWh:")
print(df["energy_kWh"].describe())

# Show extra debug info
print("\n🔍 Extras:")
print("Missing values:", df["energy_kWh"].isna().sum())
print("Zero values:", (df["energy_kWh"] == 0).sum())
print("Negative values:", (df["energy_kWh"] < 0).sum())
print("Unique values:", df["energy_kWh"].nunique())

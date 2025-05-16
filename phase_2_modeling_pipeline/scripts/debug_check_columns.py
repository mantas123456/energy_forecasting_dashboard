import pandas as pd
from pathlib import Path

file_path = Path("phase_2_modeling_pipeline/data/processed/cleaned_energy_data.csv")

# Load and show column names
if file_path.exists():
    df = pd.read_csv(file_path)
    print("\n🧾 Columns in cleaned CSV:")
    print(df.columns.tolist())
else:
    print(f"❌ File not found: {file_path.resolve()}")

from pathlib import Path
import pandas as pd

def load_synthetic_dataset(filename):
    """
    Load a CSV file from the 'data/raw/synthetic/' directory
    regardless of current working directory depth.

    Parameters:
        filename (str): e.g., 'synthetic_energy_residential_365d.csv'

    Returns:
        pd.DataFrame: Loaded data with parsed timestamps
    """
    current = Path.cwd()

    # Search up to 5 parent levels to locate the 'data/raw/synthetic/' folder
    for _ in range(5):
        potential_path = current / "data" / "raw" / "synthetic" / filename
        if potential_path.exists():
            return pd.read_csv(potential_path, parse_dates=["timestamp"])
        current = current.parent

    raise FileNotFoundError(
        f"❌ Could not find '{filename}' under any parent directory in /data/raw/synthetic/"
    )

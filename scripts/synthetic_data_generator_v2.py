"""
synthetic_data_generator_v2.py

Generates synthetic energy consumption and carbon emission datasets based on user-defined parameters.
Includes CLI support, modular functions, and docstrings for professional use.

Author: Mantas Valantinavicius
"""

import argparse
import yaml
import pandas as pd
import numpy as np
from pathlib import Path
import os





def parse_cli_args():
    parser = argparse.ArgumentParser(description="Synthetic Energy Data Generator v2")
    parser.add_argument('--config', type=str, default='config/synthetic_config.yaml',
                        help='Path to YAML configuration file')
    return parser.parse_args()


def load_config(path: str) -> dict:
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def generate_timestamps(start_date: str, periods: int, freq: str) -> pd.DatetimeIndex:
    return pd.date_range(start=start_date, periods=periods, freq=freq)


def simulate_temperature(timestamps, profile="sinusoidal", std=1.5) -> list:
    month_means = {1: 10, 2: 11, 3: 13, 4: 17, 5: 21, 6: 27, 7: 30, 8: 30,
                   9: 27, 10: 22, 11: 16, 12: 12}
    temps = []
    for ts in timestamps:
        base = month_means[ts.month]
        if profile == "sinusoidal":
            hour_factor = np.cos((ts.hour - 15) / 12 * np.pi)
            fluctuation = hour_factor * 5
        else:
            fluctuation = 0
        noise = np.random.normal(0, std)
        temps.append(base + fluctuation + noise)
    return temps


def get_holiday_flags(timestamps):
    holiday_dates = pd.to_datetime([
        '2024-01-01', '2024-03-31', '2024-06-07',
        '2024-09-21', '2024-12-25'
    ])
    return [1 if ts.normalize() in holiday_dates else 0 for ts in timestamps]


def get_emission_factor(ts, config):
    mode = config['emissions']['mode']
    if mode == 'static':
        return config['emissions']['static_value']
    hour = ts.hour
    if hour < 6:
        return config['emissions']['dynamic_by_hour']['night']
    elif 10 <= hour <= 16:
        return config['emissions']['dynamic_by_hour']['midday']
    return config['emissions']['dynamic_by_hour']['default']


def compute_carbon(energy_kwh, timestamps, config):
    return [(e * get_emission_factor(ts, config)) / 1000 for e, ts in zip(energy_kwh, timestamps)]


def generate_energy_profile(sector, timestamps, temperature, holidays, base_profile, comfort_temp, slope, behavior_std):
    energy = []
    for ts, temp, hol in zip(timestamps, temperature, holidays):
        base = base_profile[ts.hour]
        if ts.weekday() >= 5 and sector == 'Commercial':
            base *= 0.3
        if hol and sector == 'Commercial':
            base *= 0.2
        elif hol and sector == 'Residential':
            base *= 1.1
        temp_effect = slope * abs(temp - comfort_temp)
        adjusted = base * (1 + temp_effect)
        noise = np.random.normal(0, behavior_std)
        energy.append(max(adjusted + noise, 0.05))
    return energy


def generate_dataset(config, sector: str, sector_profiles: dict) -> pd.DataFrame:
    """
    Generate a complete synthetic dataset for a given sector.

    Parameters:
        config (dict): Configuration settings
        sector (str): Sector name (e.g., 'Residential')
        sector_profiles (dict): Hourly base profiles from config

    Returns:
        pd.DataFrame: DataFrame with timestamps, temperature, energy, carbon, and anomaly flag
    """
    freq = config['frequency'].lower()
    steps_per_day = {'1d': 1, '1h': 24, '10min': 144}
    periods = config['days'] * steps_per_day.get(freq, 24)

    timestamps = generate_timestamps(config['start_date'], periods, freq)
    temperature = simulate_temperature(timestamps,
                                       config['temperature']['profile'],
                                       config['temperature']['std'])
    holidays = get_holiday_flags(timestamps)
    slope = config['temperature_impact'][f"slope_{sector.lower()}"]
    base_profile = sector_profiles[sector]

    energy = generate_energy_profile(
        sector, timestamps, temperature, holidays,
        base_profile,
        config['temperature_impact']['comfort_temp'],
        slope,
        config['noise']['behavior_std']
    )

    carbon = compute_carbon(energy, timestamps, config)

    df = pd.DataFrame({
        'timestamp': timestamps,
        'sector': sector,
        'energy_kWh': np.round(energy, 3),
        'temperature_C': np.round(temperature, 1),
        'holiday_flag': holidays,
        'carbon_kgCO2e': np.round(carbon, 3)
    })

    df = inject_anomalies(df, config)
    return df




def main(config_path: str):
    """
    Main entry point for generating synthetic datasets using config file.
    Loads configuration, sector profiles, and triggers dataset generation.
    """
    config = load_config(config_path)  # config is defined here

    # Load sector base profiles from config
    sector_profiles = config['sector_profiles']  # ✅ This is now safe

    output_dir = Path(config['output_dir'])
    output_dir.mkdir(parents=True, exist_ok=True)

    paths = {}

    if config['generate']['residential']:
        df_res = generate_dataset(config, 'Residential', sector_profiles)
        path_res = output_dir / "synthetic_energy_residential_365d.csv"
        df_res.to_csv(path_res, index=False)
        print(f"✅ Residential data saved to {path_res}")
        paths['res'] = path_res

    if config['generate']['commercial']:
        df_com = generate_dataset(config, 'Commercial', sector_profiles)
        path_com = output_dir / "synthetic_energy_commercial_365d.csv"
        df_com.to_csv(path_com, index=False)
        print(f"✅ Commercial data saved to {path_com}")
        paths['com'] = path_com

    if config['generate']['mixed'] and 'res' in paths and 'com' in paths:
        df_res = pd.read_csv(paths['res'], parse_dates=['timestamp'])
        df_com = pd.read_csv(paths['com'], parse_dates=['timestamp'])

        w = config['residential_weight']
        df_mix = df_res.copy()
        df_mix['sector'] = 'Mixed'
        df_mix['energy_kWh'] = w * df_res['energy_kWh'] + (1 - w) * df_com['energy_kWh']
        df_mix['temperature_C'] = w * df_res['temperature_C'] + (1 - w) * df_com['temperature_C']
        df_mix['carbon_kgCO2e'] = (df_mix['energy_kWh'] * config['emissions']['static_value']) / 1000
        df_mix['anomaly_flag'] = 0  # Optional: Mixed sector has no anomalies injected

        path_mix = output_dir / "synthetic_energy_mixed_365d.csv"
        df_mix.to_csv(path_mix, index=False)
        print(f"✅ Mixed-use data saved to {path_mix}")


def inject_anomalies(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Inject synthetic anomalies into energy consumption data.

    Parameters:
        df (pd.DataFrame): Original clean dataset
        config (dict): Config section for anomaly parameters

    Returns:
        pd.DataFrame: Dataset with anomalies applied and flagged
    """
    if not config.get("anomalies", {}).get("enabled", False):
        df["anomaly_flag"] = 0
        return df

    df = df.copy()
    np.random.seed(config["anomalies"].get("random_seed", 42))
    count = config["anomalies"]["count"]
    anomaly_types = config["anomalies"]["types"]
    anomaly_indices = np.random.choice(df.index, size=count, replace=False)

    df["anomaly_flag"] = 0

    for idx in anomaly_indices:
        atype = np.random.choice(anomaly_types)
        if atype == "spike":
            df.at[idx, "energy_kWh"] *= config["anomalies"]["spike_multiplier"]
        elif atype == "dropout":
            df.at[idx, "energy_kWh"] = config["anomalies"]["dropout_value"]
        elif atype == "shift":
            pct = np.random.uniform(*config["anomalies"]["shift_percent_range"])
            df.at[idx, "energy_kWh"] *= (1 + pct)
        df.at[idx, "anomaly_flag"] = 1

    return df



if __name__ == "__main__":
    args = parse_cli_args()
    main(args.config)

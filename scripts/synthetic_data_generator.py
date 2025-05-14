# synthetic_data_generator.py
"""
Generates synthetic hourly energy consumption and carbon data for:
- Residential
- Commercial
- Mixed-use buildings

Includes temperature effects, holiday impacts, and carbon footprint calculation.
"""

import pandas as pd
import numpy as np
from datetime import datetime

# --- Global Emission Factor for Malta (gCO2e/kWh) ---
EMISSION_FACTOR = 396  # from national average

# --- Hourly usage profiles for different sectors (normalized base load) ---
SECTOR_PROFILES = {
    'Residential': [
        0.6, 0.5, 0.4, 0.3, 0.3, 0.4, 0.6, 0.9, 1.0, 0.8, 0.6, 0.5,
        0.5, 0.5, 0.5, 0.6, 0.7, 0.9, 1.0, 0.9, 0.7, 0.6, 0.6, 0.5
    ],
    'Commercial': [
        0.2, 0.1, 0.1, 0.1, 0.2, 0.4, 0.8, 1.0, 1.0, 1.0, 1.0, 1.0,
        1.0, 1.0, 1.0, 1.0, 1.0, 0.8, 0.4, 0.2, 0.1, 0.1, 0.1, 0.1
    ]
}


def generate_timestamps(start_date: str, days: int):
    """Generate a list of hourly timestamps for the given duration."""
    return pd.date_range(start=start_date, periods=days * 24, freq='H')


def simulate_temperature(timestamps):
    """Simulate ambient temperature based on monthly averages + daily noise."""
    month_means = {1: 10, 2: 11, 3: 13, 4: 17, 5: 21, 6: 27, 7: 30, 8: 30,
                   9: 27, 10: 22, 11: 16, 12: 12}
    temps = []
    for ts in timestamps:
        base = month_means[ts.month]
        noise = np.random.normal(0, 1.5)
        temps.append(base + noise)
    return temps


def get_holiday_flags(timestamps):
    """Flag national holidays. You can expand this list for full coverage."""
    holiday_dates = pd.to_datetime([
        '2024-01-01', '2024-03-31', '2024-06-07',
        '2024-09-21', '2024-12-25'
    ])
    return [1 if ts.normalize() in holiday_dates else 0 for ts in timestamps]


def generate_energy_profile(sector, timestamps, temperature, holidays):
    """Create energy consumption profile for a sector."""
    profile = SECTOR_PROFILES[sector]
    energy = []

    for ts, temp, hol in zip(timestamps, temperature, holidays):
        base = profile[ts.hour]
        weekday = ts.weekday()

        # Weekend reduction for commercial
        if weekday >= 5 and sector == 'Commercial':
            base *= 0.3
        # Holiday modifiers
        if hol and sector == 'Commercial':
            base *= 0.2
        elif hol and sector == 'Residential':
            base *= 1.1

        # Temperature sensitivity (deviation from 20°C comfort)
        temp_effect = 0.01 * abs(temp - 20)
        adjusted = base * (1 + temp_effect)

        # Random behavioral noise
        noise = np.random.normal(0, 0.05)
        energy.append(max(adjusted + noise, 0.05))  # avoid negative values

    return energy


def compute_carbon(energy_kwh):
    """Convert energy (kWh) to carbon emissions (kgCO2e)."""
    return [(e * EMISSION_FACTOR) / 1000 for e in energy_kwh]


def generate_synthetic_data(start_date='2024-01-01', days=365, sector='Residential'):
    """Main function to generate synthetic dataset for a single sector."""
    timestamps = generate_timestamps(start_date, days)
    temp = simulate_temperature(timestamps)
    holidays = get_holiday_flags(timestamps)
    energy = generate_energy_profile(sector, timestamps, temp, holidays)
    carbon = compute_carbon(energy)

    df = pd.DataFrame({
        'timestamp': timestamps,
        'sector': sector,
        'energy_kWh': np.round(energy, 3),
        'temperature_C': np.round(temp, 1),
        'holiday_flag': holidays,
        'carbon_kgCO2e': np.round(carbon, 3)
    })

    return df


def generate_mixed_sector(res_path, com_path, res_weight=0.6):
    """Blend residential and commercial data to create mixed-use profile."""
    com_weight = 1.0 - res_weight

    df_res = pd.read_csv(res_path, parse_dates=['timestamp'])
    df_com = pd.read_csv(com_path, parse_dates=['timestamp'])

    df_mix = df_res[['timestamp']].copy()
    df_mix['sector'] = 'Mixed'
    df_mix['energy_kWh'] = res_weight * df_res['energy_kWh'] + com_weight * df_com['energy_kWh']
    df_mix['temperature_C'] = res_weight * df_res['temperature_C'] + com_weight * df_com['temperature_C']
    df_mix['holiday_flag'] = df_res['holiday_flag']  # same timestamps
    df_mix['carbon_kgCO2e'] = (df_mix['energy_kWh'] * EMISSION_FACTOR) / 1000

    out_path = "data/raw/synthetic/synthetic_energy_mixed_365d.csv"
    df_mix.to_csv(out_path, index=False)
    print(f"✅ Mixed-use dataset saved to: {out_path}")


if __name__ == "__main__":
    # Generate Residential
    df_res = generate_synthetic_data(days=365, sector='Residential')
    res_path = "data/raw/synthetic/synthetic_energy_residential_365d.csv"
    df_res.to_csv(res_path, index=False)
    print(f"✅ Residential dataset saved to: {res_path}")

    # Generate Commercial
    df_com = generate_synthetic_data(days=365, sector='Commercial')
    com_path = "data/raw/synthetic/synthetic_energy_commercial_365d.csv"
    df_com.to_csv(com_path, index=False)
    print(f"✅ Commercial dataset saved to: {com_path}")

    # Generate Mixed (60% Residential + 40% Commercial)
    generate_mixed_sector(res_path, com_path, res_weight=0.6)

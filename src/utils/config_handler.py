import configparser
from pathlib import Path

def load_config(config_path="config.ini"):
    config = configparser.ConfigParser()
    if not Path(config_path).exists():
        raise FileNotFoundError(f"Config file not found at {config_path}")
    config.read(config_path)
    return config

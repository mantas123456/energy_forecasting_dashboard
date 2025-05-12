import logging
from pathlib import Path

def setup_logger(name: str, log_file: str = "logs/project.log", level=logging.INFO) -> logging.Logger:
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter('%(asctime)s — %(name)s — %(levelname)s — %(message)s')

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        logger.addHandler(handler)

    return logger

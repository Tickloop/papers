import logging
from pathlib import Path

from src.core.settings import get_settings
settings = get_settings()

def setup_logger(name: str):
    base_path = Path(settings.log_dir)
    hdlr = logging.FileHandler(base_path / 'app.log', mode='a')
    hdlr.setLevel(logging.INFO)
    hdlr.setFormatter(logging.Formatter("%(asctime)s %(levelname)s [%(filename)s @ %(lineno)s]: %(message)s"))
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(hdlr)
    return logger

import logging
import os
from logging.handlers import RotatingFileHandler

import yaml

logger = logging.getLogger(__file__)


def load_config():
    """
    Load the config file
    :return: the config
    """
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)


def init_logger() -> None:
    """
    Init the logger settings on console and on file.

    :return: None
    """
    # Set library level
    logging.getLogger("httpx").setLevel(logging.ERROR)
    # Set logger
    log_name = "logs/app.log"
    file_handler = RotatingFileHandler(
        log_name, mode="w", maxBytes=100000, backupCount=1, encoding="utf-8"
    )
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s, %(levelname)-8s [%(filename)s:%(funcName)s:%(lineno)d] "
        "- %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    console_handler.setLevel(logging.INFO)
    logging.getLogger().addHandler(console_handler)
    logging.getLogger().addHandler(file_handler)
    if "PRODUCTION" in os.environ:
        logging.getLogger().setLevel(logging.ERROR)
    else:
        logging.getLogger().setLevel(logging.INFO)

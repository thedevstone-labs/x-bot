import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Dict

import yaml
from pydantic import BaseModel

logger = logging.getLogger(__file__)


class Auth(BaseModel):
    username: str
    password: str
    email: str


class Scraper(BaseModel):
    tweet_number: int
    query: str


class AppConfig(BaseModel):
    auth: Auth
    scraper: Scraper


def load_config():
    """
    Load the config file
    :return: the config
    """
    with get_path("config.yaml").open("r") as file:
        config_data: Dict = yaml.safe_load(file)
        return AppConfig(**config_data)


def get_path(path: str) -> Path:
    """
    Get the relative project path to root.

    :param path: the relative path
    :return: the absolute path
    """
    return Path.joinpath(
        Path(os.path.abspath(__file__)).parent.parent, path
    )


def init_logger() -> None:
    """
    Init the logger settings on console and on file.

    :return: None
    """
    # Set library level
    logging.getLogger("httpx").setLevel(logging.ERROR)
    # Set logger
    log_name = get_path("logs/app.log")
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

import os
from dotenv import load_dotenv
from deface.common.logging import logging

logger = logging.getLogger("config")

load_dotenv()


def get_env(name: str, default=None, required=False):
    value = os.getenv(name, default)

    if required and value is None:
        raise RuntimeError(f"Missing required env var: {name}")

    return value


FOLDER_CONFIG = {
    "upload": get_env("FOLDER_UPLOAD", default="data/upload", required=True),
    "result": get_env("FOLDER_RESULT", default="data/result",  required=True),
}

APP_ROOT_PATH = get_env("APP_ROOT_PATH", default="")

# Konfiguration beim Start loggen
logger.info("🚀 Loading configuration...")
logger.info(f"APP_ROOT_PATH: '{APP_ROOT_PATH}'")
logger.info(f"Folders: {FOLDER_CONFIG}")
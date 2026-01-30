import os
from typing import List, Optional

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


def _parse_csv(env_value: Optional[str], default: str) -> List[str]:
    raw_value = env_value if env_value is not None else default
    if not raw_value:
        return []
    return [part.strip() for part in raw_value.split(",") if part.strip()]


def _parse_bool(env_value: Optional[str], default: bool):
    if env_value is None:
        return default
    return env_value.strip().lower() in {"1", "true", "yes", "on"}


CORS_ALLOW_ORIGINS = _parse_csv(get_env("CORS_ALLOW_ORIGINS", default=""), default="")
CORS_ALLOW_METHODS = _parse_csv(get_env("CORS_ALLOW_METHODS", default="GET,POST,OPTIONS"), default="GET,POST,OPTIONS")
CORS_ALLOW_HEADERS = _parse_csv(get_env("CORS_ALLOW_HEADERS", default="Authorization,Content-Type"), default="Authorization,Content-Type")
CORS_ALLOW_CREDENTIALS = _parse_bool(get_env("CORS_ALLOW_CREDENTIALS", default="false"), default=False)

CORS_CONFIG = {
    "allow_origins": CORS_ALLOW_ORIGINS,
    "allow_methods": CORS_ALLOW_METHODS,
    "allow_headers": CORS_ALLOW_HEADERS,
    "allow_credentials": CORS_ALLOW_CREDENTIALS,
}

# Konfiguration beim Start loggen
logger.info("🚀 Loading configuration...")
logger.info(f"APP_ROOT_PATH: '{APP_ROOT_PATH}'")
logger.info(f"Folders: {FOLDER_CONFIG}")
logger.info(f"CORS: {CORS_CONFIG}")

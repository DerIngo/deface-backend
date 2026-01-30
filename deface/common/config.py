import os
from dotenv import load_dotenv

load_dotenv()


def get_env(name: str, default=None, required=False):
    value = os.getenv(name, default)

    if required and value is None:
        raise RuntimeError(f"Missing required env var: {name}")

    return value


FOLDER_CONFIG = {
    "upload": get_env("FOLDER_UPLOAD", required=True),
    "result": get_env("FOLDER_RESULT", required=True),
}

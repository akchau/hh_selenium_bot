import os
from pathlib import Path
from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):

    DEBUG: bool
    BASE_LOG_PATH: str
    HH_EMAIL: str
    HH_PASSWORD: str

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"


settings = Settings()

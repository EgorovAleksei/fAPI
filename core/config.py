import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent

load_dotenv(find_dotenv("../.env"))


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db_url: str = os.getenv("DB_URL_LOCAL")
    # db_echo: bool = True
    db_echo: bool = False


settings = Settings()

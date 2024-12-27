import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent

load_dotenv(find_dotenv("../.env"))


class DbSettings(BaseModel):
    url: str = os.getenv("DB_URL_LOCAL")
    # echo: bool = True
    echo: bool = False


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 5


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db: DbSettings = DbSettings()
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()

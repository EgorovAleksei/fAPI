import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent
#
# load_dotenv(find_dotenv("../.env"))


class DbSettings(BaseModel):
    # url: str = os.getenv("DB_URL_LOCAL")
    # echo: bool = True
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 10
    max_overflow: int = 10


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 5
    refresh_token_expire_days: int = 30


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
    )
    api_v1_prefix: str = "/api/v1"
    # db: DbSettings = DbSettings()
    db: DbSettings
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()

import os
from typing import Literal

from pydantic import (
    BaseModel,
    PostgresDsn,
)
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseModel):
    NAME: str = os.getenv(
        "POSTGRES_DB",
        "example_db",
    )
    USER: str = os.getenv(
        "POSTGRES_USER",
        "admin",
    )
    PASS: str = os.getenv(
        "POSTGRES_PASSWORD",
        "password",
    )
    HOST: str = os.getenv(
        "DB_HOST",
        "db",
    )
    PORT: int = os.getenv(
        "DB_PORT",
        5432,
    )
    URL: PostgresDsn = f"postgresql+asyncpg://{USER}:{PASS}@{HOST}:{PORT}/{NAME}"

    ECHO: bool = False
    POOL_SIZE: int = 50
    MAX_OVERFLOW: int = 10


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()

    MODE: Literal["DEV", "TEST", "PROD"] = os.getenv("MODE", "TEST")


settings = Settings()

import os
from functools import lru_cache

from pydantic_settings import BaseSettings

from app.core import logger

USE_CACHED_SETTINGS = os.environ.get("USE_CACHED_SETTINGS", "TRUE").lower() == "true"


class Settings(BaseSettings):
    env: str = "prod"
    deta_space_app_hostname: str
    secret_key_length: int = 8

    app_name: str = "URL shortener"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


@lru_cache
def _get_cached_settings() -> Settings:
    settings = Settings()  # pyright:  ignore [reportGeneralTypeIssues]
    logger.info(f"Loading cached settings for: {settings.env}")
    return settings


def get_settings() -> Settings:
    if USE_CACHED_SETTINGS:
        return _get_cached_settings()
    else:
        settings = Settings()  # pyright:  ignore [reportGeneralTypeIssues]
        logger.info(f"Loading settings for: {settings.env}")
        return settings

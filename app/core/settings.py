import os
from functools import lru_cache

from pydantic import BaseSettings

from app.core import logger

USE_CACHED_SETTINGS = os.environ.get("USE_CACHED_SETTINGS", "TRUE").lower() == "true"


class Settings(BaseSettings):
    env: str
    base_url: str

    app_name = "URL shortener"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


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

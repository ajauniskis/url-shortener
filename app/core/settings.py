from functools import lru_cache

from pydantic import BaseSettings

from app.core import logger


class Settings(BaseSettings):
    env: str
    base_url: str
    project_key: str
    project_id: str

    app_name = "URL shortener"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()  # pyright:  ignore [reportGeneralTypeIssues]
    logger.info(f"Loading settings for: {settings.env}")
    return settings

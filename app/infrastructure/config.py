from functools import lru_cache

from pydantic import BaseSettings

from app.core import USE_CACHED_SETTINGS, logger


class DatabaseConfig(BaseSettings):
    database_type: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def _get_cached_database_config() -> DatabaseConfig:
    logger.info("Loading cached database config")
    return DatabaseConfig()  # pyright:  ignore [reportGeneralTypeIssues]


def get_database_config() -> DatabaseConfig:
    if USE_CACHED_SETTINGS:
        return _get_cached_database_config()
    else:
        logger.info("Loading database config")
        return DatabaseConfig()  # pyright:  ignore [reportGeneralTypeIssues]

from functools import lru_cache

from pydantic import BaseSettings


class DatabaseConfig(BaseSettings):
    database_type: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_database_config() -> DatabaseConfig:
    return DatabaseConfig()  # pyright:  ignore [reportGeneralTypeIssues]

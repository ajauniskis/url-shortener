from functools import lru_cache

from pydantic_settings import BaseSettings


class DetaBaseConfig(BaseSettings):
    deta_project_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


@lru_cache
def get_deta_base_config() -> DetaBaseConfig:
    return DetaBaseConfig()  # pyright:  ignore [reportGeneralTypeIssues]

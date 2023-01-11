from functools import lru_cache

from app.infrastructure import get_database_config
from app.infrastructure.abstract_database_client import AbstractDatabaseClient
from app.infrastructure.deta import DetaBaseClient


@lru_cache
def get_database(table_name: str) -> AbstractDatabaseClient:
    valid_database_types = [
        "deta-base",
    ]
    config = get_database_config()

    if config.database_type == "deta-base":
        return DetaBaseClient(table_name)
    else:
        raise ValueError(
            f"Unknown database type: {config.database_type}. "
            + f"Valid database types: {valid_database_types}."
        )
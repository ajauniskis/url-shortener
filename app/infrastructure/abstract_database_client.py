from abc import ABC
from typing import Any, Dict


class AbstractDatabaseClient(ABC):
    def __init__(self, table_name: str) -> None:
        self.table_name = table_name

    async def create(self, model):
        raise NotImplementedError

    async def get(self, key: str) -> Dict[str, Any]:
        raise NotImplementedError

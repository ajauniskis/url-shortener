from abc import ABC, abstractmethod
from typing import Any, Dict, List


class AbstractDatabaseClient(ABC):
    def __init__(self, table_name: str) -> None:
        self.table_name = table_name

    @abstractmethod
    async def create(self, model):
        raise NotImplementedError

    @abstractmethod
    async def get(self, key: str) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def query(self, query: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        raise NotImplementedError

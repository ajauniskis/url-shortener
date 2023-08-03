from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union


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
    async def query(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        key: str,
        record: Dict[str, Union[str, Dict, float, int, bool]],
    ) -> Dict[str, Union[str, Dict, float, int, bool]]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str) -> None:
        raise NotImplementedError

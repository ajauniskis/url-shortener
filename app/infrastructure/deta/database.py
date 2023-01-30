from typing import Any, Dict, List, Union

from pydantic import BaseModel

from app.domain import RecordDoesNotExistExeption
from app.infrastructure.abstract_database_client import AbstractDatabaseClient
from app.infrastructure.deta.base import get_base


class DetaBaseClient(AbstractDatabaseClient):
    def __init__(self, table_name: str) -> None:
        super().__init__(table_name)
        self.base = get_base(self.table_name)

    async def create(self, model) -> BaseModel:
        response = await self.base.put([model.dict()])
        return model.parse_obj(response["processed"]["items"][0])

    async def get(self, key: str) -> Dict[str, Any]:
        response = await self.base.get(key)
        return response

    async def query(self, query: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        response = await self.base.query(query)
        items = response.get("items")
        return items

    async def update(
        self,
        key: str,
        record: Dict[str, Union[str, Dict, float, int, bool]],
    ) -> Dict[str, Union[str, Dict, float, int, bool]]:
        response = await self.base.update(key=key, set=record)
        if "Key not found" in response.get("errors", []):
            raise RecordDoesNotExistExeption
        return {"key": response.get("key"), **response.get("set")}

    async def delete(self, key: str) -> None:
        await self.base.delete(key)

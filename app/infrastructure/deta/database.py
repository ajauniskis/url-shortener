from typing import Any, Dict, List, Union

from aiohttp.client import ClientResponseError
from pydantic import BaseModel

from app.infrastructure.abstract_database_client import AbstractDatabaseClient
from app.infrastructure.deta.base import get_base


class DetaBaseClient(AbstractDatabaseClient):
    def __init__(self, table_name: str) -> None:
        super().__init__(table_name)
        self.base = get_base(self.table_name)

    async def create(self, model) -> BaseModel:
        record = model.model_dump()
        del record["key"]
        response = await self.base.put(model.model_dump())
        model.key = response["key"]
        return model

    async def get(self, key: str) -> Dict[str, Any]:
        response = await self.base.get(key)
        return response

    async def query(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        response = await self.base.fetch(query)
        return response.items

    async def update(
        self,
        key: str,
        record: Dict[str, Union[str, Dict, float, int, bool]],
    ) -> bool:
        try:
            await self.base.update(updates=record, key=key)
            return True
        except ClientResponseError:
            return False

    async def delete(self, key: str) -> None:
        await self.base.delete(key)

from typing import Union

from app.domain import Url
from app.infrastructure import AbstractDatabaseClient, get_database
from app.repositories.abstract_repository import AbstractRepository


class UrlRepository(AbstractRepository):
    def __init__(self) -> None:
        self.table_name = "url"
        self.database: AbstractDatabaseClient = get_database(self.table_name)

    async def create(self, url_model: Url) -> Url:
        return await self.database.create(url_model)

    async def get(self, key: str) -> Union[Url, None]:
        response = await self.database.get(key)
        if not "target_url" in response.keys():
            return None
        return Url(**response)

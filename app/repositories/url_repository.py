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
        if "target_url" not in response.keys():
            return None
        return Url(**response)

    async def get_by_secret_key(self, secret_key: str) -> Union[Url, None]:
        response = await self.database.query(
            [
                {"secret_key": secret_key},
            ]
        )

        if not len(response):
            return None

        return Url(**response[0])  # pyright:  ignore [reportGeneralTypeIssues]

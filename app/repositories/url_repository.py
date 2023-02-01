from __future__ import annotations

from typing import Union

from app.domain import RecordDoesNotExistExeption, Url
from app.infrastructure import AbstractDatabaseClient, get_database
from app.repositories.abstract_repository import AbstractRepository


class UrlRepository(AbstractRepository):
    def __init__(self) -> None:
        self.table_name = "url"
        self.database: AbstractDatabaseClient = get_database(self.table_name)

    async def create(self, model: Url) -> Url:
        return await self.database.create(model)

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

    async def update(self, model: Url) -> Url:
        if not model.key:
            raise RecordDoesNotExistExeption

        response = await self.database.update(
            key=model.key,
            record={
                "secret_key": model.secret_key,
                "target_url": str(model.target_url),
                "is_active": model.is_active,
                "clicks": model.clicks,
            },
        )

        return Url.construct(**response)

    async def delete(self, model: Url) -> None:
        if not model.key:
            raise RecordDoesNotExistExeption

        await self.database.delete(key=model.key)

    @classmethod
    async def get_repository(cls) -> UrlRepository:
        return cls()  # pragma: no cover

from typing import Union

from pydantic import HttpUrl

from app.domain import Url
from app.infrastructure import AbstractDatabaseClient
from app.repositories import UrlRepository


class UrlRepositoryOverride(UrlRepository):
    def __init__(self) -> None:
        self.table_name = "url"

    async def create(self, url_model: Url) -> Url:
        url_model.key = "key"
        url_model.is_active = True
        url_model.clicks = 0
        return url_model

    async def get(self, key: str) -> Union[Url, None]:
        if key == "redirect_url":
            return Url(
                key=key,
                secret_key="secret_key",
                target_url=HttpUrl("https://google.com", scheme="https"),
            )
        elif key == "disabled_redirect_url":
            return Url(
                key=key,
                secret_key="secret_key",
                target_url=HttpUrl("https://google.com", scheme="https"),
                is_active=False,
            )
        else:
            return None


class DatabaseClientOverride(AbstractDatabaseClient):
    async def create(self, model):
        model.key = "key"
        return model.parse_obj(model.dict())

    async def get(self, key):
        if key == "valid_url":
            return {
                "key": "some_key",
                "secret_key": "secret_key",
                "target_url": "https://test.com",
                "is_active": True,
                "clicks": 0,
            }
        else:
            return {}

    async def query(self, query):
        if query == [
            {
                "secret_key": "invalid_key",
            }
        ]:
            return []
        if query == [
            {
                "secret_key": "single_record",
            }
        ]:
            return [
                {
                    "key": "some_key",
                    "secret_key": "single_record",
                    "target_url": HttpUrl("https://google.com", scheme="https"),
                }
            ]
        if query == [
            {
                "secret_key": "multiple_records",
            }
        ]:
            return [
                {
                    "key": "some_key1",
                    "secret_key": "multiple_records",
                    "target_url": HttpUrl("https://google.com", scheme="https"),
                },
                {
                    "key": "some_key2",
                    "secret_key": "multiple_records",
                    "target_url": HttpUrl("https://google.com", scheme="https"),
                },
            ]
        else:
            raise NotImplementedError

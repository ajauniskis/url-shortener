from __future__ import annotations

from typing import Dict, Union

from pydantic import HttpUrl

from app.domain import Url
from app.infrastructure import AbstractDatabaseClient
from app.repositories import UrlRepository


class UrlRepositoryOverride(UrlRepository):
    def __init__(self) -> None:
        self.table_name = "url"

    async def create(self, model: Url) -> Url:
        model.key = "key"
        model.is_active = True
        model.clicks = 0
        return model

    async def get(self, key: str) -> Union[Url, None]:
        if key == "redirect_url":
            return Url(
                key=key,
                secret_key="secret_key",
                target_url=HttpUrl("https://google.com"),
            )
        elif key == "disabled_redirect_url":
            return Url(
                key=key,
                secret_key="secret_key",
                target_url=HttpUrl("https://google.com"),
                is_active=False,
            )
        else:
            return None

    async def get_by_secret_key(self, secret_key: str) -> Union[Url, None]:
        if secret_key == "valid_secret_key":
            return Url(
                key="key",
                secret_key=secret_key,
                target_url=HttpUrl("https://google.com"),
                is_active=True,
            )

        if secret_key == "inactive_secret_key":
            return Url(
                key="key",
                secret_key=secret_key,
                target_url=HttpUrl("https://google.com"),
                is_active=False,
            )

        return None

    async def update(self, model: Url) -> Url:
        return model

    async def delete(self, model: Url) -> None:
        return

    @classmethod
    async def get_repository(cls) -> UrlRepositoryOverride:
        return cls()


class DatabaseClientOverride(AbstractDatabaseClient):
    async def create(self, model):
        model.key = "key"
        return model.parse_obj(model.model_dump())

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
        if query == {"secret_key": "invalid_key"}:
            return []
        if query == {"secret_key": "single_record"}:
            return [
                {
                    "key": "some_key",
                    "secret_key": "single_record",
                    "target_url": HttpUrl("https://google.com"),
                }
            ]
        if query == {"secret_key": "multiple_records"}:
            return [
                {
                    "key": "some_key1",
                    "secret_key": "multiple_records",
                    "target_url": HttpUrl("https://google.com"),
                },
                {
                    "key": "some_key2",
                    "secret_key": "multiple_records",
                    "target_url": HttpUrl("https://google.com"),
                },
            ]
        else:
            raise NotImplementedError

    async def update(
        self,
        key: str,
        record: Dict[str, Union[str, Dict, float, int, bool]],
    ) -> Dict[str, Union[str, Dict, float, int, bool]]:
        if key == "test_update_returns_url_model":
            return {
                "key": "test_update_returns_url_model",
                "secret_key": "secret_key",
                "target_url": "https://example.com",
                "is_active": True,
                "clicks": 1,
            }
        else:
            raise NotImplementedError

    async def delete(self, key: str) -> None:
        return

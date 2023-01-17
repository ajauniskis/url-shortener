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


class DatabaseClientOverride(AbstractDatabaseClient):
    async def create(self, model):
        model.key = "key"
        return model.parse_obj(model.dict())

from app.domain import Url
from app.repositories import UrlRepository


class UrlRepositoryOverride(UrlRepository):
    def __init__(self) -> None:
        self.table_name = "url"

    async def create_url(self, url_model: Url) -> Url:
        url_model.key = "key"
        url_model.is_active = True
        url_model.clicks = 0
        return url_model

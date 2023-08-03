from typing import Optional

from pydantic import BaseModel, HttpUrl, field_serializer

from app.core import get_settings
from app.domain.exception import (
    RecordDoesNotExistExeption,
    UrlIsActiveException,
    UrlIsNotActiveException,
)


class Url(BaseModel):
    key: Optional[str] = None
    secret_key: str
    target_url: HttpUrl
    is_active: bool = True
    clicks: int = 0

    @field_serializer("target_url")
    def serialize_dt(self, target_url: HttpUrl, _info):
        return str(target_url)

    @property
    def short_url(self) -> HttpUrl:
        if not self.key:
            raise RecordDoesNotExistExeption
        return HttpUrl(get_settings().deta_space_app_hostname + f"/api/url/{self.key}")

    async def click(self) -> None:
        self.clicks += 1

    async def activate(self) -> None:
        if not self.is_active:
            self.is_active = True
        else:
            raise UrlIsActiveException

    async def deactivate(self) -> None:
        if self.is_active:
            self.is_active = False
        else:
            raise UrlIsNotActiveException

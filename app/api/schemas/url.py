from pydantic import BaseModel, HttpUrl


class URLBase(BaseModel):
    target_url: HttpUrl


class URL(URLBase):
    is_active: bool
    clicks: int


class URLInfo(URL):
    url: HttpUrl
    admin_url: str

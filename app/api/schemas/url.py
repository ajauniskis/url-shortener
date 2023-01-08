from pydantic import BaseModel, HttpUrl


class URLBase(BaseModel):
    target_url: HttpUrl

    class Config:
        schema_extra = {
            "example": {"target_url": "https://google.com"},
        }


class URL(URLBase):
    is_active: bool
    clicks: int


class URLInfo(URL):
    url: HttpUrl
    admin_url: str

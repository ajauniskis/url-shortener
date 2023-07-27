from pydantic import BaseModel, HttpUrl, field_serializer


class URLBase(BaseModel):
    target_url: HttpUrl

    @field_serializer("target_url")
    def serialize_dt(self, target_url: HttpUrl, _info):
        return str(target_url)


class URL(URLBase):
    is_active: bool
    clicks: int


class URLInfo(URL):
    url: HttpUrl
    secret_key: str

    @field_serializer("target_url")
    def serialize_dt(self, url: HttpUrl, _info):
        return str(url)

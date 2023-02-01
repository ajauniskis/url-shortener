from app.api.schemas.url import URLBase


class PeekUrlResponse(URLBase):
    class Config:
        schema_extra = {
            "example": {"target_url": "https://google.com"},
        }

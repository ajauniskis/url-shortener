from app.api.schemas.url import URLBase


class PeekUrlResponse(URLBase):
    class Config:
        json_schema_extra = {
            "example": {"target_url": "https://google.com"},
        }

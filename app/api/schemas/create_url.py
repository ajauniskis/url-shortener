from app.api.schemas.admin_url import AdminUrlResponse
from app.api.schemas.url import URLBase


class CreateUrlRequest(URLBase):
    class Config:
        json_schema_extra = {
            "example": {"target_url": "https://google.com"},
        }


class CreateUrlResponse(AdminUrlResponse):
    pass

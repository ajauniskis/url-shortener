from app.api.schemas.url import URLBase
from app.api.schemas.admin_url import AdminUrlResponse


class CreateUrlRequest(URLBase):
    class Config:
        schema_extra = {
            "example": {"target_url": "https://google.com"},
        }


class CreateUrlResponse(AdminUrlResponse):
    pass

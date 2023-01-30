from app.api.schemas.url import URLInfo
from app.core import get_settings


class AdminUrlResponse(URLInfo):
    pass

    class Config:
        schema_extra = {
            "example": {
                "url": f"{get_settings().base_url}/api/url/sampleUrlKey",
                "secret_key": "SAMPLESECRETKEY",
                "target_url": "https://example.com",
                "is_active": True,
                "clicks": 0,
            },
        }

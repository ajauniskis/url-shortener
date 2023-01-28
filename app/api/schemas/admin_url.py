from app.api.schemas.url import URLInfo
from app.core import get_settings



class AdminUrlResponse(URLInfo):
    pass

    class Config:
        schema_extra = {
            "example": {
                "url": f"{get_settings().base_url}/api/url/oo0etstpl045",
                "secret_key": "VRXAKPWG",
                "target_url": "https://google.com",
                "is_active": True,
                "clicks": 0,
            },
        }

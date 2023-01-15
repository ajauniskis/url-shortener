from app.api.schemas.url import URL, URLBase


class CreateUrlRequest(URLBase):
    class Config:
        schema_extra = {
            "example": {"target_url": "https://google.com"},
        }


class CreateUrlResponse(URL):
    key: str
    secret_key: str

    class Config:
        schema_extra = {
            "example": {
                "key": "oo0etstpl045",
                "secret_key": "VRXAKPWG",
                "target_url": "https://google.com",
                "is_active": True,
                "clicks": 0,
            },
        }

from typing import Optional

from pydantic import BaseModel, HttpUrl


class Url(BaseModel):
    key: Optional[str] = None
    secret_key: str
    target_url: HttpUrl
    is_active: bool = True
    clicks: int = 0

    async def click(self):
        self.clicks += 1

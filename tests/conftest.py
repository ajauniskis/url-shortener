import os
from typing import Optional

from pydantic import BaseModel

os.environ["USE_CACHED_SETTINGS"] = "FALSE"
os.environ["ENV"] = "test"


class TestDomainModel(BaseModel):
    key: Optional[str] = None
    value: str

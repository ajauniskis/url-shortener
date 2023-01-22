import asyncio
import os
from typing import Optional

import pytest
from pydantic import BaseModel

os.environ["USE_CACHED_SETTINGS"] = "FALSE"
os.environ["ENV"] = "test"


class TestDomainModel(BaseModel):
    key: Optional[str] = None
    value: str


@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop()

    yield loop

    pending = asyncio.tasks.all_tasks(loop)
    loop.run_until_complete(asyncio.gather(*pending))
    loop.run_until_complete(asyncio.sleep(1))

    loop.close()

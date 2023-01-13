from functools import lru_cache

from aiodeta import Deta
from aiodeta.client import _Base

from app.infrastructure.deta.config import get_deta_base_config


@lru_cache
def get_base(base_name: str) -> _Base:
    deta_base_config = get_deta_base_config()

    deta = Deta(
        project_key=deta_base_config.deta_project_key,
        project_id=deta_base_config.deta_project_id,
    )

    return deta.Base(base_name)

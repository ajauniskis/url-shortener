from functools import lru_cache

from aiodeta import Deta
from aiodeta.client import _Base

from app.core import USE_CACHED_SETTINGS
from app.infrastructure.deta.config import get_deta_base_config


@lru_cache
def _get_cached_base(base_name: str) -> _Base:
    deta_base_config = get_deta_base_config()

    deta = Deta(
        project_key=deta_base_config.deta_project_key,
    )

    return deta.Base(base_name)


def get_base(base_name: str) -> _Base:
    if USE_CACHED_SETTINGS:
        return _get_cached_base(base_name)
    else:
        deta_base_config = get_deta_base_config()

        deta = Deta(
            project_key=deta_base_config.deta_project_key,
        )

        return deta.Base(base_name)

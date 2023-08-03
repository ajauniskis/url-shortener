from functools import lru_cache

from deta import Deta
from deta._async.client import _AsyncBase

from app.core import USE_CACHED_SETTINGS
from app.infrastructure.deta.config import get_deta_base_config


@lru_cache
def _get_cached_base(base_name: str) -> _AsyncBase:
    deta_base_config = get_deta_base_config()

    return Deta(project_key=deta_base_config.deta_project_key).AsyncBase(name=base_name)


def get_base(base_name: str) -> _AsyncBase:
    if USE_CACHED_SETTINGS:
        return _get_cached_base(base_name)
    else:
        deta_base_config = get_deta_base_config()

        return Deta(project_key=deta_base_config.deta_project_key).AsyncBase(
            name=base_name
        )

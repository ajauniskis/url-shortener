from functools import lru_cache

from deta._async.client import _AsyncBase

from app.core import USE_CACHED_SETTINGS
from app.infrastructure.deta.config import get_deta_base_config


@lru_cache
def _get_cached_base(base_name: str) -> _AsyncBase:
    deta_base_config = get_deta_base_config()

    return _AsyncBase(
        name=base_name,
        project_key=deta_base_config.deta_project_key,
        project_id=deta_base_config.deta_project_id,
    )


def get_base(base_name: str) -> _AsyncBase:
    if USE_CACHED_SETTINGS:
        return _get_cached_base(base_name)
    else:
        deta_base_config = get_deta_base_config()

        return _AsyncBase(
            name=base_name,
            project_key=deta_base_config.deta_project_key,
            project_id=deta_base_config.deta_project_id,
        )

from app.infrastructure.deta.config import get_deta_base_config
from app.infrastructure.deta.database import DetaBaseClient

__all__ = [
    "DetaBaseClient",
    "get_deta_base_config",
]

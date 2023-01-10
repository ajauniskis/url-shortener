from app.infrastructure.abstract_database_client import AbstractDatabaseClient
from app.infrastructure.deta.base import get_base


class DetaBaseClient(AbstractDatabaseClient):
    def __init__(self, table_name: str) -> None:
        super().__init__(table_name)
        self.base = get_base(self.table_name)

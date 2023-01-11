from app.infrastructure import AbstractDatabaseClient, get_database
from app.repositories.abstract_repository import AbstractRepository


class UrlRepository(AbstractRepository):
    def __init__(self) -> None:
        self.table_name = "url"
        self.database: AbstractDatabaseClient = get_database(self.table_name)

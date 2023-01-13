from abc import ABC


class AbstractDatabaseClient(ABC):
    def __init__(self, table_name: str) -> None:
        self.table_name = table_name

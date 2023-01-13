from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from app.repositories import UrlRepository


class TestUrlRepository(IsolatedAsyncioTestCase):
    @patch("app.infrastructure.config.DatabaseConfig")
    async def test_url_repository__table_name__returns_url(self, patch_database_config):
        patch_database_config.return_value.database_type = "deta-base"

        repo = UrlRepository()
        self.assertEqual(
            repo.table_name,
            "url",
        )

    @patch("app.infrastructure.config.DatabaseConfig")
    async def test_url_repository__database__returns_database_client(
        self, patch_database_config
    ):
        patch_database_config.return_value.database_type = "deta-base"

        repo = UrlRepository()
        actual = type(repo.database).__bases__[0].__name__

        self.assertEqual(
            actual,
            "AbstractDatabaseClient",
        )

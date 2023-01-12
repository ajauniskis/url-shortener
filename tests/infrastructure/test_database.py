from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from app.infrastructure import get_database


class TestGetDatabase(IsolatedAsyncioTestCase):
    @patch("app.infrastructure.config.DatabaseConfig")
    async def test_get_database__invalid_database_type__thorws(self, patch_config):
        patch_config.return_value.database_type = "invalid-database"

        with self.assertRaises(ValueError) as exception_context:
            get_database("some_table")

        self.assertEqual(
            str(exception_context.exception),
            "Unknown database type: invalid-database. "
            + "Valid database types: ['deta-base'].",
        )

    @patch("app.infrastructure.config.DatabaseConfig")
    async def test_get_database__returns_database_client(self, patch_config):
        patch_config.return_value.database_type = "deta-base"

        database = get_database("some_table")
        actual = type(database).__bases__[0].__name__

        self.assertEqual(
            actual,
            "AbstractDatabaseClient",
        )

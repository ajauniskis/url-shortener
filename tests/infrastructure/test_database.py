from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from app.infrastructure import get_database
from app.infrastructure.database import _get_cached_database


class TestGetDatabase(IsolatedAsyncioTestCase):
    @patch("app.infrastructure.database.USE_CACHED_SETTINGS", True)
    @patch("app.infrastructure.database._get_cached_database")
    async def test_get_database__USE_CACHE_SETTINGS_true__uses_cache(
        self, patch_get_cached_database
    ):
        get_database("some_table")
        patch_get_cached_database.assert_called()

    @patch("app.infrastructure.database._get_cached_database")
    def test_get_database__USE_CACHED_SETTINGS_false__not_uses_cache(
        self, patch_get_cached_database
    ):
        get_database("some_table")
        patch_get_cached_database.assert_not_called()

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

    @patch("app.infrastructure.config.DatabaseConfig")
    async def test_get_cached_database__invalid_database_type__thorws(
        self, patch_config
    ):
        patch_config.return_value.database_type = "invalid-database"

        with self.assertRaises(ValueError) as exception_context:
            _get_cached_database("some_table")

        self.assertEqual(
            str(exception_context.exception),
            "Unknown database type: invalid-database. "
            + "Valid database types: ['deta-base'].",
        )

    @patch("app.infrastructure.config.DatabaseConfig")
    async def test_get_cached_database__returns_database_client(self, patch_config):
        patch_config.return_value.database_type = "deta-base"

        database = _get_cached_database("some_table")
        actual = type(database).__bases__[0].__name__

        self.assertEqual(
            actual,
            "AbstractDatabaseClient",
        )

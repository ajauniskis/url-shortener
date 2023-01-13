from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from app.infrastructure import get_database_config
from app.infrastructure.config import DatabaseConfig, _get_cached_database_config


class TestGetDatabaseConfig(IsolatedAsyncioTestCase):
    @patch("app.infrastructure.config.USE_CACHED_SETTINGS", True)
    @patch("app.infrastructure.config._get_cached_database_config")
    async def test_get_database_config__USE_CACHE_SETTINGS_true__uses_cache(
        self, patch_get_cached_database_config
    ):
        get_database_config()
        patch_get_cached_database_config.assert_called()

    @patch("app.infrastructure.config._get_cached_database_config")
    def test_get_database_config__USE_CACHED_SETTINGS_false__not_uses_cache(
        self, patch_get_cached_settings
    ):
        get_database_config()
        patch_get_cached_settings.assert_not_called()

    @patch("app.infrastructure.config.USE_CACHED_SETTINGS", True)
    def test_get_cached_database_config__logs_and_returns(self):

        with self.assertLogs() as logger_context:
            actual = _get_cached_database_config()

        self.assertEqual(
            logger_context.output[0],
            "INFO:uvicorn.info:Loading cached database config",
        )

        self.assertEqual(
            actual,
            DatabaseConfig(),  # pyright:  ignore [reportGeneralTypeIssues]
        )

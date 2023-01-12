from unittest import TestCase
from unittest.mock import patch

from app.core import get_settings
from app.core.settings import Settings, _get_cached_settings


class TestSettings(TestCase):
    @patch("app.core.settings.USE_CACHED_SETTINGS", True)
    @patch("app.core.settings._get_cached_settings")
    def test_get_settings__USE_CACHED_SETTINGS_true__uses_cache(
        self, patch_get_cached_settings
    ):
        get_settings()
        patch_get_cached_settings.assert_called()

    @patch("app.core.settings._get_cached_settings")
    def test_get_settings__USE_CACHED_SETTINGS_false__not_uses_cache(
        self, patch_get_cached_settings
    ):
        get_settings()
        patch_get_cached_settings.assert_not_called()

    @patch("app.core.settings.USE_CACHED_SETTINGS", True)
    def test_get_cached_settings__logs_and_returns(self):

        with self.assertLogs() as logger_context:
            actual = _get_cached_settings()

        self.assertEqual(
            logger_context.output[0],
            "INFO:uvicorn.info:Loading cached settings for: test",
        )

        self.assertEqual(
            actual,
            Settings(),  # pyright:  ignore [reportGeneralTypeIssues]
        )

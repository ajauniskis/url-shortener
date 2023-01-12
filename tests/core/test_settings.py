from unittest import TestCase
from unittest.mock import patch

from app.core import get_settings


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

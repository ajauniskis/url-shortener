from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch
from app.infrastructure.deta.base import get_base


class TestGetBase(IsolatedAsyncioTestCase):
    @patch("app.infrastructure.deta.base.USE_CACHED_SETTINGS", True)
    @patch("app.infrastructure.deta.base._get_cached_base")
    async def test_get_base__USE_CACHE_SETTINGS_true__uses_cache(
        self, patch_get_cached_base
    ):
        get_base("test")
        patch_get_cached_base.assert_called()

    @patch("app.infrastructure.deta.base.USE_CACHED_SETTINGS", False)
    @patch("app.infrastructure.deta.base._get_cached_base")
    async def test_get_base__USE_CACHE_SETTINGS_false__not_uses_cache(
        self, patch_get_cached_base
    ):
        get_base("test")
        patch_get_cached_base.assert_not_called()

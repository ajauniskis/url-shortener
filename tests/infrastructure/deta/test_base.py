from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from deta._async.client import _AsyncBase

from app.infrastructure.deta.base import _get_cached_base, get_base
from tests.conftest import TEST_BASE


class TestGetBase(IsolatedAsyncioTestCase):
    @patch("app.infrastructure.deta.base.USE_CACHED_SETTINGS", True)
    @patch("app.infrastructure.deta.base._get_cached_base")
    async def test_get_base__USE_CACHE_SETTINGS_true__uses_cache(
        self, patch_get_cached_base
    ):
        get_base(TEST_BASE)
        patch_get_cached_base.assert_called()

    @patch("app.infrastructure.deta.base.USE_CACHED_SETTINGS", False)
    @patch("app.infrastructure.deta.base._get_cached_base")
    async def test_get_base__USE_CACHE_SETTINGS_false__not_uses_cache(
        self, patch_get_cached_base
    ):
        get_base(TEST_BASE)
        patch_get_cached_base.assert_not_called()

    @patch("app.infrastructure.deta.base.USE_CACHED_SETTINGS", True)
    async def test_get_cached_base__returns_base(self):
        actual = _get_cached_base(TEST_BASE)

        self.assertIsInstance(
            actual,
            _AsyncBase,
        )

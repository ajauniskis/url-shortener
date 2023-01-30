from unittest import IsolatedAsyncioTestCase

from pydantic import HttpUrl

from app.core import get_settings
from app.domain.exception import RecordDoesNotExistExeption, UrlIsNotActiveException
from app.domain.url import Url


class TestUrl(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.test_model = Url(
            key="test-key",
            secret_key="test-secret-key",
            target_url=HttpUrl(
                "https://test-url.com",
                scheme="https",
            ),
            is_active=True,
            clicks=0,
        )

    async def test_short_url__returns_short_url(self):
        actual = self.test_model.short_url
        expected = HttpUrl(
            get_settings().base_url + f"/api/url/{self.test_model.key}",
            scheme="https",
        )

        self.assertEqual(
            actual,
            expected,
        )

    async def test_short_url__no_key__returns_short_url(self):
        self.test_model.key = None

        with self.assertRaises(RecordDoesNotExistExeption):
            self.test_model.short_url

    async def test_click__increments_clicks(self):
        expected = self.test_model.clicks + 1
        await self.test_model.click()
        actual = self.test_model.clicks

        self.assertEqual(
            actual,
            expected,
        )

    async def test_deactivate__deactivates_url(self):
        await self.test_model.deactivate()

        self.assertFalse(self.test_model.is_active)

    async def test_deactivate__inactive_url__throws(self):
        self.test_model.is_active = False
        with self.assertRaises(UrlIsNotActiveException):
            await self.test_model.deactivate()

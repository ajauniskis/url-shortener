from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from fastapi.testclient import TestClient
from pydantic import HttpUrl

from app.api.schemas.create_url import CreateUrlResponse
from main import app
from tests.overrides import UrlRepositoryOverride


class TestUrl(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.client = TestClient(app)

    async def test_create_url__invalid_url__returns_422(self):
        actual = self.client.post(
            "/api/url",
            json={
                "target_url": "invalid_url",
            },
        )

        self.assertEqual(
            actual.status_code,
            422,
        )

        self.assertEqual(
            actual.json(),
            {
                "detail": [
                    {
                        "loc": ["body", "target_url"],
                        "msg": "invalid or missing URL scheme",
                        "type": "value_error.url.scheme",
                    }
                ]
            },
        )

    async def test_create_url__invalid_request_body__returns_422(self):
        actual = self.client.post(
            "/api/url",
            json={},
        )

        self.assertEqual(
            actual.status_code,
            422,
        )

        self.assertEqual(
            actual.json(),
            {
                "detail": [
                    {
                        "loc": ["body", "target_url"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
        )

    @patch(
        "app.api.endpoints.url.UrlRepository",
        new=UrlRepositoryOverride,
    )
    async def test_create_url__returns_created_url(self):
        actual = self.client.post(
            "/api/url",
            json={
                "target_url": "https://test.com",
            },
        )

        expected = CreateUrlResponse(
            key="key",
            secret_key="",
            target_url=HttpUrl("https://test.com", scheme="https"),
            is_active=True,
            clicks=0,
        )

        self.assertEqual(
            actual.status_code,
            200,
        )

        self.assertEqual(
            actual.json()["key"],
            expected.key,
        )

        self.assertEqual(
            actual.json()["target_url"],
            expected.target_url,
        )

        self.assertEqual(
            actual.json()["is_active"],
            expected.is_active,
        )

        self.assertEqual(
            actual.json()["clicks"],
            expected.clicks,
        )

    @patch(
        "app.api.endpoints.url.UrlRepository",
        new=UrlRepositoryOverride,
    )
    async def test_forward_to_url__redirects_to_url(self):
        actual = self.client.get(
            "/api/url/redirect_url",
            follow_redirects=False,
        )

        self.assertEqual(
            actual.headers["location"],
            "https://google.com",
        )

        self.assertEqual(
            actual.status_code,
            307,
        )

    @patch(
        "app.api.endpoints.url.UrlRepository",
        new=UrlRepositoryOverride,
    )
    async def test_forward_to_url__invalid_key__returns_404(self):
        redirect_key = "invalid_redirect_url"
        actual = self.client.get(
            f"/api/url/{redirect_key}",
            follow_redirects=False,
        )

        expected = {
            "detail": f"Requested key: '{redirect_key}' does not exist.",
        }

        self.assertEqual(
            actual.json(),
            expected,
        )

        self.assertEqual(
            actual.status_code,
            404,
        )

    @patch(
        "app.api.endpoints.url.UrlRepository",
        new=UrlRepositoryOverride,
    )
    async def test_forward_to_url__disabled_key__returns_400(self):
        redirect_key = "disabled_redirect_url"
        actual = self.client.get(
            f"/api/url/{redirect_key}",
            follow_redirects=False,
        )

        expected = {
            "detail": f"Requested key: '{redirect_key}' is not active.",
        }

        self.assertEqual(
            actual.json(),
            expected,
        )

        self.assertEqual(
            actual.status_code,
            400,
        )

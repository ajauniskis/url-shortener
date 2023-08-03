from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from fastapi.testclient import TestClient
from pydantic import HttpUrl

from app.api.schemas.admin_url import AdminUrlResponse
from app.api.schemas.create_url import CreateUrlResponse
from app.api.schemas.peek_url import PeekUrlResponse
from app.core.settings import get_settings
from app.domain import Url
from app.repositories.url_repository import UrlRepository
from main import app
from tests.overrides import UrlRepositoryOverride


class TestUrl(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.client = TestClient(app)
        app.dependency_overrides[
            UrlRepository.get_repository
        ] = UrlRepositoryOverride.get_repository

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
                        "type": "url_parsing",
                        "loc": ["body", "target_url"],
                        "msg": "Input should be a valid URL,"
                        + " relative URL without a base",
                        "input": "invalid_url",
                        "ctx": {"error": "relative URL without a base"},
                        "url": "https://errors.pydantic.dev/2.1/v/url_parsing",
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
                        "type": "missing",
                        "loc": ["body", "target_url"],
                        "msg": "Field required",
                        "input": {},
                        "url": "https://errors.pydantic.dev/2.1/v/missing",
                    }
                ]
            },
        )

    @patch("app.domain.secret_key.SecretKey.generate_unique")
    async def test_create_url__returns_created_url(self, patch_generate_unique):
        patch_generate_unique.return_value = "valid_secret_key"
        actual = self.client.post(
            "/api/url",
            json={
                "target_url": "https://google.com",
            },
        )

        expected = CreateUrlResponse(
            url=HttpUrl("http://127.0.0.1:8000/api/url/key"),
            secret_key="valid_secret_key",
            target_url=HttpUrl("https://google.com"),
            is_active=True,
            clicks=0,
        )

        self.assertEqual(
            actual.status_code,
            200,
        )

        self.assertEqual(
            CreateUrlResponse(**actual.json()),
            expected,
        )

    async def test_forward_to_url__redirects_to_url(self):
        actual = self.client.get(
            "/api/url/redirect_url",
            follow_redirects=False,
        )

        self.assertEqual(
            actual.headers["location"],
            "https://google.com/",
        )

        self.assertEqual(
            actual.status_code,
            307,
        )

    @patch("tests.overrides.UrlRepositoryOverride.update")
    async def test_forward_to_url__increments_clicks(self, mock_update):
        self.client.get(
            "/api/url/redirect_url",
            follow_redirects=False,
        )

        mock_update.assert_called_with(
            Url(
                key="redirect_url",
                secret_key="secret_key",
                target_url=HttpUrl("https://google.com"),
                clicks=1,
            )
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

    @patch("tests.overrides.UrlRepositoryOverride.update")
    async def test_forward_to_url__invalid_key__doesnt_increment_clicks(
        self, mock_update
    ):
        self.client.get(
            "/api/url/invalid_redirect_url",
            follow_redirects=False,
        )

        mock_update.assert_not_called()

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

    @patch("tests.overrides.UrlRepositoryOverride.update")
    async def test_forward_to_url__disabled_key__doesnt_increment_clicks(
        self, mock_update
    ):
        self.client.get(
            "/api/url/disabled_redirect_url",
            follow_redirects=False,
        )

        mock_update.assert_not_called()

    async def test_get_admin_info__returns_admin_response(self):
        actual = self.client.get(
            "/api/url/admin/valid_secret_key",
        )

        expected = AdminUrlResponse(
            secret_key="valid_secret_key",
            target_url=HttpUrl("https://google.com"),
            is_active=True,
            url=HttpUrl(get_settings().deta_space_app_hostname + "/api/url/key"),
            clicks=0,
        )

        self.assertEqual(
            AdminUrlResponse(**actual.json()),
            expected,
        )

        self.assertEqual(
            actual.status_code,
            200,
        )

    async def test_get_admin_info__invalid_secret_key__returns_404(self):
        actual = self.client.get(
            "/api/url/admin/invalid_secret_key",
        )

        expected = {
            "detail": "Requested secret key: 'invalid_secret_key' does not exist."
        }

        self.assertEqual(
            actual.json(),
            expected,
        )

        self.assertEqual(
            actual.status_code,
            404,
        )

    async def test_deactivate_url__returns_inactive_url(self):
        actual = self.client.post(
            "/api/url/admin/deactivate/valid_secret_key",
        )

        expected = AdminUrlResponse(
            secret_key="valid_secret_key",
            target_url=HttpUrl("https://google.com"),
            is_active=False,
            url=HttpUrl(get_settings().deta_space_app_hostname + "/api/url/key"),
            clicks=0,
        )

        self.assertEqual(
            AdminUrlResponse(**actual.json()),
            expected,
        )

        self.assertEqual(
            actual.status_code,
            200,
        )

    async def test_deactivate_url__inactive_url__returns_400(self):
        actual = self.client.post(
            "/api/url/admin/deactivate/inactive_secret_key",
        )

        expected = {
            "detail": "Requested secret key: 'inactive_secret_key' is not active."
        }

        self.assertEqual(
            actual.json(),
            expected,
        )

        self.assertEqual(
            actual.status_code,
            400,
        )

    async def test_deactivate_url__invalid_secret_key__returns_404(self):
        actual = self.client.post(
            "/api/url/admin/deactivate/invalid_secret_key",
        )

        expected = {
            "detail": "Requested secret key: 'invalid_secret_key' does not exist."
        }

        self.assertEqual(
            actual.json(),
            expected,
        )

        self.assertEqual(
            actual.status_code,
            404,
        )

    async def test_activate_url__returns_active_url(self):
        actual = self.client.post(
            "/api/url/admin/activate/inactive_secret_key",
        )

        expected = AdminUrlResponse(
            secret_key="inactive_secret_key",
            target_url=HttpUrl("https://google.com"),
            is_active=True,
            url=HttpUrl(get_settings().deta_space_app_hostname + "/api/url/key"),
            clicks=0,
        )

        self.assertEqual(
            AdminUrlResponse(**actual.json()),
            expected,
        )

        self.assertEqual(
            actual.status_code,
            200,
        )

    async def test_activate_url__active_url__returns_400(self):
        actual = self.client.post(
            "/api/url/admin/activate/valid_secret_key",
        )

        expected = {
            "detail": "Requested secret key: 'valid_secret_key' is already active."
        }

        self.assertEqual(
            actual.json(),
            expected,
        )

        self.assertEqual(
            actual.status_code,
            400,
        )

    async def test_activate_url__invalid_secret_key__returns_404(self):
        actual = self.client.post(
            "/api/url/admin/activate/invalid_secret_key",
        )

        expected = {
            "detail": "Requested secret key: 'invalid_secret_key' does not exist."
        }

        self.assertEqual(
            actual.json(),
            expected,
        )

        self.assertEqual(
            actual.status_code,
            404,
        )

    async def test_delete_url__returns_204(self):
        actual = self.client.delete(
            "/api/url/admin/valid_secret_key",
        )

        self.assertEqual(
            actual.status_code,
            204,
        )

    async def test_delete_url__invalid_secret_key__returns_404(self):
        actual = self.client.delete(
            "/api/url/admin/invalid_secret_key",
        )

        expected = {
            "detail": "Requested secret key: 'invalid_secret_key' does not exist."
        }

        self.assertEqual(
            actual.json(),
            expected,
        )

        self.assertEqual(
            actual.status_code,
            404,
        )

    async def test_peek_url__returns_target_url(self):
        actual = self.client.get("/api/url/peek/redirect_url")

        expected = PeekUrlResponse(target_url=HttpUrl("https://google.com"))

        self.assertEqual(
            actual.json(),
            expected.model_dump(),
        )

        self.assertEqual(
            actual.status_code,
            200,
        )

    async def test_peek_url__invalid_key__returns_404(self):
        actual = self.client.get("/api/url/peek/invalid_key")

        expected = {"detail": "Requested key: 'invalid_key' does not exist."}

        self.assertEqual(
            actual.json(),
            expected,
        )

        self.assertEqual(
            actual.status_code,
            404,
        )

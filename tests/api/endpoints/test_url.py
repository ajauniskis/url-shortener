from unittest import TestCase

from fastapi.testclient import TestClient

from main import app


class TestUrl(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_create_url__invalid_url__returns_422(self):
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

    def test_create_url__invalid_request_body__returns_422(self):
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

    def test_create_url__returns_respone(self):
        actual = self.client.post(
            "/api/url",
            json={
                "target_url": "https://test.com",
            },
        )

        self.assertEqual(
            actual.status_code,
            200,
        )

        self.assertEqual(
            actual.json(),
            "Not implemented yet",
        )

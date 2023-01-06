from unittest import TestCase

from fastapi.testclient import TestClient

from app.main import app


class TestIndex(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_get_index__returns_200(self):
        actual = self.client.get("/").status_code

        self.assertEqual(
            actual,
            200,
        )

    def test_get_index__redirects_to_docs(self):
        actual = self.client.get("/").url
        expected = self.client.get("/docs").url

        self.assertEqual(
            actual,
            expected,
        )

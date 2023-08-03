from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from pydantic import HttpUrl

from app.domain import RecordDoesNotExistExeption, Url
from app.repositories import UrlRepository
from tests.overrides import DatabaseClientOverride


class TestUrlRepository(IsolatedAsyncioTestCase):
    @patch("app.infrastructure.config.DatabaseConfig")
    async def test_url_repository__table_name__returns_url(self, patch_database_config):
        patch_database_config.return_value.database_type = "deta-base"

        repo = UrlRepository()
        self.assertEqual(
            repo.table_name,
            "url",
        )

    @patch("app.infrastructure.config.DatabaseConfig")
    async def test_url_repository__database__returns_database_client(
        self, patch_database_config
    ):
        patch_database_config.return_value.database_type = "deta-base"

        repo = UrlRepository()
        actual = type(repo.database).__bases__[0].__name__

        self.assertEqual(
            actual,
            "AbstractDatabaseClient",
        )

    @patch("app.infrastructure.config.DatabaseConfig")
    @patch("app.repositories.url_repository.get_database")
    async def test_create__returns_url_model(
        self, patch_get_database, patch_database_config
    ):
        patch_database_config.return_value.database_type = "deta-base"
        patch_get_database.return_value = DatabaseClientOverride("url")
        repo = UrlRepository()
        model = Url(
            secret_key="secret_key",
            target_url=HttpUrl("https://example.com"),
            is_active=True,
            clicks=0,
        )
        actual = await repo.create(model)
        expected = Url(
            key="key",
            secret_key="secret_key",
            target_url=HttpUrl("https://example.com"),
            is_active=True,
            clicks=0,
        )
        self.assertEqual(
            actual,
            expected,
        )

    @patch("app.infrastructure.config.DatabaseConfig")
    @patch("app.repositories.url_repository.get_database")
    async def test_get__returns_url_model(
        self, patch_get_database, patch_database_config
    ):
        patch_database_config.return_value.database_type = "deta-base"
        patch_get_database.return_value = DatabaseClientOverride("url")
        repo = UrlRepository()

        actual = await repo.get("valid_url")
        expected = Url(
            key="some_key",
            secret_key="secret_key",
            target_url=HttpUrl("https://test.com"),
            is_active=True,
            clicks=0,
        )

        self.assertEqual(
            actual,
            expected,
        )

    @patch("app.infrastructure.config.DatabaseConfig")
    @patch("app.repositories.url_repository.get_database")
    async def test_get__invalid_key__returns_none(
        self, patch_get_database, patch_database_config
    ):
        patch_database_config.return_value.database_type = "deta-base"
        patch_get_database.return_value = DatabaseClientOverride("url")
        repo = UrlRepository()

        actual = await repo.get("invalid_key")

        self.assertEqual(
            actual,
            None,
        )

    @patch("app.infrastructure.config.DatabaseConfig")
    @patch("app.repositories.url_repository.get_database")
    async def test_get_by_secret_key__returns_url(
        self, patch_get_database, patch_database_config
    ):
        patch_database_config.return_value.database_type = "deta-base"
        patch_get_database.return_value = DatabaseClientOverride("url")
        repo = UrlRepository()

        actual = await repo.get_by_secret_key("single_record")

        self.assertIsInstance(
            actual,
            Url,
        )

    @patch("app.infrastructure.config.DatabaseConfig")
    @patch("app.repositories.url_repository.get_database")
    async def test_get_by_secret_key__multiple_records__returns_single_url(
        self, patch_get_database, patch_database_config
    ):
        patch_database_config.return_value.database_type = "deta-base"
        patch_get_database.return_value = DatabaseClientOverride("url")
        repo = UrlRepository()

        actual = await repo.get_by_secret_key("multiple_records")

        self.assertIsInstance(
            actual,
            Url,
        )

    @patch("app.infrastructure.config.DatabaseConfig")
    @patch("app.repositories.url_repository.get_database")
    async def test_get_by_secret_key__invalid_key__returns_none(
        self, patch_get_database, patch_database_config
    ):
        patch_database_config.return_value.database_type = "deta-base"
        patch_get_database.return_value = DatabaseClientOverride("url")
        repo = UrlRepository()

        actual = await repo.get_by_secret_key("invalid_key")

        self.assertEqual(
            actual,
            None,
        )

    @patch("app.infrastructure.config.DatabaseConfig")
    @patch("app.repositories.url_repository.get_database")
    async def test_update__no_key__throws(
        self, patch_get_database, patch_database_config
    ):
        patch_database_config.return_value.database_type = "deta-base"
        patch_get_database.return_value = DatabaseClientOverride("url")
        repo = UrlRepository()

        model = Url(
            secret_key="secret_key",
            target_url=HttpUrl("https://example.com"),
            is_active=True,
            clicks=0,
        )

        with self.assertRaises(RecordDoesNotExistExeption):
            await repo.update(model=model)

    @patch("app.infrastructure.config.DatabaseConfig")
    @patch("app.repositories.url_repository.get_database")
    async def test_update_returns_true(self, patch_get_database, patch_database_config):
        patch_database_config.return_value.database_type = "deta-base"
        patch_get_database.return_value = DatabaseClientOverride("url")
        repo = UrlRepository()

        model = Url(
            key="test_update_returns_url_model",
            secret_key="secret_key",
            target_url=HttpUrl("https://example.com"),
            is_active=True,
            clicks=0,
        )

        actual = await repo.update(model=model)

        self.assertTrue(actual)

    @patch("app.infrastructure.config.DatabaseConfig")
    @patch("app.repositories.url_repository.get_database")
    async def test_delete__returns_none(
        self, patch_get_database, patch_database_config
    ):
        patch_database_config.return_value.database_type = "deta-base"
        patch_get_database.return_value = DatabaseClientOverride("url")
        repo = UrlRepository()

        model = Url(
            key="test_delete__returns_none",
            secret_key="secret_key",
            target_url=HttpUrl("https://example.com"),
            is_active=True,
            clicks=0,
        )

        actual = await repo.delete(model=model)

        self.assertIsNone(
            actual,
        )

    @patch("app.infrastructure.config.DatabaseConfig")
    @patch("app.repositories.url_repository.get_database")
    async def test_delete__no_key__throws(
        self, patch_get_database, patch_database_config
    ):
        patch_database_config.return_value.database_type = "deta-base"
        patch_get_database.return_value = DatabaseClientOverride("url")
        repo = UrlRepository()

        model = Url(
            secret_key="secret_key",
            target_url=HttpUrl("https://example.com"),
            is_active=True,
            clicks=0,
        )

        with self.assertRaises(RecordDoesNotExistExeption):
            await repo.delete(model=model)

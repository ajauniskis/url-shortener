from unittest import IsolatedAsyncioTestCase

from app.repositories import UrlRepository


class TestAbstractRepository(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.repo = UrlRepository()

    async def test_url_repository__table_name__returns_url(self):
        self.assertEqual(
            self.repo.table_name,
            "url",
        )

    async def test_url_repository__database__returns_database_client(self):
        actual = type(self.repo.database).__bases__[0].__name__

        self.assertEqual(
            actual,
            "AbstractDatabaseClient",
        )

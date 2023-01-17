from unittest import IsolatedAsyncioTestCase

from app.infrastructure.abstract_database_client import AbstractDatabaseClient


class TestAbstractRepository(IsolatedAsyncioTestCase):
    async def test_create_url__throws(self):
        database = AbstractDatabaseClient("some_table")

        with self.assertRaises(NotImplementedError):
            await database.create({})

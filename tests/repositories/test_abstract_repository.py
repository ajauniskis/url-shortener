from unittest import IsolatedAsyncioTestCase

from app.repositories import AbstractRepository


class TestAbstractRepository(IsolatedAsyncioTestCase):
    async def test_abstract_repository(self):
        AbstractRepository()

    async def test_create_url__throws(self):
        repo = AbstractRepository()

        with self.assertRaises(NotImplementedError):
            await repo.create_url({})

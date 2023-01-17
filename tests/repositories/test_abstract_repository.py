from unittest import IsolatedAsyncioTestCase

from app.repositories import AbstractRepository


class TestAbstractRepository(IsolatedAsyncioTestCase):
    async def test_abstract_repository(self):
        AbstractRepository()

    async def test_create__throws(self):
        repo = AbstractRepository()

        with self.assertRaises(NotImplementedError):
            await repo.create({})

    async def test_get__throws(self):
        repo = AbstractRepository()

        with self.assertRaises(NotImplementedError):
            await repo.get("some_key")

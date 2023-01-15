from unittest import IsolatedAsyncioTestCase

from app.repositories import AbstractRepository


class TestAbstractRepository(IsolatedAsyncioTestCase):
    async def test_abstract_repository(self):
        AbstractRepository()

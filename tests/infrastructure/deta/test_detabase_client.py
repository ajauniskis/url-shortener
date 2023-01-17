from unittest import IsolatedAsyncioTestCase
from app.infrastructure.deta import DetaBaseClient
from tests.conftest import TestDomainModel
from aiodeta import Deta


class TestDetabaseClient(IsolatedAsyncioTestCase):
    async def test_create__adds_record(self):
        model = TestDomainModel(
            value="some_value",
        )
        database = DetaBaseClient("test")

        actual = await database.create(model)

        deta = Deta(
            project_key="a091o6zk_ZXqDeTckdgGRAiABJwoYrWv5r8hFEnX5",
            project_id="a091o6zk",
        )
        base = deta.Base("test")
        expected = await base.get(
            actual.key  # pyright:  ignore [reportGeneralTypeIssues]
        )

        self.assertEqual(
            actual,
            expected,
        )

        await base.delete(expected["key"])

from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from aiodeta import Deta

from app.infrastructure.deta import DetaBaseClient, get_deta_base_config
from tests.conftest import TestDomainModel


class TestDetabaseClient(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        deta_config = get_deta_base_config()
        self.deta_project_key = deta_config.deta_project_key
        self.deta_project_id = deta_config.deta_project_id
        self.test_model = TestDomainModel(
            value="some_value",
        )

        deta = Deta(
            project_key=self.deta_project_key,
            project_id=self.deta_project_id,
        )

        self.base = deta.Base("test")
        self.database = DetaBaseClient("test")

    @patch("app.core.settings.USE_CACHED_SETTINGS", True)
    async def test_create__adds_record(self):

        actual = await self.database.create(self.test_model)

        expected = await self.base.get(
            actual.key  # pyright:  ignore [reportGeneralTypeIssues]
        )

        self.assertEqual(
            actual,
            expected,
        )

        await self.base.delete(expected["key"])

    @patch("app.core.settings.USE_CACHED_SETTINGS", True)
    async def test_get__returns_record(self):

        created_record = await self.base.put(
            [self.test_model.dict()],
        )
        expected = created_record["processed"]["items"][0]

        actual = await self.database.get(
            expected["key"],
        )

        self.assertEqual(
            actual,
            expected,
        )

        await self.base.delete(expected["key"])
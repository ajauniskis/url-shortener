from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from deta import Deta

from app.domain import DetaBaseException
from app.infrastructure.deta import DetaBaseClient, get_deta_base_config
from tests.conftest import TEST_BASE, TestDomainModel


class TestDetabaseClient(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        deta_config = get_deta_base_config()
        self.test_model = TestDomainModel(
            value="some_value",
        )

        deta = Deta(
            project_key=deta_config.deta_project_key,
        )

        self.base = deta.AsyncBase(TEST_BASE)
        self.database = DetaBaseClient(TEST_BASE)

    @patch("app.core.settings.USE_CACHED_SETTINGS", True)
    async def test_create__adds_record(self):
        actual = await self.database.create(self.test_model)

        expected = await self.base.get(
            actual.key  # pyright:  ignore [reportGeneralTypeIssues]
        )

        if not expected:
            raise DetaBaseException

        self.assertEqual(
            actual.model_dump(),
            expected,
        )

        await self.base.delete(expected["key"])

    @patch("app.core.settings.USE_CACHED_SETTINGS", True)
    async def test_get__returns_record(self):
        expected = await self.base.put(
            self.test_model.model_dump(),
        )

        if not expected:
            raise DetaBaseException

        actual = await self.database.get(
            expected["key"],
        )

        self.assertEqual(
            actual,
            expected,
        )

        await self.base.delete(expected["key"])

    @patch("app.core.settings.USE_CACHED_SETTINGS", True)
    async def test_query__returns_record(self):
        expected = await self.base.put(
            self.test_model.model_dump(),
        )

        if not expected:
            raise DetaBaseException

        actual = await self.database.query(
            {"value": self.test_model.value},
        )

        self.assertEqual(
            actual[0],
            expected,
        )

        await self.base.delete(expected["key"])

    @patch("app.core.settings.USE_CACHED_SETTINGS", True)
    async def test_query__returns_multiple_records(self):
        created_record_1 = await self.base.put(
            TestDomainModel(
                value="test_query__returns_multiple_records1",
            ).model_dump(),
        )
        created_record_2 = await self.base.put(
            TestDomainModel(
                value="test_query__returns_multiple_records2",
            ).model_dump(),
        )

        if not created_record_1 or not created_record_2:
            raise DetaBaseException

        expected = [
            created_record_1,
            created_record_2,
        ]

        actual = await self.database.query(
            [
                {"value": "test_query__returns_multiple_records1"},
                {"value": "test_query__returns_multiple_records2"},
            ]
        )

        self.assertEqual(
            sorted(actual, key=lambda x: x["value"]),
            expected,
        )

        await self.base.delete(created_record_1["key"])
        await self.base.delete(created_record_2["key"])

    @patch("app.core.settings.USE_CACHED_SETTINGS", True)
    async def test_query__not_existing_record_returns_empty_list(self):
        actual = await self.database.query(
            {"value": "not existing"},
        )

        self.assertEqual(
            actual,
            [],
        )

    @patch("app.core.settings.USE_CACHED_SETTINGS", True)
    async def test_update__returns_true(self):
        expected = await self.base.put(
            TestDomainModel(
                value="test_update__returns_updated_record",
            ).model_dump(),
        )

        if not expected:
            raise DetaBaseException

        actual = await self.database.update(
            key=expected["key"],
            record={"value": "test_update__returns_updated_record_updated"},
        )

        self.assertTrue(
            actual,
        )

        await self.base.delete(expected["key"])

    @patch("app.core.settings.USE_CACHED_SETTINGS", True)
    async def test_update__invalid_key__throws(self):
        actual = await self.database.update(
            key="q6svtli7erih",
            record={"value": "test_update__invalid_key__throws"},
        )

        self.assertFalse(actual)

    @patch("app.core.settings.USE_CACHED_SETTINGS", True)
    async def test_delete__deletes_record(self):
        await self.base.put(
            TestDomainModel(
                key="test_delete__deletes_record",
                value="test_delete__deletes_record",
            ).model_dump(),
        )

        await self.database.delete(key="test_delete__deletes_record")
        actual = await self.database.get(key="test_delete__deletes_record")
        self.assertIsNone(
            actual,
        )

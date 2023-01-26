import os
from random import randrange
from string import ascii_letters, digits
from unittest import IsolatedAsyncioTestCase

from aiodeta import Deta

from app.domain import SecretKey
from app.infrastructure.deta import DetaBaseClient, get_deta_base_config
from app.repositories import UrlRepository


class TestSecretKey(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        deta_config = get_deta_base_config()
        self.deta_project_key = deta_config.deta_project_key
        self.deta_project_id = deta_config.deta_project_id

        deta = Deta(
            project_key=self.deta_project_key,
            project_id=self.deta_project_id,
        )

        self.base = deta.Base("url")

    def test_generate_secret_key__returns_correct_length(self):
        os.environ["SECRET_KEY_LENGTH"] = "5"

        self.assertEqual(
            len(SecretKey.generate()),
            5,
        )

        os.environ["SECRET_KEY_LENGTH"] = "10"

        self.assertEqual(
            len(SecretKey.generate()),
            10,
        )

    async def test_generate_secret_key__uniqueness(self):
        os.environ["SECRET_KEY_LENGTH"] = "1"
        characters = list(ascii_letters + digits)
        test_character = characters.pop(randrange(len(characters)))

        repository = UrlRepository()
        payloads = [
            {"secret_key": char, "target_url": "https://google.com"}
            for char in characters
        ]

        created_records = []
        for i in range(1, len(characters) + 1, 25):
            records = await self.base.put(payloads[i - 1 : i + 24])
            created_records.extend(records["processed"]["items"])
        actual = await SecretKey.generate_unique(repository)

        self.assertEqual(
            actual,
            test_character,
        )

        for record in created_records:
            await self.base.delete(record["key"])

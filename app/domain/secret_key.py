from __future__ import annotations

from secrets import choice
from string import ascii_letters, digits
from typing import TYPE_CHECKING

from app.core.settings import get_settings

if TYPE_CHECKING:
    from app.repositories import UrlRepository


class SecretKey:
    @classmethod
    def generate(cls) -> str:
        chars = ascii_letters + digits
        secret_key = "".join(
            choice(chars) for _ in range(get_settings().secret_key_length)
        )
        return secret_key

    @classmethod
    async def generate_unique(cls, repository: UrlRepository) -> str:
        key = cls.generate()
        while await repository.get_by_secret_key(key):
            key = cls.generate()
        return key

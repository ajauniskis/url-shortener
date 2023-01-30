from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    pass

    @abstractmethod
    async def create(self, model):
        raise NotImplementedError

    @abstractmethod
    async def get(self, key: str):
        raise NotImplementedError

    @abstractmethod
    async def get_by_secret_key(self, secret_key: str):
        raise NotImplementedError

    @abstractmethod
    async def update(self, model):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, model) -> None:
        raise NotImplementedError

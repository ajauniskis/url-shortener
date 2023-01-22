from abc import ABC


class AbstractRepository(ABC):
    pass

    async def create(self, model):
        raise NotImplementedError

    async def get(self, key: str):
        raise NotImplementedError

from abc import ABC


class AbstractRepository(ABC):
    pass

    async def create_url(self, model):
        raise NotImplementedError

from abc import ABC, abstractmethod


class ConnectionServiceDatabase(ABC):
    def __init__(self):
        pass

    @abstractmethod
    async def get_array_api_keys(self):
        pass

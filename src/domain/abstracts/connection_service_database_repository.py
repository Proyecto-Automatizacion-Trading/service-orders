from abc import ABC, abstractmethod

import aiohttp

from src.domain.models.InputDataTV import InputDataTV


class ConnectionServiceDatabase(ABC):
    def __init__(self):
        pass

    @abstractmethod
    async def get_array_api_keys(self, input_data_tv: InputDataTV):
        pass

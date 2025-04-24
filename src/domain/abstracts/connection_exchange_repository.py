from abc import ABC, abstractmethod

import aiohttp

from ..models.trade import Trade


class ConnectionExchange(ABC):

    @abstractmethod
    async def execute_operation(self, body_order: Trade, headers: dict, url: str, session: aiohttp.ClientSession):
        pass

    @abstractmethod
    async def get_balance(self, headers: dict, url: str, session: aiohttp.ClientSession) -> dict:
        pass

    @abstractmethod
    async def get_price_token(self, url: str, session: aiohttp.ClientSession) -> dict:
        pass

    @abstractmethod
    async def get_open_position_coin(self, url: str, token: dict, session: aiohttp.ClientSession) -> dict:
        pass

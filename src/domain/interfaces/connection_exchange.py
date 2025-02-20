from abc import ABC, abstractmethod

from ..models.trade import Trade
from ..models.response import Response
from ..constants.paths_bitget import PathsBitget

import requests


class ConnectionExchange(ABC):

    @abstractmethod
    async def execute_operation(self, body_order: Trade, headers: dict, url: str):
        pass

    @abstractmethod
    async def get_balance(self, headers: dict, url: str) -> dict:
        pass

    @abstractmethod
    async def get_price_token(self, url: str):
        pass

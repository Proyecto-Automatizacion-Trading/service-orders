from abc import ABC, abstractmethod

from ..models.trade import Trade
from ..models.response import Response
from ..constants.paths import Paths

import requests


class ConnectionExchange(ABC):

    @abstractmethod
    async def execute_operation_bitget(self, body_order: Trade, headers: dict, url: str):
        pass

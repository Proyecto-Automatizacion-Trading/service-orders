from abc import ABC, abstractmethod

import aiohttp

from src.domain.models.InputDataTV import InputDataTV
from src.domain.models.exchangeApiKeyModel import ExchangeApiKeyModel
from src.domain.models.response import Response


class Calculator(ABC):
    @abstractmethod
    async def calculate(self, trade_input: InputDataTV, balance: float,
                        exchange_api_key: ExchangeApiKeyModel, session: aiohttp.ClientSession) -> Response:
        pass

    @abstractmethod
    async def get_price_token(self, symbol: str, session: aiohttp.ClientSession) -> float:
        pass

    @abstractmethod
    async def convert_equivalent_usdt_to_token(self, price_token: float, size_usdt: float) -> float:
        pass

    @abstractmethod
    async def calculate_percentage(self, percentage: float, balance: float) -> float:
        pass

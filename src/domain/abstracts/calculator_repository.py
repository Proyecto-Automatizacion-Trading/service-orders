from abc import ABC, abstractmethod

from src.domain.models.InputDataTV import InputDataTV


class Calculator(ABC):
    @abstractmethod
    async def calculate(self, trade_input: InputDataTV, balance: float):
        pass

    @abstractmethod
    async def get_price_token(self, symbol: str):
        pass

    @abstractmethod
    async def convert_equivalent_usdt_to_token(self, price_token: float, size_usdt: float) -> float:
        pass

    @abstractmethod
    async def calculate_percentage(self, percentage: float, balance: float) -> float:
        pass

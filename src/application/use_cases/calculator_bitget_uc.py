from src.domain.constants.paths_bitget import PathsBitget
from src.domain.interfaces.calculator import Calculator
from src.domain.models.InputDataTV import InputDataTV
from src.infrastructure.adapters.connection_bitget import ConnectionBitget


class CalculatorBitgetUC(Calculator):

    def __init__(self):
        self.connection_bitget = ConnectionBitget()

    async def calculate_percentage(self, percentage: float, balance: float) -> float:
        return balance * (percentage / 100)

    async def convert_equivalent_usdt_to_token(self, price_token: float, size_usdt: float) -> float:
        return size_usdt / price_token

    async def get_price_token(self, symbol: str) -> float:
        url = PathsBitget.PATH_BITGET + PathsBitget.REQUEST_PATH_GET_PRICE_TOKEN + symbol
        response = await self.connection_bitget.get_price_token(url)
        return float(response["data"][0]["price"])

    async def calculate(self, trade_input: InputDataTV, balance: float):
        if trade_input.percentage:
            trade_input.size = await self.calculate_percentage(trade_input.size, balance)

        price_token = await self.get_price_token(trade_input.symbol)
        size_token = await self.convert_equivalent_usdt_to_token(price_token, trade_input.size)
        trade_input.size = size_token

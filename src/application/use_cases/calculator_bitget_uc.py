from src.application.utilities.validations import Validations
from src.domain.constants.paths_bitget import PathsBitget
from src.domain.abstracts.calculator_repository import Calculator
from src.domain.models.InputDataTV import InputDataTV
from src.domain.models.response import Response
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

    async def calculate(self, trade_input: InputDataTV, balance: float) -> Response:
        if trade_input.percentage:
            trade_input.size = await self.calculate_percentage(trade_input.size, balance)

        # Valida si el balance de la operación que se va a abrir si es suficiente
        if await Validations.validate_balance(trade_input.size):
            price_token = await self.get_price_token(trade_input.symbol)
            size_token = await self.convert_equivalent_usdt_to_token(price_token, trade_input.size)
            trade_input.size = size_token
            return Response(statusCode=200, data={"Status": "Ok"}, valid=True)
        else:
            print(f"Error in size: {trade_input.size}")
            return Response(statusCode=400, data={"Error": f"Undersized {trade_input.size}$"}, valid=False)

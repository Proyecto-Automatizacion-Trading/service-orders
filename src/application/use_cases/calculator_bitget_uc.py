import aiohttp

from src.application.utilities.validations import Validations
from src.domain.constants.paths_bitget import PathsBitget
from src.domain.abstracts.calculator_repository import Calculator
from src.domain.models.InputDataTV import InputDataTV
from src.domain.models.exchangeApiKeyModel import ExchangeApiKeyModel
from src.domain.models.response import Response
from src.infrastructure.adapters.connection_bitget import ConnectionBitget


class CalculatorBitgetUC(Calculator):

    def __init__(self):
        self.connection_bitget = ConnectionBitget()

    async def calculate_percentage(self, percentage: float, balance: float) -> float:
        return balance * (percentage / 100)

    async def convert_equivalent_usdt_to_token(self, price_token: float, size_usdt: float) -> float:
        return size_usdt / price_token

    async def get_price_token(self, symbol: str, session: aiohttp.ClientSession) -> float:
        url = PathsBitget.PATH_BITGET + PathsBitget.REQUEST_PATH_GET_PRICE_TOKEN + symbol
        response = await self.connection_bitget.get_price_token(url, session)
        return float(response["data"][0]["price"])

    async def calculate(self, trade_input: InputDataTV, balance: float,
                        exchange_api_key: ExchangeApiKeyModel, session: aiohttp.ClientSession) -> Response:
        if exchange_api_key.get("is_percentage"):
            self.update_size(exchange_api_key, await self.calculate_percentage(exchange_api_key.get("size"), balance))

        # Valida si el balance de la operación que se va a abrir si es suficiente
        if await Validations.validate_balance(exchange_api_key.get("size")):
            price_token = await self.get_price_token(trade_input.symbol, session)
            self.update_size(exchange_api_key,
                             await self.convert_equivalent_usdt_to_token(price_token, exchange_api_key.get("size")))
            return Response(statusCode=200, data={"Status": "Ok"}, valid=True)
        else:
            print(f"Error in size: {exchange_api_key['size']}")
            raise Exception(Response(statusCode=400, data={"Error": f"Undersized {exchange_api_key['size']}$"}, valid=False))

    @staticmethod
    def update_size(exchange_api_key: ExchangeApiKeyModel, size: float) -> None:
        exchange_api_key.update({"size": size})

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
        """
        Obtiene el precio actual del token con el símbolo dado.

        Parámetros:
        symbol (str): El símbolo del token.
        session (aiohttp.ClientSession): La sesión aiohttp a utilizar.

        Retorna:
        float: El precio actual del token.
        """
        pass

    @abstractmethod
    async def convertir_equivalente_usdt_a_token(self, precio_token: float, monto_usdt: float) -> float:
        """
        Convierte el monto equivalente en USDT al monto correspondiente en tokens según el precio del token proporcionado.

        Parámetros:
        precio_token (float): El precio de un solo token.
        monto_usdt (float): El monto en USDT a ser convertido.

        Retorna:
        float: El monto equivalente en tokens.
        """
        pass

    @abstractmethod
    async def calculate_percentage(self, percentage: float, balance: float) -> float:
        """
        Calcula el monto que se va a operar con base en el porcentaje proporcionado.

        Parámetros:
        percentage (float): El porcentaje a calcular.
        balance (float): El saldo total disponible.

        Retorna:
        float: El monto que se va a operar.
        """
        pass

from abc import ABC, abstractmethod
from ..models.response import Response
from ..models.InputDataTV import InputDataTV
from ..interfaces.exchange_auth import ExchangeAuth


class PositionRepository(ABC):
    # Método encargado de gestionar la apertura de una posición
    @abstractmethod
    async def open_position(self, trade_input: InputDataTV, exchange_auth: ExchangeAuth) -> Response:
        pass

    # Método encargado de gestionar el cierre de una posición
    @abstractmethod
    async def close_position(self, trade_input: InputDataTV, exchange_auth: ExchangeAuth) -> Response:
        pass

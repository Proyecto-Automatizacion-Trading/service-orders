from abc import ABC, abstractmethod

from ..models.exchangeApiKeyModel import ExchangeApiKeyModel
from ..models.response import Response
from ..models.InputDataTV import InputDataTV
from ..abstracts.exchange_auth_repository import ExchangeAuth


class PositionRepository(ABC):
    # Método encargado de gestionar la apertura de una posición
    @abstractmethod
    async def open_position(self, exchange_api_key: ExchangeApiKeyModel) -> Response:
        pass

    # Método encargado de gestionar el cierre de una posición
    @abstractmethod
    async def close_position(self, total: float, hold_side: str, exchange_api_key: ExchangeApiKeyModel) -> Response:
        pass

    # Método principal sobre el cual se ejecutará la operación ya sea de apertura o cierre
    async def execute_operation(self, trade_input: InputDataTV, exchange_auth: ExchangeAuth) -> Response:
        pass

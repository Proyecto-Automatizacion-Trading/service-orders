from abc import ABC, abstractmethod
from ..models.trade import Trade
from ..models.response import Response


class PositionRepository(ABC):
    # Método encargado de gestionar la apertura de una posición
    @abstractmethod
    async def open_position(self, trade: Trade) -> Response:
        pass

    # Método encargado de gestionar el cierre de una posición
    @abstractmethod
    async def close_position(self, trade: Trade) -> Response:
        pass

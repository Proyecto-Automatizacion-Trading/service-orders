from abc import ABC, abstractmethod
from ..models.response import Response
from ..models.InputDataTV import InputDataTV


class PositionRepository(ABC):
    # Método encargado de gestionar la apertura de una posición
    @abstractmethod
    async def open_position(self, trade_input: InputDataTV) -> Response:
        pass

    # Método encargado de gestionar el cierre de una posición
    @abstractmethod
    async def close_position(self, trade_input: InputDataTV) -> Response:
        pass

from pydantic import BaseModel
from ..enums.order_type import OrderType
from ..enums.position_side import PositionSide


class InputDataTV(BaseModel):
    symbol: str
    size: str
    side: str  # Cambiado de "buy" a "sell"
    tradeSide: str  # Cambiado de "close" a "open"
    leverage: str  # apalancamiento

from pydantic import BaseModel
from ..enums.order_type import OrderType
from ..enums.position_side import PositionSide


class InputDataTV(BaseModel):
    symbol: str
    size: float
    side: PositionSide  # Cambiado de "buy" a "sell"
    tradeSide: OrderType  # Cambiado de "close" a "open"
    leverage: str  # apalancamiento

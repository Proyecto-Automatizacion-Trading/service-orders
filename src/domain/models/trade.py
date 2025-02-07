from datetime import datetime
from ..enums.order_type import OrderType
from ..enums.position_side import PositionSide
from pydantic import BaseModel

from ...application.utilities.timeUtility import TimeUtility


class Trade(BaseModel):
    symbol: str
    productType: str
    marginMode: str
    marginCoin: str
    size: str
    side: str  # Cambiado de "buy" a "sell"
    tradeSide: str  # Cambiado de "close" a "open"
    orderType: str
    timeInForceValue: str
    clientOid: str = TimeUtility.get_timestamp_datetime()
    leverage: str


from dataclasses import dataclass
from datetime import datetime
from ..enums.order_type import OrderType
from ..enums.position_side import PositionSide
from dataclasses import asdict
from pydantic import BaseModel


@dataclass
class Trade(BaseModel):
    symbol: str
    productType: str
    marginMode: str
    marginCoin: str
    size: float
    side: PositionSide
    tradeSide: OrderType
    orderType: str
    timeInForceValue: str
    clientOid: str
    leverage: str
    createdTime: datetime

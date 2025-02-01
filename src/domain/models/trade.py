from dataclasses import dataclass
from datetime import datetime
from ..enums.order_type import OrderType
from ..enums.position_side import PositionSide
from dataclasses import asdict


@dataclass
class Trade:
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

    def dict(self):
        data = asdict(self)  # Convertir el objeto en un diccionario
        data["createdTime"] = self.createdTime.isoformat()  # Convertir el objeto datetime en una cadena de texto
        # Convertir enums a sus valores en string
        data["tradeSide"] = self.tradeSide.value
        data["side"] = self.side.value
        return data

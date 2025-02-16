from pydantic import BaseModel


class Trade(BaseModel):
    symbol: str
    productType: str
    marginMode: str
    marginCoin: str
    size: float
    side: str  # Cambiado de "buy" a "sell"
    tradeSide: str  # Cambiado de "close" a "open"
    orderType: str
    timeInForceValue: str
    clientOid: str

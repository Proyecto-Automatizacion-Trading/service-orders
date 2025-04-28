from pydantic import BaseModel


class InputDataTV(BaseModel):
    symbol: str  # Símbolo de la moneda
    side: str  # Cambiado de "buy" a "sell"
    strategy: str  # Estrategia de trading
    temporality: str  # Temporalidad de la orden

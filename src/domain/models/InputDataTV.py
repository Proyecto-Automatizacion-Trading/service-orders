from pydantic import BaseModel


class InputDataTV(BaseModel):
    symbol: str  # Símbolo de la moneda
    side: str  # Cambiado de "buy" a "sell"
    size: float  # Porcentaje para abrir la orden si es porcentaje, el tamaño de la orden si es tamaño
    currentPrice: float  # Precio actual de la moneda
    strategy: str  # Estrategia de trading
    temporality: str  # Temporalidad de la orden

from pydantic import BaseModel


class InputDataTV(BaseModel):
    symbol: str  # Símbolo de la moneda
    side: str  # Cambiado de "buy" a "sell"
    tradeSide: str  # Cambiado de "close" a "open"
    percentage: bool  # Porcentaje para abrir la orden
    size: str  # Porcentaje para abrir la orden si es porcentaje, el tamaño de la orden si es tamaño

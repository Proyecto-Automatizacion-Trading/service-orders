from pydantic import BaseModel


# class InputDataTV(BaseModel):
#    symbol: str  # Símbolo de la moneda
#    side: str  # Cambiado de "buy" a "sell"
#    size: float  # Porcentaje para abrir la orden si es porcentaje, el tamaño de la orden si es tamaño
#    currentPrice: float  # Precio actual de la moneda
#    strategy: str  # Estrategia de trading
#    temporality: str  # Temporalidad de la orden

class InputDataTV(BaseModel):
    symbol: str  # Símbolo de la moneda
    side: str  # Cambiado de "buy" a "sell"
    # tradeSide: str  # Cambiado de "close" a "open"
    percentage: bool  # Porcentaje para abrir la orden
    size: float  # Porcentaje para abrir la orden si es porcentaje, el tamaño de la orden si es tamaño
    exchange: str  # Define el exchange en donde se va a ejecutar la operación

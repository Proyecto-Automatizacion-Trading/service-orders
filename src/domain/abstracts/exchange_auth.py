"""
Clase abstracta encargada de generar las firmas necesarias para
configurar las credenciales, firmas y cabeceras para poder
ejecutar las órdenes en cualquier exchange.
"""

from abc import ABC, abstractmethod
from typing import Dict


class ExchangeAuth(ABC):

    # Retorna las credenciales necesarias para el exchange
    @abstractmethod
    def get_credentials(self) -> Dict[str, str]:
        pass

    # Retorna la firma necesaria para el exchange
    @abstractmethod
    def generate_signature(self, timestamp, method, request_path, body, secret) -> str:
        pass

    # Retorna los headers necesarios para el exchange
    @abstractmethod
    def generate_headers(self, timestamp, method, request_path, body, secret) -> Dict[str, str]:
        pass

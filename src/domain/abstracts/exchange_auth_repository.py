from abc import ABC, abstractmethod
from typing import Dict

from src.domain.models.exchangeApiKeyModel import ExchangeApiKeyModel


class ExchangeAuth(ABC):
    """
    Clase abstracta encargada de generar las firmas necesarias para
    configurar las credenciales, firmas y cabeceras para poder
    ejecutar las órdenes en cualquier exchange.
    """

    @abstractmethod
    def generate_signature(self, timestamp: str, method: str, request_path: str, body: str, secret: str) -> str:
        """
        Genera la firma necesaria para el exchange.

        Args:
            timestamp (str): Timestamp en formato ISO 8601.
            method (str): Método de petición.
            request_path (str): Ruta de la petición.
            body (str): Cuerpo de la petición.
            secret (str): Clave secreta del exchange.

        Returns:
            str: Firma generada.
        """
        pass

    @abstractmethod
    def generate_headers(self, timestamp: str, method: str, request_path: str, body: str,
                         secret: str) -> Dict[str, str]:
        """
        Genera los headers necesarios para el exchange.

        Args:
            timestamp (str): Timestamp en formato ISO 8601.
            method (str): Método de petición.
            request_path (str): Ruta de la petición.
            body (str): Cuerpo de la petición.
            secret (str): Clave secreta del exchange.

        Returns:
            Dict[str, str]: Diccionario con los headers necesarios
                para el exchange.
        """
        pass

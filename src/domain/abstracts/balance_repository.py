from abc import ABC, abstractmethod

import aiohttp

from src.domain.abstracts.exchange_auth_repository import ExchangeAuth
from src.domain.models.exchangeApiKeyModel import ExchangeApiKeyModel


class Balance(ABC):

    @abstractmethod
    def get_balance(self, exchange_auth: ExchangeAuth, exchange_api_key: ExchangeApiKeyModel,
                    session: aiohttp.ClientSession) -> float:
        """
        Obtiene el saldo de la llave de la API de intercambio dada

        Args:
            exchange_auth (ExchangeAuth): El objeto de autenticación para interactuar con la API del intercambio
            exchange_api_key (ExchangeApiKeyModel): La llave de la API del intercambio cuyo saldo se va a obtener
            session (aiohttp.ClientSession): La sesión HTTP usada para interactuar con la API del intercambio

        Returns:
            float: El saldo de la llave de la API del intercambio dada
        """
        pass

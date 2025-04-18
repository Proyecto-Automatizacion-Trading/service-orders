from abc import ABC, abstractmethod

from src.domain.abstracts.exchange_auth_repository import ExchangeAuth
from src.domain.models.exchangeApiKeyModel import ExchangeApiKeyModel


class Balance(ABC):
    @abstractmethod
    def get_balance(self, exchange_auth: ExchangeAuth, exchange_api_key: ExchangeApiKeyModel) -> float:
        pass

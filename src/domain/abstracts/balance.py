from abc import ABC, abstractmethod

from src.domain.abstracts.exchange_auth import ExchangeAuth


class Balance(ABC):
    @abstractmethod
    def get_balance(self, exchange_auth: ExchangeAuth) -> float:
        pass

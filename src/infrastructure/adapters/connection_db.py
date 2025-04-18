from typing import List

from src.domain.abstracts.connection_service_database_repository import ConnectionServiceDatabase
from src.domain.models.exchangeApiKeyModel import ExchangeApiKeyModel
from my_config import SECRETS


class ConnectionDB(ConnectionServiceDatabase):

    async def get_array_api_keys(self) -> List[ExchangeApiKeyModel]:
        return SECRETS

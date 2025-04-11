from typing import Dict

from src.domain.interfaces.connection_service_database import ConnectionServiceDatabase


class ConnectionDB(ConnectionServiceDatabase):

    def get_array_api_keys(self) -> Dict[str, str]:
        pass

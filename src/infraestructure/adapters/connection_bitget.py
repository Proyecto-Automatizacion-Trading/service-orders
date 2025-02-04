import json

import requests

from src.domain.interfaces.connection_exchange import ConnectionExchange
from src.domain.models.trade import Trade


class ConnectionBitget(ConnectionExchange):
    async def execute_operation(self, body_order: json, headers: dict, url: str):
        try:
            response = requests.post(url, headers=headers, data=body_order)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
        except Exception as e:
            print(f"Error: {str(e)}")

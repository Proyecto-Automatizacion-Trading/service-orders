import json

import requests

from src.domain.interfaces.connection_exchange import ConnectionExchange
from src.domain.models.response import Response


class ConnectionBitget(ConnectionExchange):

    async def get_price_token(self, url: str) -> dict:
        try:
            response = requests.get(url)
            print(f"Status Code: {response.status_code}")
            print(f"Response Bitget: {response.json()}")
            return response.json()
        except Exception as e:
            print(f"Error in get_price_token: {str(e)}")
            raise e

    async def execute_operation(self, body_order: json, headers: dict, url: str) -> Response:
        try:
            response = requests.post(url, headers=headers, data=body_order)
            print(f"Status Code: {response.status_code}")
            print(f"Response Bitget: {response.json()}")
            if response.status_code == 200:
                return Response(statusCode=response.status_code, data=response.json(), valid=True)
            return Response(statusCode=response.status_code, data=response.json(), valid=False)
        except Exception as e:
            print(f"Error in execute_operation: {str(e)}")
            raise e

    async def get_balance(self, headers: dict, url: str) -> dict:
        try:
            response = requests.get(url, headers=headers)
            print(f"Status Code: {response.status_code}")
            print(f"Balance Bitget: {response.json()}")
            return response.json()
        except Exception as e:
            print(f"Error in get_balance_bitget: {str(e)}")
            raise e

import json

import requests

from src.domain.abstracts.connection_exchange_repository import ConnectionExchange
from src.domain.models.response import Response


class ConnectionBitget(ConnectionExchange):

    async def get_open_position_coin(self, url: str, headers: dict) -> dict:
        try:
            print("Obteniendo Posiciones Bitget..." + "--" * 10)
            response = requests.get(url, headers=headers)
            print(f"Status Code: {response.status_code}")
            print(f"Response Position Bitget: {response.json()}")
            return response.json()
        except Exception as e:
            print(f"Error in get_open_position_coin: {str(e)}")
            raise e

    async def get_price_token(self, url: str) -> dict:
        try:
            print("Obteniendo Precio Token Bitget..." + "--" * 10)
            response = requests.get(url)
            print(f"Status Code: {response.status_code}")
            print(f"Response Price Token Bitget: {response.json()}")
            return response.json()
        except Exception as e:
            print(f"Error in get_price_token: {str(e)}")
            raise e

    async def execute_operation(self, body_order: json, headers: dict, url: str) -> Response:
        try:
            print("Enviando Orden Bitget..." + "--" * 10)
            response = requests.post(url, headers=headers, data=body_order)
            print(f"Status Code: {response.status_code}")
            print(f"Response Execute Bitget: {response.json()}")
            if response.status_code == 200:
                return Response(statusCode=response.status_code, data=response.json(), valid=True)
            return Response(statusCode=response.status_code, data=response.json(), valid=False)
        except Exception as e:
            print(f"Error in execute_operation: {str(e)}")
            raise e

    async def get_balance(self, headers: dict, url: str) -> dict:
        try:
            print("Obteniendo Balance Bitget..." + "--" * 10)
            response = requests.get(url, headers=headers)
            print(f"Status Code: {response.status_code}")
            print(f"Response Balance Bitget: {response.json()}")
            return response.json()
        except Exception as e:
            print(f"Error in get_balance_bitget: {str(e)}")
            raise e

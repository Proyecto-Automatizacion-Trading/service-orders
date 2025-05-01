import json

import aiohttp

from src.domain.abstracts.connection_exchange_repository import ConnectionExchange
from src.domain.models.response import Response


class ConnectionBitget(ConnectionExchange):

    async def get_open_position_coin(self, url: str, headers: dict, session: aiohttp.ClientSession) -> dict:
        try:
            async with session.get(url, headers=headers) as response:
                data = await response.json()
            print(f"Status Code Position: {response.status}")
            print(f"Response Position Bitget: {data}")
            return data
        except Exception as e:
            print(f"Error in get_open_position_coin: {str(e)}")
            raise e

    async def get_price_token(self, url: str, session: aiohttp.ClientSession) -> dict:
        try:
            async with session.get(url) as response:
                data = await response.json()
            print(f"Status Code Price Token: {response.status}")
            print(f"Response Price Token Bitget: {data}")
            return data
        except Exception as e:
            print(f"Error in get_price_token: {str(e)}")
            raise e

    async def execute_operation(self, body_order: json, headers: dict, url: str,
                                session: aiohttp.ClientSession) -> Response:
        try:
            async with session.post(url, headers=headers, data=body_order) as response:
                data = await response.json()
            print(f"Status Code Execute Order: {response.status}")
            print(f"Response Execute Bitget: {data}")
            if response.status == 200:
                return Response(statusCode=response.status, data=data, valid=True)
            return Response(statusCode=response.status, data=data, valid=False)
        except Exception as e:
            print(f"Error in execute_operation: {str(e)}")
            raise e

    async def get_balance(self, headers: dict, url: str, session: aiohttp.ClientSession) -> dict:
        try:
            async with session.get(url, headers=headers) as response:
                data = await response.json()
            print(f"Status Code Balance: {response.status}")
            print(f"Response Balance Bitget: {data}")
            return data
        except Exception as e:
            print(f"Error in get_balance_bitget: {str(e)}")
            raise e

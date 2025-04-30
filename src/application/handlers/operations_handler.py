import asyncio
import aiohttp
from typing import List

from fastapi import HTTPException

from src.application.use_cases.position_bitget_uc import PositionBitgetUC
from src.domain.models import InputDataTV
from src.domain.models.exchangeApiKeyModel import ExchangeApiKeyModel
from src.domain.models.response import Response
from src.infrastructure.adapters.connection_db import ConnectionDB


def format_response(response: Response):
    if isinstance(response, Exception):
        return {
            "statusCode": 500,
            "data": str(response),
            "valid": False
        }
    else:
        return {
            "statusCode": response.statusCode,
            "data": response.data,
            "valid": response.valid
        }


class OperationsHandler:

    def __init__(self):
        self.exchanges = {
            "Bitget": PositionBitgetUC(),
        }
        self.connection_service_database = ConnectionDB()

    async def positions_handler(self, alert: InputDataTV) -> Response:
        try:
            arrays_api_keys = await self.get_array_api_keys(alert)
            for credentials_exchange in arrays_api_keys["data"]:
                async with aiohttp.ClientSession() as session:
                    tasks = [
                        self.send_orders(alert, exchange_api_key, session, credentials_exchange["Exchange"])
                        for exchange_api_key in credentials_exchange["APIKeys"]
                    ]
                    responses = await asyncio.gather(*tasks, return_exceptions=True)
                formatted_responses = {}
                for i, resp in enumerate(responses):
                    formatted_responses[f"order_{i}"] = format_response(resp)
                return Response(statusCode=200, data=formatted_responses, valid=all(r.valid for r in responses))
        except Exception as e:
            print("Error in OperationsHandler: " + str(e))
            raise HTTPException(status_code=500, detail=f"Error in operations_handler: {str(e)}")

    async def send_orders(self, data_alert: InputDataTV, exchange_api_key: ExchangeApiKeyModel,
                          session: aiohttp.ClientSession, exchange: str) -> Response:
        exchange_api_key["size"] = 50
        exchange_api_key["is_percentage"] = True
        return await self.exchanges[exchange].execute_order(data_alert, exchange_api_key, session)

    async def get_array_api_keys(self, input_data_tv: InputDataTV) -> List[ExchangeApiKeyModel]:
        try:
            return await self.connection_service_database.get_array_api_keys(input_data_tv)
        except Exception as e:
            print("Error in get_array_api_keys: " + str(e))
            raise HTTPException(status_code=500, detail=f"Error in get_array_api_keys: {str(e)}")

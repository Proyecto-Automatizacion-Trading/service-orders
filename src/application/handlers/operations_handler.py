import asyncio
import aiohttp
from typing import List

from fastapi import HTTPException

from src.application.use_cases.position_bitget_uc import PositionBitgetUC
from src.domain.models import InputDataTV
from src.domain.models.exchangeApiKeyModel import ExchangeApiKeyModel
from src.domain.models.response import Response
from src.infrastructure.adapters.connection_db import ConnectionDB


class OperationsHandler:

    def __init__(self):
        self.exchanges = {
            "bitget": PositionBitgetUC(),
        }
        self.connection_service_database = ConnectionDB()

    async def positions_handler(self, alert: InputDataTV) -> Response:
        try:
            arrays_api_keys = await self.get_array_api_keys()
            async with aiohttp.ClientSession() as session:
                tasks = [
                    self.send_orders(alert, exchange_api_key)
                    for exchange_api_key in arrays_api_keys
                ]
                response = await asyncio.gather(*tasks)
            return Response(statusCode=200, data=response, valid=True)
        except Exception as e:
            print("Error in Controller Exchanges UC: " + str(e))
            raise HTTPException(status_code=500, detail=f"Error in position_handler: {str(e)}")

    async def send_orders(self, data_alert: InputDataTV, exchange_api_key: ExchangeApiKeyModel) -> None:
        return await self.exchanges[exchange_api_key.exchange].execute_order(data_alert, exchange_api_key)

    async def controller_alert(self, alert: InputDataTV) -> Response:
        pass

    async def get_array_api_keys(self) -> List[ExchangeApiKeyModel]:
        return await self.connection_service_database.get_array_api_keys()

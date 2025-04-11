from fastapi import HTTPException

from src.application.use_cases.position_bitget_uc import PositionBitgetUC
from src.domain.models import InputDataTV
from src.domain.models.response import Response
from src.infrastructure.adapters.bitget_auth import BitgetAuth
from src.infrastructure.adapters.connection_service_database import ConnectionServiceDatabase


class ControllerExchangesUC:

    def __init__(self):
        self.exchanges = {
            "bitget": PositionBitgetUC(),
        }
        self.connection_service_database = ConnectionServiceDatabase()

    async def controller_exchanges(self, alert: InputDataTV) -> Response:
        try:
            return await self.exchanges[alert.exchange].execute_order(alert, BitgetAuth())
        except Exception as e:
            print("Error in Controller Exchanges UC: " + str(e))
            raise HTTPException(status_code=500, detail=f"Error in controller_exchanges: {str(e)}")

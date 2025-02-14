from typing import Optional

from fastapi import HTTPException

from src.domain.constants.request_methods import RequestMethods
from src.domain.constants.paths import Paths
from ...domain.interfaces.exchange_auth import ExchangeAuth
from ...domain.interfaces.position_repository import PositionRepository
from ...domain.models.trade import Trade
from ...domain.models.response import Response
from ...domain.models.InputDataTV import InputDataTV
from ...infrastructure.adapters.bitget_auth import BitgetAuth
from ...infrastructure.adapters.connection_bitget import ConnectionBitget
from ...application.utilities.timeUtility import TimeUtility
from ...application.utilities.serializable_utility import SerializableUtility
from ...application.utilities.validations import Validations
from ...domain.enums.order_type import OrderType
from ...domain.enums.position_side import PositionSide


class PositionBitgetUC(PositionRepository):

    def __init__(self):
        self.connection_bitget = ConnectionBitget()
        self.bitget_auth: Optional[BitgetAuth] = None
        self.trade_input: Optional[InputDataTV] = None

    async def execute_operation(self, trade_input: InputDataTV, exchange_auth: ExchangeAuth) -> Response:
        self.trade_input = trade_input
        self.bitget_auth = exchange_auth
        if trade_input.tradeSide == OrderType.OPEN.value:
            return await self.open_position()
        elif trade_input.tradeSide == OrderType.CLOSE.value:
            return await self.close_position()
        else:
            print("Invalid tradeSide: " + trade_input.tradeSide)
            raise HTTPException(status_code=400, detail=f"Invalid tradeSide: {trade_input.tradeSide}")

    async def open_position(self) -> Response:
        if Validations.validate_enum(self.trade_input.side, PositionSide) and Validations.validate_enum(
                self.trade_input.tradeSide, OrderType):
            trade = await self.create_json_trading(self.trade_input)
            body_trade = SerializableUtility.serialize_json(trade.model_dump())
            url = Paths.PATH_BITGET + Paths.REQUEST_PATH_FUTURES
            headers = self.bitget_auth.generate_headers(TimeUtility.get_timestamp(), RequestMethods.POST,
                                                        Paths.REQUEST_PATH_FUTURES, body_trade,
                                                        self.bitget_auth.get_credentials().get("API_SECRET"))
            return await self.connection_bitget.execute_operation_bitget(body_trade, headers, url)
        else:
            print(f"Error in side or tradeSide: {self.trade_input.side} - {self.trade_input.tradeSide}")
            return Response(statusCode=400, data="Error in side or tradeSide", valid=False)

    async def close_position(self) -> Response:
        if Validations.validate_enum(self.trade_input.side, PositionSide) and Validations.validate_enum(
                self.trade_input.tradeSide, OrderType):
            trade = await self.create_json_trading(self.trade_input)
            body_trade = SerializableUtility.serialize_json(trade.model_dump())
            url = Paths.PATH_BITGET + Paths.REQUEST_PATH_FUTURES
            headers = self.bitget_auth.generate_headers(TimeUtility.get_timestamp(), RequestMethods.POST,
                                                        Paths.REQUEST_PATH_FUTURES, body_trade,
                                                        self.bitget_auth.get_credentials().get("API_SECRET"))
            return await self.connection_bitget.execute_operation_bitget(body_trade, headers, url)
        else:
            print(f"Error in side or tradeSide: {self.trade_input.side} - {self.trade_input.tradeSide}")
            return Response(statusCode=400, data="Error in side or tradeSide", valid=False)

    @staticmethod
    async def create_json_trading(trade_input: InputDataTV) -> Trade:
        return Trade(
            symbol=trade_input.symbol,
            productType="USDT-FUTURES",
            marginMode="isolated",
            marginCoin="USDT",
            size=trade_input.size,
            side=trade_input.side,
            tradeSide=trade_input.tradeSide,
            orderType="market",
            timeInForceValue="normal",
            clientOid=TimeUtility.get_timestamp_datetime(),
        )

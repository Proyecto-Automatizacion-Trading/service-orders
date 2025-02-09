import json

from src.domain.constants.request_methods import RequestMethods
from src.domain.constants.paths import Paths
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
    connection_bitget = ConnectionBitget()

    async def open_position(self, trade_input: InputDataTV, bitget_auth: BitgetAuth) -> Response:
        if Validations.validate_enum(trade_input.side, PositionSide) and Validations.validate_enum(
                trade_input.tradeSide, OrderType):
            trade = await self.create_json_trading(trade_input)
            body_trade = SerializableUtility.serialize_json(trade.model_dump())
            url = Paths.PATH_BITGET + Paths.REQUEST_PATH_FUTURES
            headers = bitget_auth.generate_headers(TimeUtility.get_timestamp(), RequestMethods.POST,
                                                   Paths.REQUEST_PATH_FUTURES, body_trade,
                                                   bitget_auth.get_credentials().get("API_SECRET"))
            return await self.connection_bitget.execute_operation(body_trade, headers, url)
        else:
            print(f"Error in side or tradeSide: {trade_input.side} - {trade_input.tradeSide}")
            return Response(statusCode=400, data="Error in side or tradeSide", valid=False)

    async def close_position(self, trade_input: InputDataTV, bitget_auth: BitgetAuth) -> Response:
        if Validations.validate_enum(trade_input.side, PositionSide) and Validations.validate_enum(
                trade_input.tradeSide, OrderType):
            trade = await self.create_json_trading(trade_input)
            body_trade = SerializableUtility.serialize_json(trade.model_dump())
            url = Paths.PATH_BITGET + Paths.REQUEST_PATH_FUTURES
            headers = bitget_auth.generate_headers(TimeUtility.get_timestamp(), RequestMethods.POST,
                                                   Paths.REQUEST_PATH_FUTURES, body_trade,
                                                   bitget_auth.get_credentials().get("API_SECRET"))
            return await self.connection_bitget.execute_operation(body_trade, headers, url)
        else:
            print(f"Error in side or tradeSide: {trade_input.side} - {trade_input.tradeSide}")
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
        )

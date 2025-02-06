import json

from src.domain.constants.request_methods import RequestMethods
from src.domain.constants.paths import Paths
from ...domain.interfaces.position_repository import PositionRepository
from ...domain.models.trade import Trade
from ...domain.models.response import Response
from ...domain.models.InputDataTV import InputDataTV
from ...infrastructure.adapters.bitget_auth import BitgetAuth
from ...infrastructure.adapters.connection_bitget import ConnectionBitget
from ...application.utilities.timeUtiliti import TimeUtiliti


class PositionBitgetUC(PositionRepository):
    connection_bitget = ConnectionBitget()

    async def open_position(self, trade_input: InputDataTV, bitget_auth: BitgetAuth) -> Response:
        trade = await self.create_json_trading(trade_input)
        body_trade = json.dumps(trade.model_dump(), separators=(",", ":"))
        url = Paths.PATH_BITGET + Paths.REQUEST_PATH_FUTURES
        headers = bitget_auth.generate_headers(RequestMethods.POST, url, body_trade,
                                               bitget_auth.get_credentials().get("API_SECRET"))
        return await self.connection_bitget.execute_operation(body_trade, headers, url)

    async def close_position(self, trade_input: InputDataTV, bitget_auth: BitgetAuth) -> Response:
        trade = await self.create_json_trading(trade_input)
        body_trade = json.dumps(trade.model_dump(), separators=(",", ":"))
        timestamp = TimeUtiliti.get_timestamp()
        url = Paths.PATH_BITGET + Paths.REQUEST_PATH_FUTURES
        headers = bitget_auth.generate_headers(timestamp, RequestMethods.POST, url, body_trade,
                                               bitget_auth.get_credentials().get("API_SECRET"))
        return await self.connection_bitget.execute_operation(body_trade, headers, url)

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
            leverage=trade_input.leverage,
        )

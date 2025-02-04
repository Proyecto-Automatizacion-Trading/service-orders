from ...domain.interfaces.position_repository import PositionRepository
from ...domain.models.trade import Trade
from ...domain.models.response import Response
from ...domain.models.InputDataTV import InputDataTV
from datetime import datetime
import json
import time

from ...infraestructure.adapters.bitget_auth import BitgetAuth
from src.domain.constants.request_methods import RequestMethods
from src.domain.constants.paths import Paths
from ...infraestructure.adapters.connection_bitget import ConnectionBitget


class PositionBitgetUC(PositionRepository):
    connection_bitget = ConnectionBitget()

    async def open_position(self, trade_input: InputDataTV, bitget_auth: BitgetAuth):
        trade = await self.create_json_trading(trade_input)
        body_trade = json.dumps(trade, separators=(",", ":"))
        timestamp = await self.get_timestamp()
        url = Paths.PATH_BITGET + Paths.REQUEST_PATH_FUTURES
        headers = bitget_auth.generate_headers(timestamp, RequestMethods.POST, url, body_trade,
                                               bitget_auth.get_credentials().get("API_SECRET"))
        await self.connection_bitget.execute_operation(body_trade, headers, url)

    async def close_position(self, trade_input: InputDataTV) -> Response:
        pass

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
            clientOid=str(int(datetime.now().timestamp() * 1000)),
            leverage=trade_input.leverage,
            createdTime=datetime.now()
        )

    @staticmethod
    async def get_timestamp() -> str:
        return str(int(time.time() * 1000))

from ...domain.interfaces.position_repository import PositionRepository
from ...domain.models.trade import Trade
from ...domain.models.response import Response
from ...domain.models.InputDataTV import InputDataTV
from datetime import datetime


class PositionBitgetUC(PositionRepository):
    async def open_position(self, trade_input: InputDataTV) -> Response:
        trade = await self.create_json_trading(trade_input)

        return None

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

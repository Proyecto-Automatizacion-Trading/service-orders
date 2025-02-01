from ...domain.interfaces.position_repository import PositionRepository
from ...domain.models.trade import Trade
from ...domain.models.response import Response


class PositionUC(PositionRepository):
    async def open_position(self, trade: Trade) -> Response:
        pass

    async def close_position(self, trade: Trade) -> Response:
        pass


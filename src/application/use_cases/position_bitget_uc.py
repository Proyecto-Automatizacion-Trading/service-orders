from typing import Optional

from fastapi import HTTPException

from src.domain.constants.request_methods import RequestMethods
from src.domain.constants.paths_bitget import PathsBitget
from .balance_bitget_uc import BalanceBitgetUC
from .calculator_bitget_uc import CalculatorBitgetUC
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
        self.balance_uc: BalanceBitgetUC = BalanceBitgetUC()
        self.calculator_bitget: CalculatorBitgetUC = CalculatorBitgetUC()

    async def execute_order(self, trade_input: InputDataTV, bitget_auth: BitgetAuth) -> Response:
        try:
            self.trade_input = trade_input
            self.bitget_auth = bitget_auth
            balance = await self.balance_uc.get_balance(self.bitget_auth)
            if self.validate_balance(float(balance)):
                if trade_input.tradeSide == OrderType.OPEN.value:
                    return await self.open_position()
                elif trade_input.tradeSide == OrderType.CLOSE.value:
                    return await self.close_position()
                else:
                    print("Invalid tradeSide: " + trade_input.tradeSide)
                    raise HTTPException(status_code=400, detail=f"Invalid tradeSide: {trade_input.tradeSide}")
        except Exception as e:
            print(f"Error in execute_operation: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error in execute_operation: {str(e)}")

    async def open_position(self) -> Response:
        if self.validate_enums(self.trade_input):
            await self.calculator_bitget.calculate(self.trade_input)
            trade = await self.create_json_trading(self.trade_input)
            body_trade = SerializableUtility.serialize_json(trade.model_dump())
            url = PathsBitget.PATH_BITGET + PathsBitget.REQUEST_PATH_FUTURES
            headers = self.bitget_auth.generate_headers(TimeUtility.get_timestamp(), RequestMethods.POST,
                                                        PathsBitget.REQUEST_PATH_FUTURES, body_trade,
                                                        self.bitget_auth.get_credentials().get("API_SECRET"))
            return await self.connection_bitget.execute_operation(body_trade, headers, url)
        else:
            print(f"Error in side or tradeSide: {self.trade_input.side} - {self.trade_input.tradeSide}")
            return Response(statusCode=400, data={"Error": "Error in side or tradeSide"}, valid=False)

    async def close_position(self) -> Response:
        if self.validate_enums(self.trade_input):
            await self.calculator_bitget.calculate(self.trade_input)
            trade = await self.create_json_trading(self.trade_input)
            body_trade = SerializableUtility.serialize_json(trade.model_dump())
            url = PathsBitget.PATH_BITGET + PathsBitget.REQUEST_PATH_FUTURES
            headers = self.bitget_auth.generate_headers(TimeUtility.get_timestamp(), RequestMethods.POST,
                                                        PathsBitget.REQUEST_PATH_FUTURES, body_trade,
                                                        self.bitget_auth.get_credentials().get("API_SECRET"))
            return await self.connection_bitget.execute_operation(body_trade, headers, url)
        else:
            print(f"Error in side or tradeSide: {self.trade_input.side} - {self.trade_input.tradeSide}")
            return Response(statusCode=400, data={"Error": "Error in side or tradeSide"} , valid=False)

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

    @staticmethod
    async def validate_enums(trade_input: InputDataTV) -> bool:
        return Validations.validate_enum(trade_input.side, PositionSide) and Validations.validate_enum(
            trade_input.tradeSide, OrderType)

    @staticmethod
    def validate_balance(balance: float) -> bool:
        if balance is None:
            print("Balance is None")
            raise HTTPException(status_code=400, detail=f"Balance is None")
        if not balance:
            print("Balance is empty")
            raise HTTPException(status_code=400, detail=f"Balance is empty")
        if balance < 5:
            print("Balance is less than 5")
            raise HTTPException(status_code=400, detail=f"Balance is less than 5")
        return True

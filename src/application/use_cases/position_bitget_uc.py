from typing import Optional

from fastapi import HTTPException

from src.domain.constants.request_methods import RequestMethods
from src.domain.constants.paths_bitget import PathsBitget
from .balance_bitget_uc import BalanceBitgetUC
from .calculator_bitget_uc import CalculatorBitgetUC
from ...domain.constants.dicts.dict_position_side import DICT_POSITION_SIDE
from ...domain.enums.order_type import OrderType
from ...domain.interfaces.position_repository import PositionRepository
from ...domain.models.positionValidate import PositionValidate
from ...domain.models.trade import Trade
from ...domain.models.response import Response
from ...domain.models.InputDataTV import InputDataTV
from ...infrastructure.adapters.bitget_auth import BitgetAuth
from ...infrastructure.adapters.connection_bitget import ConnectionBitget
from ...application.utilities.timeUtility import TimeUtility
from ...application.utilities.serializable_utility import SerializableUtility
from ...application.utilities.validations import Validations
from ...domain.enums.position_side import PositionSide


class PositionBitgetUC(PositionRepository):

    def __init__(self):
        self.connection_bitget = ConnectionBitget()
        self.bitget_auth: Optional[BitgetAuth] = None
        self.trade_input: Optional[InputDataTV] = None
        self.balance_uc: BalanceBitgetUC = BalanceBitgetUC()
        self.calculator_bitget: CalculatorBitgetUC = CalculatorBitgetUC()
        self.balance = 0.0

    async def execute_order(self, trade_input: InputDataTV, bitget_auth: BitgetAuth) -> Response:
        try:
            self.trade_input = trade_input
            self.bitget_auth = bitget_auth
            self.balance = float(await self.balance_uc.get_balance(self.bitget_auth))
            url: str = PathsBitget.REQUEST_PATH_GET_OPEN_POSITION_COIN.format(trade_input.symbol)
            position_validate_coin: PositionValidate = await Validations.validate_position_open_coin(
                url, trade_input.symbol, self.connection_bitget, self.bitget_auth)
            if position_validate_coin.open and position_validate_coin.holdSide == DICT_POSITION_SIDE.get(
                    trade_input.side):
                return await self.close_position(float(position_validate_coin.total),
                                                 position_validate_coin.holdSide)
            elif (position_validate_coin.open and position_validate_coin.holdSide != DICT_POSITION_SIDE.get(
                    trade_input.side)) or not position_validate_coin.open:
                if position_validate_coin.open:
                    await self.close_position(float(position_validate_coin.total), position_validate_coin.holdSide)
                return await self.open_position()
            else:
                print("Invalid execute_order: " + position_validate_coin.json())
                raise HTTPException(status_code=400,
                                    detail=f"Invalid execute_order: {position_validate_coin.json()}")
        except Exception as e:
            print(f"Error in execute_order: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error in execute_order: {str(e)}")

    async def open_position(self) -> Response:
        if await self.validate_enums(self.trade_input):
            response_calculator: Response =  await self.calculator_bitget.calculate(self.trade_input, self.balance)
            if response_calculator.valid:
                trade = await self.create_json_trading(self.trade_input, self.trade_input.size, OrderType.OPEN.value,
                                                       self.trade_input.side)
                body_trade = SerializableUtility.serialize_json(trade.model_dump())
                url = PathsBitget.PATH_BITGET + PathsBitget.REQUEST_PATH_FUTURES
                headers = self.bitget_auth.generate_headers(TimeUtility.get_timestamp(), RequestMethods.POST,
                                                            PathsBitget.REQUEST_PATH_FUTURES, body_trade,
                                                            self.bitget_auth.get_credentials().get("API_SECRET"))
                return await self.connection_bitget.execute_operation(body_trade, headers, url)
            else:
                print(f"Error in size: {self.trade_input.size}")
                return Response(statusCode=400, data={"Error": f"Undersized {self.trade_input.size}$"}, valid=False)
        else:
            print(f"Error in side: {self.trade_input.side}")
            return Response(statusCode=400, data={"Error": "Error in side"}, valid=False)

    async def close_position(self, total: float, hold_side: str) -> Response:
        if await self.validate_enums(self.trade_input):
            trade = await self.create_json_trading(self.trade_input, total, OrderType.CLOSE.value,
                                                   await self.get_key_from_value(DICT_POSITION_SIDE, hold_side))
            body_trade = SerializableUtility.serialize_json(trade.model_dump())
            url = PathsBitget.PATH_BITGET + PathsBitget.REQUEST_PATH_FUTURES
            headers = self.bitget_auth.generate_headers(TimeUtility.get_timestamp(), RequestMethods.POST,
                                                        PathsBitget.REQUEST_PATH_FUTURES, body_trade,
                                                        self.bitget_auth.get_credentials().get("API_SECRET"))
            return await self.connection_bitget.execute_operation(body_trade, headers, url)
        else:
            print(f"Error in side or tradeSide: {self.trade_input.side} - {self.trade_input.tradeSide}")
            return Response(statusCode=400, data={"Error": "Error in side or tradeSide"}, valid=False)

    @staticmethod
    async def create_json_trading(trade_input: InputDataTV, total: float = 0, trade_side: str = "",
                                  hold_side: str = "") -> Trade:
        return Trade(
            symbol=trade_input.symbol,
            productType="USDT-FUTURES",
            marginMode="isolated",
            marginCoin="USDT",
            size=total,
            side=hold_side,  # buy or sell
            tradeSide=trade_side,  # close or open
            orderType="market",
            timeInForceValue="normal",
            clientOid=TimeUtility.get_timestamp_datetime(),
        )

    @staticmethod
    async def validate_enums(trade_input: InputDataTV) -> bool:
        return Validations.validate_enum(trade_input.side, PositionSide)

    @staticmethod
    async def get_key_from_value(dictionary: dict, value: str) -> str:
        return next((key for key, val in dictionary.items() if val == value), None)

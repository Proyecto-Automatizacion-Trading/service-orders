from fastapi import HTTPException

from src.application.utilities.timeUtility import TimeUtility
from src.domain.constants.paths_bitget import PathsBitget
from src.domain.constants.request_methods import RequestMethods
from src.domain.interfaces.connection_exchange import ConnectionExchange
from src.domain.interfaces.exchange_auth import ExchangeAuth
from src.domain.models.positionValidate import PositionValidate


class Validations:

    @staticmethod
    def validate_enum(value, enum) -> bool:
        try:
            return any(value == item.value for item in enum)
        except Exception as e:
            print(f"Error in validate_enum: {str(e)}")
            raise e

    @staticmethod
    async def validate_balance(balance: float) -> bool:
        if balance is None:
            print("Balance is None")
            raise HTTPException(status_code=400, detail=f"Balance is None")
        if not balance:
            print("Balance is empty")
            raise HTTPException(status_code=400, detail=f"Balance is empty")
        if balance < 5.5:
            print("Balance is less than 6")
            raise HTTPException(status_code=400, detail=f"Balance is less than 6")
        return True

    @staticmethod
    async def validate_position_open_coin(url: str, token: str,
                                          connection_exchange: ConnectionExchange,
                                          exchange_auth: ExchangeAuth) -> PositionValidate:
        try:
            headers = exchange_auth.generate_headers(TimeUtility.get_timestamp_iso8601(), RequestMethods.GET, url, "",
                                                     exchange_auth.get_credentials().get('API_SECRET'))
            url_request = PathsBitget.PATH_BITGET + url
            response = await connection_exchange.get_open_position_coin(url_request, headers)
            if response["data"] is None or len(response["data"]) == 0:
                return PositionValidate(symbol=token, open=False, holdSide="", total="")
            return PositionValidate(symbol=token, open=True, holdSide=response["data"][0]["holdSide"],
                                    total=response["data"][0]["total"])
        except Exception as e:
            print(f"Error in validate_position_open_coin: {str(e)}")
            raise e

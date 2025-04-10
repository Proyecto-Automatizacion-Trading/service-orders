from src.application.utilities.timeUtility import TimeUtility
from src.domain.constants.paths_bitget import PathsBitget
from src.domain.constants.request_methods import RequestMethods
from src.domain.interfaces.balance import Balance
from src.infrastructure.adapters.bitget_auth import BitgetAuth
from src.infrastructure.adapters.connection_bitget import ConnectionBitget


class BalanceBitgetUC(Balance):

    def __init__(self):
        self.connection_bitget: ConnectionBitget = ConnectionBitget()

    async def get_balance(self, bitget_auth: BitgetAuth) -> float:
        url = PathsBitget.PATH_BITGET + PathsBitget.REQUEST_PATH_BALANCE_FUTURES
        headers = bitget_auth.generate_headers(TimeUtility.get_timestamp_iso8601(), RequestMethods.GET,
                                               PathsBitget.REQUEST_PATH_BALANCE_FUTURES, "",
                                               bitget_auth.get_credentials().get("API_SECRET"))
        response = await self.connection_bitget.get_balance(headers, url)
        if response["data"] is None:
            return 0
        return response["data"][0]["available"]

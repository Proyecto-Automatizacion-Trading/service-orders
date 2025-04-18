from fastapi import HTTPException

from src.application.utilities.timeUtility import TimeUtility
from src.domain.constants.paths_bitget import PathsBitget
from src.domain.constants.request_methods import RequestMethods
from src.domain.abstracts.connection_exchange_repository import ConnectionExchange
from src.domain.abstracts.exchange_auth_repository import ExchangeAuth
from src.domain.models.exchangeApiKeyModel import ExchangeApiKeyModel
from src.domain.models.positionValidate import PositionValidate


class Validations:
    """
    Esta clase contiene métodos estáticos para la validación de los datos antes de realizar una operación en la API de
    Exchange Bitget.

    Attributes:
        None
    """

    @staticmethod
    def validate_enum(value, enum) -> bool:
        """
        Valida si un valor se encuentra en una enumeración.

        Args:
        value (str): Valor a validar
        enum (Enum): Enumeración a la que se va a validar el valor

        Returns:
        bool: Verdadero si el valor se encuentra en la enumeración, False de lo contrario.
        """
        try:
            return any(value == item.value for item in enum)
        except Exception as e:
            print(f"Error en validate_enum: {str(e)}")
            raise e

    @staticmethod
    async def validate_balance(balance: float) -> bool:
        """
        Valida si el saldo es mayor o igual a 6.

        Args:
        balance (float): Saldo a validar

        Returns:
        bool: Verdadero si el saldo es mayor o igual a 6, False de lo contrario.
        """
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
    async def validate_position_open_coin(
            url: str, token: str, connection_exchange: ConnectionExchange, exchange_auth: ExchangeAuth,
            exchange_api_key: ExchangeApiKeyModel) -> PositionValidate:
        """
        Valida si la posición de un token está abierta en la API de Bitget.

        Args:
        url (str): URL para la petición de la posición abierta
        token (str): Símbolo del token a validar
        connection_exchange (ConnectionExchange): Instancia de la conexión a la API de Bitget
        exchange_auth (ExchangeAuth): Instancia de la autenticación para la API de Bitget
        exchange_api_key (ExchangeApiKeyModel): Modelo de la llave de la API de Bitget

        Returns:
        PositionValidate: Objeto con la información de la posición abierta.
        """
        try:
            headers = exchange_auth.generate_headers(TimeUtility.get_timestamp_iso8601(), RequestMethods.GET, url, "",
                                                     exchange_api_key.get('api_secret'))
            url_request = PathsBitget.PATH_BITGET + url
            response = await connection_exchange.get_open_position_coin(url_request, headers)
            if response["data"] is None or len(response["data"]) == 0:
                return PositionValidate(symbol=token, open=False, holdSide="", total="")
            return PositionValidate(symbol=token, open=True, holdSide=response["data"][0]["holdSide"],
                                    total=response["data"][0]["total"])
        except Exception as e:
            print(f"Error in validate_position_open_coin: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error in validate_position_open_coin: {str(e)}")

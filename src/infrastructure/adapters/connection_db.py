from typing import List

import aiohttp

from src.domain.abstracts.connection_service_database_repository import ConnectionServiceDatabase
from src.domain.models import InputDataTV
from src.domain.models.exchangeApiKeyModel import ExchangeApiKeyModel
import requests


class ConnectionDB(ConnectionServiceDatabase):

    async def get_array_api_keys(self, input_data_tv: InputDataTV) -> List[ExchangeApiKeyModel]:
        try:
            print("Obteniendo Datos BD..." + "--" * 10)
            url = self.build_api_url(input_data_tv.temporality, input_data_tv.strategy, input_data_tv.symbol)
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Status Code BD: {response.status_code}")
                raise Exception
            data = response.json()
            print(f"Status Code BD: {response.status_code}")
            return data
        except Exception as e:
            print(f"Error in get data base: {str(e)}")
            raise e

    @staticmethod
    def build_api_url(temporality, strategy, symbol):
        base_url = "https://apigo.lat:443/api/v1/usuarios/apikeys"
        return f"{base_url}?temporalidad={temporality}&estrategia={strategy}&moneda={symbol}"

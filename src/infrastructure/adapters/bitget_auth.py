import base64
import hashlib
import hmac

from typing import Dict
from my_config import SECRETS

from ...domain.abstracts.exchange_auth_repository import ExchangeAuth
from ...domain.models.exchangeApiKeyModel import ExchangeApiKeyModel


class BitgetAuth(ExchangeAuth):

    def __init__(self):
        self.exchange_api_key = None

    def generate_signature(self, timestamp, method, request_path, body, secret) -> str:
        message = timestamp + method + request_path + body
        signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
        return base64.b64encode(signature).decode()

    def generate_headers(self, timestamp, method, request_path, body, secret) -> Dict[str, str]:
        return {
            'ACCESS-KEY': self.get_exchange_api_key().get('api_key'),
            'ACCESS-SIGN': self.generate_signature(timestamp, method, request_path, body, secret),
            'ACCESS-PASSPHRASE': self.get_exchange_api_key().get('api_passphrase'),
            'ACCESS-TIMESTAMP': timestamp,
            'Content-Type': 'application/json'
        }

    @staticmethod
    def generate_signature_debug(timestamp, method, request_path, body, secret):
        # Mostrar cada componente y su representación
        print("Timestamp repr:", repr(timestamp))
        print("Method repr:", repr(method))
        print("Request path repr:", repr(request_path))
        print("Body repr:", repr(body))

        message = timestamp + method + request_path + body
        print("Concatenated message repr:", repr(message))

        print("Secret repr:", repr(secret))

        print("Length of secret:", len(secret))
        print("Hex of secret:", secret.encode().hex())

        signature = hmac.new(secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).digest()
        encoded_signature = base64.b64encode(signature).decode('utf-8')

        print("Generated signature:", encoded_signature)
        print(repr(timestamp), repr(method), repr(request_path), repr(body), repr(secret))
        return encoded_signature

    def set_exchange_api_key(self, exchange_api_key: ExchangeApiKeyModel) -> None:
        self.exchange_api_key = exchange_api_key

    def get_exchange_api_key(self) -> ExchangeApiKeyModel:
        return self.exchange_api_key

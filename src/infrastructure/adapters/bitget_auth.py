import base64
import hashlib
import hmac

from typing import Dict
from config import SECRETS

from ...domain.interfaces.exchange_auth import ExchangeAuth


class BitgetAuth(ExchangeAuth):
    def get_credentials(self) -> Dict[str, str]:
        return {
            'API_KEY': SECRETS["API_KEY"],
            'API_SECRET': SECRETS["API_SECRET"],
            'API_PASSPHRASE': SECRETS["API_PASSPHRASE"]
        }

    def generate_signature(self, timestamp, method, request_path, body, secret) -> str:
        message = timestamp + method + request_path + body
        signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
        return base64.b64encode(signature).decode()

    def generate_headers(self, timestamp, method, request_path, body, secret) -> Dict[str, str]:
        return {
            'ACCESS-KEY': self.get_credentials().get('API_KEY'),
            'ACCESS-SIGN': self.generate_signature(timestamp, method, request_path, body, secret),
            'ACCESS-PASSPHRASE': self.get_credentials().get('API_PASSPHRASE'),
            'ACCESS-TIMESTAMP': timestamp,
            'Content-Type': 'application/json'
        }

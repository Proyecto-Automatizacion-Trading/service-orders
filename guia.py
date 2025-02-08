import time
import hmac
import hashlib
import base64
import json
import requests
from config import SECRETS

# Credenciales de acceso
API_KEY = SECRETS["API_KEY"]
API_SECRET = SECRETS["API_SECRET"]
API_PASSPHRASE = SECRETS["API_PASSPHRASE"]


def get_timestamp():
    return str(int(time.time() * 1000))


def generate_signature(timestamp, method, request_path, body, secret) -> str:
    message = timestamp + method + request_path + body
    signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
    return base64.b64encode(signature).decode()


# Datos de la orden modificados
order_data = {
    "symbol": "PEPEUSDT",
    "productType": "USDT-FUTURES",
    "marginMode": "isolated",
    "marginCoin": "USDT",
    "size": 398000,
    "side": "sell",  # Cambiado de "buy" a "sell"
    "tradeSide": "close",  # Cambiado de "close" a "open"
    "orderType": "market",
    "timeInForceValue": "normal",  # Cambiado de "force" a "timeInForceValue"
    "clientOid": str(int(time.time() * 1000)),
    "leverage": "5"
}

# Convertir el JSON a string
body = json.dumps(order_data, separators=(",", ":"))

timestamp = get_timestamp()
method = "POST"
request_path = "/api/v2/mix/order/place-order"

signature = generate_signature(timestamp, method, request_path, body, API_SECRET)

headers = {
    "ACCESS-KEY": API_KEY,
    "ACCESS-SIGN": signature,
    "ACCESS-PASSPHRASE": API_PASSPHRASE,
    "ACCESS-TIMESTAMP": timestamp,
    "Content-Type": "application/json"
}

url = "https://api.bitget.com" + request_path

# Agregar manejo de errores
try:
    response = requests.post(url, headers=headers, data=body)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {str(e)}")

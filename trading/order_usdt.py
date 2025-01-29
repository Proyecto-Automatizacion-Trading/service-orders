import time
import hmac
import hashlib
import base64
import json
import requests

# 🚀 Tus credenciales API de Bitget
API_KEY = "bg_c9f10de1be92d3ca1abbb66ff27e02ef"
API_SECRET = "282852162291061fa30feabf99f61c40334b5b4e88f0ff74cd1ed117309069f2"
API_PASSPHRASE = "4872931650"

# 🔹 Obtener el precio actual de ETH/USDT
def get_eth_price():
    url = "https://api.bitget.com/api/v2/market/ticker?symbol=ETHUSDT"
    response = requests.get(url)
    data = response.json()
    return float(data["data"]["last"])

# 🔹 Generar timestamp
def get_timestamp():
    return str(int(time.time() * 1000))

# 🔹 Generar firma HMAC SHA256 en base64
def generate_signature(timestamp, method, request_path, body, secret):
    message = timestamp + method + request_path + body
    signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
    return base64.b64encode(signature).decode()

# 🔹 Monto en USDT que quieres invertir
usdt_amount = 1  # 👈 Aquí defines el monto en USDT que deseas invertir

# 🔹 Obtener precio actual de ETH/USDT
eth_price = get_eth_price()

# 🔹 Calcular tamaño (size) en ETH
size = round(usdt_amount / eth_price, 6)  # Redondeamos a 6 decimales

# 🔹 Crear el cuerpo de la orden
order_data = {
    "symbol": "ETHUSDT",
    "productType": "USDT-FUTURES",
    "marginMode": "isolated",
    "marginCoin": "USDT",
    "size": str(size),  # Tamaño calculado en función del USDT
    "side": "buy",
    "tradeSide": "open",
    "orderType": "market",
    "force": "ioc",
    "clientOid": "121211212122"
}

# 🔹 Convertir JSON a string sin espacios extra
body = json.dumps(order_data, separators=(",", ":"))

# 🔹 Datos para firmar la petición
timestamp = get_timestamp()
method = "POST"
request_path = "/api/v2/mix/order/place-order"

# 🔹 Generar firma
signature = generate_signature(timestamp, method, request_path, body, API_SECRET)

# 🔹 Configurar los headers
headers = {
    "ACCESS-KEY": API_KEY,
    "ACCESS-SIGN": signature,
    "ACCESS-PASSPHRASE": API_PASSPHRASE,
    "ACCESS-TIMESTAMP": timestamp,
    "Content-Type": "application/json"
}

# 🔹 URL de la API de Bitget
url = "https://api.bitget.com" + request_path

# 🔹 Enviar la orden
response = requests.post(url, headers=headers, data=body)

# 🔹 Mostrar respuesta
print(f"ETH Price: {eth_price}")
print(f"Size (ETH): {size}")
print(f"Response: {response.status_code}")
print(response.json())

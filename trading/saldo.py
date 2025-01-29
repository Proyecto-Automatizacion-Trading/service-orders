import time
import hmac
import hashlib
import base64
import requests

# Credenciales de acceso
API_KEY = "bg_c9f10de1be92d3ca1abbb66ff27e02ef"
API_SECRET = "282852162291061fa30feabf99f61c40334b5b4e88f0ff74cd1ed117309069f2"
API_PASSPHRASE = "4872931650"

def get_timestamp():
    return str(int(time.time() * 1000))

def generate_signature(timestamp, method, request_path, body, secret):
    message = timestamp + method + request_path + body
    signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
    return base64.b64encode(signature).decode()

# Generar los valores requeridos
timestamp = get_timestamp()
method = "GET"
request_path = "/api/v2/mix/account/accounts?productType=USDT-FUTURES"
body = ""

# Generar firma
signature = generate_signature(timestamp, method, request_path, body, API_SECRET)

# Configurar los headers
headers = {
    "ACCESS-KEY": API_KEY,
    "ACCESS-SIGN": signature,
    "ACCESS-PASSPHRASE": API_PASSPHRASE,
    "ACCESS-TIMESTAMP": timestamp,
    "Content-Type": "application/json"
}

# URL de la API de Bitget
url = "https://api.bitget.com" + request_path

# Enviar la solicitud a Bitget
response = requests.get(url, headers=headers)

# Mostrar respuesta
print(response.status_code)
print(response.json())

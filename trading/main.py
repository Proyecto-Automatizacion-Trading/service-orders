import requests
import time

# Configuración
API_URL = "https://api.bitget.com/api/mix/v1/market/candles"
symbol = "BTCUSDT"  # Cambia por el par que necesites
granularity = 60  # 1 minuto (puedes usar 300, 900, etc.)
start_time = int(time.time() - 3600 * 24) * 1000  # Últimas 24 horas
end_time = int(time.time()) * 1000  # Hasta ahora

# Solicitud
params = {
    "symbol": symbol,
    "granularity": granularity,
    "startTime": start_time,
    "endTime": end_time
}

response = requests.get(API_URL, params=params)
if response.status_code == 200:
    data = response.json()
    print("Datos obtenidos:", data)
else:
    print("Error:", response.status_code, response.text)

from fastapi import FastAPI, Depends, HTTPException
from mangum import Mangum

from src.application.handlers.operations_handler import OperationsHandler
from src.domain.models.InputDataTV import InputDataTV
from src.domain.models.response import Response

app = FastAPI(
    title="Trading Algorítmico",
    description="API para ejecutar ordenes de trading automático",
    version="1.0.0"
)


def get_operations_handler() -> OperationsHandler:
    return OperationsHandler()


@app.get("/lambda")
async def home():
    return {"mensaje": "¡Hola desde Trading Fast Lambda!"}


@app.get("/webhook/alert/tradingview/")
async def health_check():
    return {"status": "ok"}


@app.post("/webhook/alert/tradingview/",
          response_model=Response,
          summary="Controla las alertas que llegan de trading view y determina el exchange para ejecutar la orden",
          description="Recibe alertas de TradingView y ejecuta operaciones en los distintos exchange"
          )
async def controller_tradingview_webhook_alert(
        alert: InputDataTV,
        controller: OperationsHandler = Depends(get_operations_handler)
):
    try:
        return await controller.positions_handler(alert)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in controller_tradingview_webhook_alert: {str(e)}"
        )


@app.get("/handler/health")
async def health_check(controller: OperationsHandler = Depends(get_operations_handler)):
    api_keys = await controller.get_array_api_keys()
    print(api_keys)
    return {"status": "ok", "api_keys": api_keys}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

# Adaptador para que funcione en Lambda
lambda_handler = Mangum(app)

from fastapi import FastAPI, Depends, HTTPException
from mangum import Mangum

from src.application.use_cases.controller_exchanges_uc import ControllerExchangesUC
from src.domain.models.InputDataTV import InputDataTV
from src.domain.models.response import Response

app = FastAPI(
    title="Trading Algorítmico",
    description="API para ejecutar ordenes de trading automático",
    version="1.0.0"
)


def get_controller_exchanges_uc() -> ControllerExchangesUC:
    return ControllerExchangesUC()


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
        controller: ControllerExchangesUC = Depends(get_controller_exchanges_uc)
):
    try:
        return await controller.controller_exchanges(alert)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in controller_tradingview_webhook_alert: {str(e)}"
        )


# Adaptador para que funcione en Lambda
lambda_handler = Mangum(app)

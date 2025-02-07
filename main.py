import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from src.domain.models.InputDataTV import InputDataTV
from src.application.use_cases.position_bitget_uc import PositionBitgetUC
from src.domain.enums.order_type import OrderType
from src.infrastructure.adapters.bitget_auth import BitgetAuth
from src.domain.models.response import Response

app = FastAPI(
    title="Trading Algorítmico",
    description="API para ejecutar ordenes de trading automático",
    version="1.0.0"
)


# Función de dependencia para crear la autenticación de Bitget
def get_bitget_auth() -> BitgetAuth:
    try:
        return BitgetAuth()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al inicializar BitgetAuth: {str(e)}"
        )


# Función de dependencia para crear el caso de uso de posiciones
def get_position_use_case(auth_bitget: BitgetAuth = Depends(get_bitget_auth)) -> PositionBitgetUC:
    return PositionBitgetUC()


@app.post("/webhook/alert/tradingview/bitget/",
          response_model=Response,
          summary="Procesa alertas de TradingView para Bitget",
          description="Recibe alertas de TradingView y ejecuta operaciones en Bitget"
          )
async def tradingview_webhook_alert(
        alert: InputDataTV,
        position_bitget_uc: PositionBitgetUC = Depends(get_position_use_case),
        bitget_auth: BitgetAuth = Depends(get_bitget_auth)
):
    try:
        if alert.tradeSide == OrderType.OPEN.value:
            return await position_bitget_uc.open_position(alert, bitget_auth)
        elif alert.tradeSide == OrderType.CLOSE.value:
            return await position_bitget_uc.close_position(alert, bitget_auth)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Operación Inválida: {alert.tradeSide}"
            )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error in tradingview_webhook_alert: {str(e)}"
        )


@app.get("/health",
         summary="Health check endpoint",
         description="Verifica el estado del servicio")
async def health_check():
    return {
        "status": "healthy",
        "service": "trading-bot",
        "version": "1.0.0"
    }


@app.get("/",
         summary="Root endpoint",
         description="Endpoint de bienvenida")
async def root():
    return {
        "message": "Welcome to Trading Bot API",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

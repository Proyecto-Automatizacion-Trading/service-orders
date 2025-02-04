import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from .src.domain.models.InputDataTV import InputDataTV
from .src.application.use_cases.position_bitget_uc import PositionBitgetUC
from .src.domain.enums.order_type import OrderType

app = FastAPI()


@app.post("/webhook/alert/tradingview")
async def tradingview_webhook_alert(alert: InputDataTV,
                                    position_use_case: PositionBitgetUC = Depends(PositionBitgetUC)):
    try:
        if alert.tradeSide == OrderType.OPEN.value:
            await position_use_case.open_position(alert)
        elif alert.tradeSide == OrderType.CLOSE.value:
            await position_use_case.close_position(alert)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

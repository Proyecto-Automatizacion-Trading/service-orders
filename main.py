import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from src.domain.models.InputDataTV import InputDataTV
from src.application.use_cases.position_bitget_uc import PositionBitgetUC
from src.domain.enums.order_type import OrderType
from src.infraestructure.adapters.bitget_auth import BitgetAuth

app = FastAPI()


@app.post("/webhook/alert/tradingview/bitget")
async def tradingview_webhook_alert(
        alert: InputDataTV,
        position_use_case: PositionBitgetUC = Depends(PositionBitgetUC),
        bitget_auth: BitgetAuth = Depends(BitgetAuth)
):
    try:
        if alert.tradeSide == OrderType.OPEN.value:
            await position_use_case.open_position(alert, bitget_auth)
        elif alert.tradeSide == OrderType.CLOSE.value:
            await position_use_case.close_position(alert)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


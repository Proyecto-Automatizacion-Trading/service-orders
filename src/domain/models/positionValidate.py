from pydantic import BaseModel


class PositionValidate(BaseModel):
    symbol: str
    open: bool
    holdSide: str
    total: str

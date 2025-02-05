from pydantic import BaseModel


class Response(BaseModel):
    statusCode: int
    data: str
    valid: bool

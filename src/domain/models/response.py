from pydantic import BaseModel


class Response(BaseModel):
    statusCode: int
    data: dict
    valid: bool

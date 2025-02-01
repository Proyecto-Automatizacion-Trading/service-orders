from dataclasses import dataclass
from datetime import datetime
from pydantic import BaseModel


class ClientResponse:
    clientOid: str
    orderId: str


@dataclass
class Response(BaseModel):
    statusCode: int
    code: str
    msg: str
    requestTime: datetime
    data: ClientResponse

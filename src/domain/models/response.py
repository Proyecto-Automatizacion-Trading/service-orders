from dataclasses import dataclass
from datetime import datetime


class ClientResponse:
    clientOid: str
    orderId: str


@dataclass
class Response:
    statusCode: int
    code: str
    msg: str
    requestTime: datetime
    data: ClientResponse

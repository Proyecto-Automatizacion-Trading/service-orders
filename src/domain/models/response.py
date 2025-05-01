from typing import Union, Dict, List

from pydantic import BaseModel


class Response(BaseModel):
    statusCode: int
    data: Union[Dict, List]
    valid: bool

from pydantic import BaseModel


class ExchangeApiKeyModel(BaseModel):
    apiKey: str
    exchange: str

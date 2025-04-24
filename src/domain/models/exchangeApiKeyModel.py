class ExchangeApiKeyModel(dict):
    def __init__(self, api_key: str, api_secret: str, passphrase: str, exchange: str, is_percentage: bool, size: float):
        super().__init__(
            {
                "api_key": api_key,
                "api_secret": api_secret,
                "api_passphrase": passphrase,
                "exchange": exchange,
                "is_percentage": is_percentage,
                "size": size
            }
        )

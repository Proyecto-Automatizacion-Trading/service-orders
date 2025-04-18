class ExchangeApiKeyModel(dict):
    def __init__(self, api_key: str, api_secret: str, passphrase: str, exchange: str):
        super().__init__(
            {"api_key": api_key, "api_secret": api_secret, "api_passphrase": passphrase, "exchange": exchange})

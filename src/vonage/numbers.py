import vonage

class Numbers:
    def __init__(self, client):
        self._client = client
        
    def get_account_numbers(self, params=None, **kwargs):
        return self._client.get(self._client.host(), "/account/numbers", params or kwargs)

    def get_available_numbers(self, country_code, params=None, **kwargs):
        return self._client.get(
            self._client.host(), "/number/search", dict(params or kwargs, country=country_code)
        )

    def buy_number(self, params=None, **kwargs):
        return self._client.post(self._client.host(), "/number/buy", params or kwargs)

    def cancel_number(self, params=None, **kwargs):
        return self._client.post(self._client.host(), "/number/cancel", params or kwargs)

    def update_number(self, params=None, **kwargs):
        return self._client.post(self._client.host(), "/number/update", params or kwargs)

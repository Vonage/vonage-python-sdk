import vonage

class Numbers:
    def __init__(
        self,
        client=None,
        key=None,
        secret=None,
        signature_secret=None,
        signature_method=None
    ):
        try:
            self._client = client
            if self._client is None:
                self._client = vonage.Client(
                    key=key,
                    secret=secret,
                    signature_secret=signature_secret,
                    signature_method=signature_method
                )
        except Exception as e:
            print(f'Error: {str(e)}')

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

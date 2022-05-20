import vonage

class Account:
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

    def get_balance(self):
        return self._client.get(self._client.host(), "/account/get-balance")

    def get_country_pricing(self, country_code):
        return self._client.get(
            self._client.host(), "/account/get-pricing/outbound", {"country": country_code}
        )

    def get_prefix_pricing(self, prefix):
        return self._client.get(
            self._client.host(), "/account/get-prefix-pricing/outbound", {"prefix": prefix}
        )
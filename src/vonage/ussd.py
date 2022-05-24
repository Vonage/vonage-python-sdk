import vonage

class Ussd:
    #To init Sms class pass a client reference or a key and secret
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

    def send_ussd_push_message(self, params=None, **kwargs):
        return self._client.post(self._client.host(), "/ussd/json", params or kwargs)

    def send_ussd_prompt_message(self, params=None, **kwargs):
        return self._client.post(self._client.host(), "/ussd-prompt/json", params or kwargs)

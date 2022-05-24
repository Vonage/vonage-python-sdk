import vonage

class ShortCodes:
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

    def send_2fa_message(self, params=None, **kwargs):
        return self._client.post(self._client.host(), "/sc/us/2fa/json", params or kwargs)

    def send_event_alert_message(self, params=None, **kwargs):
        return self._client.post(self._client.host(), "/sc/us/alert/json", params or kwargs)

    def send_marketing_message(self, params=None, **kwargs):
        return self._client.post(self._client.host(), "/sc/us/marketing/json", params or kwargs)

    def get_event_alert_numbers(self):
        return self._client.get(self._client.host(), "/sc/us/alert/opt-in/query/json")

    def resubscribe_event_alert_number(self, params=None, **kwargs):
        return self._client.post(
            self._client.host(), "/sc/us/alert/opt-in/manage/json", params or kwargs
        )
    
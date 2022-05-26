class ShortCodes:
    def __init__(self, client):
        self._client = client

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
    
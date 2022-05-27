class Messages:
    def __init__(self, client):
        self._client = client

    def send_message(self, params):
        return self._client.post(self._client.api_host(), "/v1/messages", params, header_auth=True)
        
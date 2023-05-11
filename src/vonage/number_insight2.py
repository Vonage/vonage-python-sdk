class NumberInsight2:
    def __init__(self, client):
        self._client = client
        self._auth_type = 'jwt'

    def fraud_check(self, params: dict):
        return self._client.post(self._client.api_host(), '/v2/ni', params, auth_type=self._auth_type)

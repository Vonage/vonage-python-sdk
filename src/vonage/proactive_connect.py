class ProactiveConnect:
    def __init__(self, client):
        self._client = client
        self._auth_type = 'jwt'

    def list_all_lists(self, page: int = None, page_size: int = None):
        params = {}
        if page:
            params['page'] = page
        if page_size:
            params['page_size'] = page_size

        return self._client.get(
            self._client.proactive_connect_host(), '/v0.1/bulk/lists', params, auth_type=self._auth_type
        )

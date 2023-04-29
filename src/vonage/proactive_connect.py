from .errors import ProactiveConnectError


class ProactiveConnect:
    def __init__(self, client):
        self._client = client
        self._auth_type = 'jwt'

    def list_all_lists(self, page: int = None, page_size: int = None):
        params = self._check_pagination_params(page, page_size)
        return self._client.get(
            self._client.proactive_connect_host(), '/v0.1/bulk/lists', params, auth_type=self._auth_type
        )

    def create_list(self, params: dict):
        self._validate_list_params(params)
        return self._client.post(
            self._client.proactive_connect_host(), '/v0.1/bulk/lists', params, auth_type=self._auth_type
        )

    def get_list(self, list_id: str):
        return self._client.get(
            self._client.proactive_connect_host(), f'/v0.1/bulk/lists/{list_id}', auth_type=self._auth_type
        )

    def update_list(self, list_id: str, params: dict):
        self._validate_list_params(params)
        return self._client.put(
            self._client.proactive_connect_host(), f'/v0.1/bulk/lists/{list_id}', params, auth_type=self._auth_type
        )

    def delete_list(self, list_id: str):
        return self._client.delete(
            self._client.proactive_connect_host(), f'/v0.1/bulk/lists/{list_id}', auth_type=self._auth_type
        )

    def clear_list(self, list_id: str):
        return self._client.post(
            self._client.proactive_connect_host(),
            f'/v0.1/bulk/lists/{list_id}/clear',
            params=None,
            auth_type=self._auth_type,
        )

    def sync_list_from_datasource(self, list_id: str):
        return self._client.post(
            self._client.proactive_connect_host(),
            f'/v0.1/bulk/lists/{list_id}/fetch',
            params=None,
            auth_type=self._auth_type,
        )

    def _check_pagination_params(self, page=None, page_size=None) -> dict:
        params = {}
        if page is not None:
            if type(page) == int and page > 0:
                params['page'] = page
            elif page <= 0:
                raise ProactiveConnectError('"page" must be an int > 0.')
        if page_size is not None:
            if type(page_size) == int and page_size > 0:
                params['page_size'] = page_size
            elif page_size and page_size <= 0:
                raise ProactiveConnectError('"page_size" must be an int > 0.')
        return params

    def _validate_list_params(self, params: dict):
        if 'name' not in params:
            raise ProactiveConnectError('You must supply a name for the new list.')
        if 'datasource' in params and 'type' in params['datasource'] and params['datasource']['type'] == 'salesforce':
            self._check_salesforce_params_correct(params['datasource'])

    def _check_salesforce_params_correct(self, datasource):
        if 'integration_id' not in datasource or 'soql' not in datasource:
            raise ProactiveConnectError(
                'You must supply a value for "integration_id" and "soql" when creating a list with Salesforce.'
            )
        if type(datasource['integration_id']) is not str or type(datasource['soql']) is not str:
            raise ProactiveConnectError('You must supply values for "integration_id" and "soql" as strings.')

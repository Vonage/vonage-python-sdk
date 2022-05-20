import vonage
from .errors import CallbackRequiredError

class NumberInsight:
    # To init NumberInsight class, pass a client reference or a key and secret
    def __init__(
        self,
        client=None,
        key=None,
        secret=None,
    ):
        try:
            self._client = client
            if self._client is None:
                self._client = vonage.Client(
                    key=key,
                    secret=secret
                )
        except Exception as e:
            print(f'Error: {str(e)}')

    def get_basic_number_insight(self, params=None, **kwargs):
        return self._client.get(self._client.api_host(), "/ni/basic/json", params or kwargs)

    def get_standard_number_insight(self, params=None, **kwargs):
        return self._client.get(self._client.api_host(), "/ni/standard/json", params or kwargs)

    def get_advanced_number_insight(self, params=None, **kwargs):
        return self._client.get(self._client.api_host(), "/ni/advanced/json", params or kwargs)

    def get_async_advanced_number_insight(self, params=None, **kwargs):
        argoparams = params or kwargs
        if "callback" in argoparams:
            return self._client.get(
                self._client.api_host(), "/ni/advanced/async/json", params or kwargs
            )
        else:
            raise CallbackRequiredError(
                "A callback is needed for async advanced number insight"
            )
    
    def request_number_insight(self, params=None, **kwargs):
        return self._client.post(self._client.host(), "/ni/json", params or kwargs)
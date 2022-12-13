from .errors import CallbackRequiredError, NumberInsightError
import json

class NumberInsight:
    auth_type = 'params'
    
    def __init__(self, client):
        self._client = client

    def get_basic_number_insight(self, params=None, **kwargs):
        response = self._client.get(self._client.api_host(), "/ni/basic/json", params or kwargs, auth_type=NumberInsight.auth_type)
        self.check_for_error(response)

        return response

    def get_standard_number_insight(self, params=None, **kwargs):
        response = self._client.get(self._client.api_host(), "/ni/standard/json", params or kwargs, auth_type=NumberInsight.auth_type)
        self.check_for_error(response)

        return response

    def get_advanced_number_insight(self, params=None, **kwargs):
        response = self._client.get(self._client.api_host(), "/ni/advanced/json", params or kwargs, auth_type=NumberInsight.auth_type)
        self.check_for_error(response)

        return response

    def get_async_advanced_number_insight(self, params=None, **kwargs):
        argoparams = params or kwargs
        self.check_for_callback(argoparams)
        
        if "callback" in argoparams and type(argoparams["callback"]) == str and argoparams["callback"] != "":
            return self._client.get(
                self._client.api_host(), "/ni/advanced/async/json", params or kwargs, auth_type=NumberInsight.auth_type
            )
        else:
            raise CallbackRequiredError(
                "A callback is needed for async advanced number insight"
            )
    
    def check_for_error(self, response):
        if response['status'] != 0:
            raise NumberInsightError(f'Number Insight API method failed with status: {response["status"]} and error: {response["status_message"]}')

    def check_for_callback(self, argoparams):
        if not any("callback" in argoparams and type(argoparams["callback"]) == str and argoparams["callback"] != ""):
            raise CallbackRequiredError(
                "A callback is needed for async advanced number insight"
            )

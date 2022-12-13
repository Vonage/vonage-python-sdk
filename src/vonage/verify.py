from .errors import VerifyError, BlockedNumberError


class Verify:
    auth_type = 'params'
    defaults = {'auth_type': auth_type, 'body_is_json': False}

    def __init__(self, client):
        self._client = client

    def start_verification(self, params=None, **kwargs):
        response = self._client.post(
            self._client.api_host(), 
            "/verify/json", 
            params or kwargs,
            **Verify.defaults,
        )

        self.check_for_error(response)
        return response

    def check(self, request_id, code):
        response = self._client.post(
            self._client.api_host(),
            "/verify/check/json",
            {"request_id": request_id, "code": code},
            **Verify.defaults,
        )

        self.check_for_error(response)
        return response

    def search(self, request_id=None, request_ids=None):
        if request_id:
            response = self._client.get(
                self._client.api_host(), "/verify/search/json", {"request_id": request_id}, auth_type=Verify.auth_type
            )
        elif request_ids:
            response = self._client.get(
                self._client.api_host(), "/verify/search/json", {"request_ids": request_ids}, auth_type=Verify.auth_type
            )
        else:
            raise VerifyError('At least one request ID must be provided.')

        self.check_for_error(response)
        return response

    def cancel(self, request_id):
        response = self._client.post(
            self._client.api_host(),
            "/verify/control/json",
            {"request_id": request_id, "cmd": "cancel"},
            **Verify.defaults,
        )

        self.check_for_error(response)
        return response

    def trigger_next_event(self, request_id):
        response = self._client.post(
            self._client.api_host(),
            "/verify/control/json",
            {"request_id": request_id, "cmd": "trigger_next_event"},
            **Verify.defaults,
        )

        self.check_for_error(response)
        return response

    def psd2(self, params=None, **kwargs):
        response = self._client.post(
            self._client.api_host(), "/verify/psd2/json", params or kwargs, **Verify.defaults,
        )

        self.check_for_error(response)
        return response

    def check_for_error(self, response):
        if response['status'] == '7':
            raise BlockedNumberError('Error code 7: The number you are trying to verify is blocked for verification.')
        elif 'error_text' in response:
            raise VerifyError(f'Verify API method failed with status: {response["status"]} and error: {response["error_text"]}')

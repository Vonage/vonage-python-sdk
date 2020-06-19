import nexmo
import warnings

class Verify:
    def __init__(
        self,
        client=None,
        key=None,
        secret=None
    ):
        try:
            self._client = client
            if self._client is None:
                self._client = nexmo.Client(
                    key=key,
                    secret=secret
                )
        except Exception as e:
            print('Error: {error_message}'.format(error_message=str(e)))
    
    def request(self, params=None, **kwargs):
        return self._client.post(self._client.api_host(), "/verify/json", params or kwargs)
    
    def send_verification_request(self, params=None, **kwargs):
        warnings.warn(
            "nexmo.Client#send_verification_request is deprecated (use #start_verification instead)",
            DeprecationWarning,
            stacklevel=2,
        )

        return self._client.post(self._client.api_host(), "/verify/json", params or kwargs)
    
    def check(self, request_id, params=None, **kwargs):
        return self._client.post(
            self._client.api_host(),
            "/verify/check/json",
            dict(params or kwargs, request_id=request_id),
        )
    
    def check_verification_request(self, params=None, **kwargs):
        warnings.warn(
            "nexmo.Client#check_verification_request is deprecated (use #check_verification instead)",
            DeprecationWarning,
            stacklevel=2,
        )

        return self._client.post(self._client.api_host(), "/verify/check/json", params or kwargs)

    def search(self, request_id):
        return self._client.get(
            self._client.api_host(), "/verify/search/json", {"request_id": request_id}
        )
    
    def get_verification_request(self, request_id):
        warnings.warn(
            "nexmo.Client#get_verification_request is deprecated (use #get_verification instead)",
            DeprecationWarning,
            stacklevel=2,
        )

        return self._client.get(
            self._client.api_host(), "/verify/search/json", {"request_id": request_id}
        )
    
    def cancel(self, request_id):
        return self._client.post(
            self._client.api_host(),
            "/verify/control/json",
            {"request_id": request_id, "cmd": "cancel"},
        )
    
    def trigger_next_event(self, request_id):
        return self._client.post(
            self._client.api_host(),
            "/verify/control/json",
            {"request_id": request_id, "cmd": "trigger_next_event"},
        )

    def control_verification_request(self, params=None, **kwargs):
        warnings.warn(
            "nexmo.Client#control_verification_request is deprecated",
            DeprecationWarning,
            stacklevel=2,
        )

        return self._client.post(self._client.api_host(), "/verify/control/json", params or kwargs)
    
    def psd2(self, params=None, **kwargs):
        return self._client.post(self._client.api_host(), "/verify/psd2/json", params or kwargs)
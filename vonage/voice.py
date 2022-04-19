import vonage

class Voice():
    #application_id and private_key are needed for the calling methods
    #Passing a Vonage Client is also possible 
    def __init__(
        self,
        client=None,
        application_id=None,
        private_key=None,
    ):
        try:
            # Client is protected
            self._client = client
            if self._client is None:
                self._client = vonage.Client(application_id=application_id, private_key=private_key)
        except Exception as e:
            print(f'Error: {str(e)}')

    # Creates a new call session
    def create_call(self, params, **kwargs):
        """
            Adding Random From Number Feature for the Voice API, 
            if set to `True`, the from number will be randomly selected 
            from the pool of numbers available to the application making 
            the call.

            :param params is a dictionry that holds the 'from' and 'random_from_number'
            
        """
        if not params:
            params = kwargs

            key = 'from'
            if key not in params:
                params['random_from_number'] = True


        return self._jwt_signed_post("/v1/calls", params or kwargs)
    
    # Get call history paginated. Pass start and end dates to filter the retrieved information
    def get_calls(self, params=None, **kwargs):
        return self._jwt_signed_get("/v1/calls", params or kwargs)
    
    # Get a single call record by identifier
    def get_call(self, uuid):
        return self._jwt_signed_get(f"/v1/calls/{uuid}")
    
    # Update call data using custom ncco
    def update_call(self, uuid, params=None, **kwargs):
        return self._jwt_signed_put(
            f"/v1/calls/{uuid}", params or kwargs
        )
    
    # Plays audio streaming into call in progress - stream_url parameter is required
    def send_audio(self, uuid, params=None, **kwargs):
        return self._jwt_signed_put(
            f"/v1/calls/{uuid}/stream", params or kwargs
        )
    
    # Play an speech into specified call - text parameter (text to speech) is required
    def send_speech(self, uuid, params=None, **kwargs):
        return self._jwt_signed_put(
            f"/v1/calls/{uuid}/talk", params or kwargs
        )
    
    # plays DTMF tones into the specified call
    def send_dtmf(self, uuid, params=None, **kwargs):
        return self._jwt_signed_put(
            f"/v1/calls/{uuid}/dtmf", params or kwargs
        )
    
    # Stops audio recently played into specified call
    def stop_audio(self, uuid):
        return self._jwt_signed_delete(f"/v1/calls/{uuid}/stream")
    
    # Stop a speech recently played into specified call
    def stop_speech(self, uuid):
        return self._jwt_signed_delete(f"/v1/calls/{uuid}/talk")
    
    # Deprecated section
    # This methods are deprecated, to use them a definition of client with key and secret parameters is mandatory
    def initiate_call(self, params=None, **kwargs):
        return self._client.post(self._client.host(), "/call/json", params or kwargs)

    def initiate_tts_call(self, params=None, **kwargs):
        return self._client.post(self._client.api_host(), "/tts/json", params or kwargs)

    def initiate_tts_prompt_call(self, params=None, **kwargs):
        return self._client.post(self._client.api_host(), "/tts-prompt/json", params or kwargs)
    # End deprecated section
    
    # Utils methods
    # _jwt_signed_post private method that Allows developer perform signed post request
    def _jwt_signed_post(self, request_uri, params):
        uri = f"https://{self._client.api_host()}{request_uri}"

        # Uses the client session to perform the call action with api
        return self._client.parse(
            self._client.api_host(), self._client.session.post(uri, json=params, headers=self._client._headers())
        )
    
    # _jwt_signed_post private method that Allows developer perform signed get request
    def _jwt_signed_get(self, request_uri, params=None):
        uri = f"https://{self._client.api_host()}{request_uri}"

        return self._client.parse(
            self._client.api_host(),
            self._client.session.get(uri, params=params or {}, headers=self._client._headers()),
        )
    
    # _jwt_signed_put private method that Allows developer perform signed put request
    def _jwt_signed_put(self, request_uri, params):
        uri = f"https://{self._client.api_host()}{request_uri}"

        return self._client.parse(
            self._client.api_host(), self._client.session.put(uri, json=params, headers=self._client._headers())
        )
    
    # _jwt_signed_put private method that Allows developer perform signed put request
    def _jwt_signed_delete(self, request_uri):
        uri = f"https://{self._client.api_host()}{request_uri}"

        return self._client.parse(
            self._client.api_host(), self._client.session.delete(uri, headers=self._client._headers())
        )

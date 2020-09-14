import vonage

class Voice():
    #application_id and private_key are needed for the calling methods
    #Passing a Nexmo Client is also possible 
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
            print('Error: {error_message}'.format(error_message=str(e)))

    # Creates a new call session
    def create_call(self, params=None, **kwargs):
        return self._jwt_signed_post("/v1/calls", params or kwargs)
    
    # Get call history paginated. Pass start and end dates to filter the retrieved information
    def get_calls(self, params=None, **kwargs):
        return self._jwt_signed_get("/v1/calls", params or kwargs)
    
    # Get a single call record by identifier
    def get_call(self, uuid):
        return self._jwt_signed_get("/v1/calls/{uuid}".format(uuid=uuid))
    
    # Update call data using custom ncco
    def update_call(self, uuid, params=None, **kwargs):
        return self._jwt_signed_put(
            "/v1/calls/{uuid}".format(uuid=uuid), params or kwargs
        )
    
    # Plays audio streaming into call in progress - stream_url parameter is required
    def send_audio(self, uuid, params=None, **kwargs):
        return self._jwt_signed_put(
            "/v1/calls/{uuid}/stream".format(uuid=uuid), params or kwargs
        )
    
    # Play an speech into specified call - text parameter (text to speech) is required
    def send_speech(self, uuid, params=None, **kwargs):
        return self._jwt_signed_put(
            "/v1/calls/{uuid}/talk".format(uuid=uuid), params or kwargs
        )
    
    # plays DTMF tones into the specified call
    def send_dtmf(self, uuid, params=None, **kwargs):
        return self._jwt_signed_put(
            "/v1/calls/{uuid}/dtmf".format(uuid=uuid), params or kwargs
        )
    
    # Stops audio recently played into specified call
    def stop_audio(self, uuid):
        return self._jwt_signed_delete("/v1/calls/{uuid}/stream".format(uuid=uuid))
    
    # Stop a speech recently played into specified call
    def stop_speech(self, uuid):
        return self._jwt_signed_delete("/v1/calls/{uuid}/talk".format(uuid=uuid))
    
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
        uri = "https://{api_host}{request_uri}".format(
            api_host=self._client.api_host(), request_uri=request_uri
        )

        # Uses the client session to perform the call action with api
        return self._client.parse(
            self._client.api_host(), self._client.session.post(uri, json=params, headers=self._client._headers())
        )
    
    # _jwt_signed_post private method that Allows developer perform signed get request
    def _jwt_signed_get(self, request_uri, params=None):
        uri = "https://{api_host}{request_uri}".format(
            api_host=self._client.api_host(), request_uri=request_uri
        )

        return self._client.parse(
            self._client.api_host(),
            self._client.session.get(uri, params=params or {}, headers=self._client._headers()),
        )
    
    # _jwt_signed_put private method that Allows developer perform signed put request
    def _jwt_signed_put(self, request_uri, params):
        uri = "https://{api_host}{request_uri}".format(
            api_host=self._client.api_host(), request_uri=request_uri
        )

        return self._client.parse(
            self._client.api_host(), self._client.session.put(uri, json=params, headers=self._client._headers())
        )
    
    # _jwt_signed_put private method that Allows developer perform signed put request
    def _jwt_signed_delete(self, request_uri):
        uri = "https://{api_host}{request_uri}".format(
            api_host=self._client.api_host(), request_uri=request_uri
        )

        return self._client.parse(
            self._client.api_host(), self._client.session.delete(uri, headers=self._client._headers())
        )

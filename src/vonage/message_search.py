import vonage

class MessageSearch:
    def __init__(
        self,
        client=None,
        key=None,
        secret=None,
        signature_secret=None,
        signature_method=None
    ):
        try:
            self._client = client
            if self._client is None:
                self._client = vonage.Client(
                    key=key,
                    secret=secret,
                    signature_secret=signature_secret,
                    signature_method=signature_method
                )
        except Exception as e:
            print(f'Error: {str(e)}')

    def get_message(self, message_id):
        return self._client.get(self._client.host(), "/search/message", {"id": message_id})

    def search_messages(self, params=None, **kwargs):
        return self._client.get(self._client.host(), "/search/messages", params or kwargs)

    def get_message_rejections(self, params=None, **kwargs):
        return self._client.get(self._client.host(), "/search/rejections", params or kwargs)

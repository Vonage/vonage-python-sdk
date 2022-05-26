class MessageSearch:
    def __init__(self, client):
        self._client = client

    def get_message(self, message_id):
        return self._client.get(self._client.host(), "/search/message", {"id": message_id})

    def search_messages(self, params=None, **kwargs):
        return self._client.get(self._client.host(), "/search/messages", params or kwargs)

    def get_message_rejections(self, params=None, **kwargs):
        return self._client.get(self._client.host(), "/search/rejections", params or kwargs)

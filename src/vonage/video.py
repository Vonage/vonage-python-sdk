class Video:
    auth_type = 'jwt'

    def __init__(self, client):
        self._client = client


    def create_session(self, params=None):
        return self._client.post(
            self._client.video_host(), 
            '/session/create', 
            params, 
            auth_type=Video.auth_type,
            body_is_json=False
        )[0]

    def get_stream(self, session_id, stream_id):
        return self._client.get(
            self._client.video_host(),
            f'/v2/project/{self._client.application_id}/session/{session_id}/stream/{stream_id}',
            auth_type=Video.auth_type
        )

    def list_streams(self, session_id):
        return self._client.get(
            self._client.video_host(),
            f'/v2/project/{self._client.application_id}/session/{session_id}/stream',
            auth_type=Video.auth_type
        )

    def set_stream_layout(self, session_id, items):
        return self._client.put(
            self._client.video_host(),
            f'/v2/project/{self._client.application_id}/session/{session_id}/stream',
            items,
            auth_type=Video.auth_type
        )

    def send_signal(self, session_id, type, data, connection_id=None):
        if connection_id:
            request_uri = f'/v2/project/{self._client.application_id}/session/{session_id}/connection/{connection_id}/signal'
        else:
            request_uri = f'/v2/project/{self._client.application_id}/session/{session_id}/signal'
        
        params = {'type': type, 'data': data}

        return self._client.post(
            self._client.video_host(),
            request_uri,
            params,
            auth_type=Video.auth_type
        )





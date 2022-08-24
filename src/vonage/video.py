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
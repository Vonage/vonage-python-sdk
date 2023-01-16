from .errors import MeetingsError


class Meetings:
    """Class containing methods used to create and manage meetings using the Meetings API."""

    _auth_type = 'jwt'
    _meetings_api_host = 'api-eu.vonage.com/beta/meetings'

    def __init__(self, client):
        self._client = client

    def list_rooms(self, start_id: str = None, end_id: str = None):
        params = {}
        if start_id is not None:
            params['start_id'] = start_id
        if end_id is not None:
            params['end_id'] = end_id

        return self._client.get(self._meetings_api_host, '/rooms', params, auth_type=Meetings._auth_type)

    def create_room(self, params: dict):
        return self._client.post(self._meetings_api_host, '/rooms', params, auth_type=Meetings._auth_type)

    def get_room_details(self, room_id: str):
        return self._client.get(self._meetings_api_host, f'/rooms/{room_id}', auth_type=Meetings._auth_type)

    def update_room(self, room_id: str, params: dict):
        return self._client.patch(self._meetings_api_host, f'/rooms/{room_id}', params, auth_type=Meetings._auth_type)

    def get_recording(self, recording_id: str):
        return self._client.get(self._meetings_api_host, f'/recordings/{recording_id}', auth_type=Meetings._auth_type)

    def delete_recording(self, recording_id: str):
        return self._client.delete(
            self._meetings_api_host, f'/recordings/{recording_id}', auth_type=Meetings._auth_type
        )

    def get_session_recordings(self, session_id: str):
        return self._client.get(
            self._meetings_api_host, f'/sessions/{session_id}/recordings', auth_type=Meetings._auth_type
        )

    def list_dial_in_numbers(self):
        return self._client.get(self._meetings_api_host, '/dial-in-numbers', auth_type=Meetings._auth_type)

    def list_themes(self):
        return self._client.get(self._meetings_api_host, '/themes', auth_type=Meetings._auth_type)

    def create_theme(self, params: dict):
        if 'main_color' not in params or 'brand_text' not in params:
            raise MeetingsError('Values for "main_color" and "brand_text" must be specified')

        return self._client.post(self._meetings_api_host, '/themes', params, auth_type=Meetings._auth_type)

    def get_theme(self, theme_id: str):
        return self._client.get(self._meetings_api_host, f'/themes/{theme_id}', auth_type=Meetings._auth_type)

    def delete_theme(self, theme_id: str):
        return self._client.delete(self._meetings_api_host, f'/themes/{theme_id}', auth_type=Meetings._auth_type)

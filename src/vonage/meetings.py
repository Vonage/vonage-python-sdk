from .errors import MeetingsError


class Meetings:
    """Class containing methods used to create and manage meetings using the Meetings API."""

    _auth_type = 'jwt'

    def __init__(self, client):
        self._client = client
        self._meetings_api_host = client.meetings_api_host()

    def list_rooms(self, start_id: str = None, end_id: str = None):
        params = Meetings.set_start_and_end_params(start_id, end_id)
        return self._client.get(self._meetings_api_host, '/rooms', params, auth_type=Meetings._auth_type)

    def create_room(self, params: dict = None):
        if 'display_name' not in params:
            raise MeetingsError('You must include a value for display_name when creating a meeting room.')
        return self._client.post(self._meetings_api_host, '/rooms', params, auth_type=Meetings._auth_type)

    def get_room(self, room_id: str):
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

    def delete_theme(self, theme_id: str, force: bool = False):
        params = {'force': force}
        return self._client.delete(
            self._meetings_api_host, f'/themes/{theme_id}', params=params, auth_type=Meetings._auth_type
        )

    def update_theme(self, theme_id: str, params: dict):
        return self._client.patch(self._meetings_api_host, f'/themes/{theme_id}', params, auth_type=Meetings._auth_type)

    def make_logo_permanent(self, theme_id: str, params: dict):
        return self._client.put(
            self._meetings_api_host, f'/themes/{theme_id}/finalizeLogos', params, auth_type=Meetings._auth_type
        )

    def list_logo_upload_urls(self):
        return self._client.get(self._meetings_api_host, '/themes/logos-upload-urls', auth_type=Meetings._auth_type)

    def list_rooms_with_theme_id(self, theme_id: str, start_id: str = None, end_id: str = None):
        params = Meetings.set_start_and_end_params(start_id, end_id)
        return self._client.get(
            self._meetings_api_host, f'/themes/{theme_id}/rooms', params, auth_type=Meetings._auth_type
        )

    def update_application_theme(self, default_theme_id: str = None):
        params = {'deafult_theme_id': default_theme_id}
        return self._client.patch(self._meetings_api_host, '/applications', params, auth_type=Meetings._auth_type)

    @staticmethod
    def set_start_and_end_params(start_id, end_id):
        params = {}
        if start_id is not None:
            params['start_id'] = start_id
        if end_id is not None:
            params['end_id'] = end_id
        return params

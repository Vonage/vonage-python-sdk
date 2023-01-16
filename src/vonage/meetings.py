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

from util import *
from vonage.errors import MeetingsError, ClientError, ServerError

import responses


@responses.activate
def test_create_instant_room(meetings, dummy_data):
    stub(responses.POST, "https://api-eu.vonage.com/beta/meetings/rooms", fixture_path='meetings/meeting_room.json')

    params = {'display_name': 'my_test_room'}
    meeting = meetings.create_room(params)

    assert isinstance(meeting, dict)
    assert request_user_agent() == dummy_data.user_agent
    assert meeting['id'] == 'b3142c46-d1c1-4405-baa6-85683827ed69'
    assert meeting['display_name'] == 'my_test_room'
    assert meeting['expires_at'] == '2023-01-24T03:30:38.629Z'


@responses.activate
def test_create_long_term_room(meetings, dummy_data):
    stub(responses.POST, "https://api-eu.vonage.com/beta/meetings/rooms", fixture_path='meetings/long_term_room.json')

    params = {'display_name': 'test_long_term_room', 'type': 'long_term', 'expires_at': '2023-01-30T00:47:04+0000'}
    meeting = meetings.create_room(params)

    assert isinstance(meeting, dict)
    assert request_user_agent() == dummy_data.user_agent
    assert meeting['id'] == '33791484-231c-421b-8349-96e1a44e27d2'
    assert meeting['display_name'] == 'test_long_term_room'
    assert meeting['expires_at'] == '2023-01-30T00:47:04.000Z'


def test_create_room_error(meetings):
    with pytest.raises(MeetingsError) as err:
        meetings.create_room()
        assert (
            str(err.value)
            == 'You must include a value for display_name as a field in the params dict when creating a meeting room.'
        )


@responses.activate
def test_get_room(meetings):
    stub(
        responses.GET,
        'https://api-eu.vonage.com/beta/meetings/rooms/b3142c46-d1c1-4405-baa6-85683827ed69',
        fixture_path='meetings/meeting_room.json',
    )
    meeting = meetings.get_room(room_id='b3142c46-d1c1-4405-baa6-85683827ed69')

    assert isinstance(meeting, dict)
    assert meeting['id'] == 'b3142c46-d1c1-4405-baa6-85683827ed69'
    assert meeting['display_name'] == 'my_test_room'
    assert meeting['expires_at'] == '2023-01-24T03:30:38.629Z'


def test_get_room_error_no_room_specified(meetings):
    with pytest.raises(TypeError):
        meetings.get_room()


@responses.activate
def test_list_rooms(meetings):
    stub(responses.GET, 'https://api-eu.vonage.com/beta/meetings/rooms', fixture_path='meetings/multiple_rooms.json')
    response = meetings.list_rooms()

    assert isinstance(response, dict)
    assert response['_embedded'][0]['id'] == '4814804d-7c2d-4846-8c7d-4f6fae1f910a'
    assert response['_embedded'][1]['id'] == 'de34416a-2a4c-4a59-a16a-8cd7d3121ea0'
    assert response['_embedded'][2]['id'] == 'd44529db-d1fa-48d5-bba0-43034bf91ae4'
    assert response['_embedded'][3]['id'] == '4f7dc750-6049-42ef-a25f-e7afa4953e32'
    assert response['_embedded'][4]['id'] == 'b3142c46-d1c1-4405-baa6-85683827ed69'
    assert response['total_items'] == 5


@responses.activate
def test_update_room(meetings):
    stub(
        responses.PATCH,
        'https://api-eu.vonage.com/beta/meetings/rooms/b3142c46-d1c1-4405-baa6-85683827ed69',
        fixture_path='meetings/update_room.json',
    )

    params = {
        'update_details': {
            "available_features": {
                "is_recording_available": False,
                "is_chat_available": False,
                "is_whiteboard_available": False,
            }
        }
    }
    meeting = meetings.update_room(room_id='b3142c46-d1c1-4405-baa6-85683827ed69', params=params)

    assert meeting['id'] == '33791484-231c-421b-8349-96e1a44e27d2'
    assert meeting['available_features']['is_recording_available'] == False
    assert meeting['available_features']['is_chat_available'] == False
    assert meeting['available_features']['is_whiteboard_available'] == False


@responses.activate
def test_update_room_error_no_room_specified(meetings):
    stub(
        responses.PATCH,
        'https://api-eu.vonage.com/beta/meetings/rooms/b3142c46-d1c1-4405-baa6-85683827ed69',
        fixture_path='meetings/update_room_type_error.json',
        status_code=400,
    )
    with pytest.raises(ClientError) as err:
        meetings.update_room(room_id='b3142c46-d1c1-4405-baa6-85683827ed69', params={})
    assert (
        str(err.value)
        == 'Status Code 400: BadRequestError: The room with id: b3142c46-d1c1-4405-baa6-85683827ed69 could not be updated because of its type: temporary'
    )


@responses.activate
def test_update_room_error_no_params_specified(meetings):
    stub(
        responses.PATCH,
        'https://api-eu.vonage.com/beta/meetings/rooms/33791484-231c-421b-8349-96e1a44e27d2',
        fixture_path='meetings/update_room_type_error.json',
        status_code=400,
    )
    with pytest.raises(TypeError) as err:
        meetings.update_room(room_id='33791484-231c-421b-8349-96e1a44e27d2')
    assert str(err.value) == "Meetings.update_room() missing 1 required positional argument: 'params'"


@responses.activate
def test_get_recording(meetings):
    stub(
        responses.GET,
        'https://api-eu.vonage.com/beta/meetings/recordings/e5b73c98-c087-4ee5-b61b-0ea08204fc65',
        fixture_path='meetings/get_recording.json',
    )

    recording = meetings.get_recording(recording_id='e5b73c98-c087-4ee5-b61b-0ea08204fc65')
    assert recording['session_id'] == '1_MX40NjMzOTg5Mn5-MTY3NDYxNDI4NjY5M35WM0xaVXBSc1lpT3hKWE1XQ2diM1B3cXB-fn4'
    assert recording['started_at'] == '2023-01-25T02:38:31.000Z'
    assert recording['status'] == 'uploaded'


@responses.activate
def test_get_recording_not_found(meetings):
    stub(
        responses.GET,
        'https://api-eu.vonage.com/beta/meetings/recordings/not-a-real-recording-id',
        fixture_path='meetings/get_recording_not_found.json',
        status_code=404,
    )

    with pytest.raises(ClientError) as err:
        meetings.get_recording(recording_id='not-a-real-recording-id')
    assert str(err.value) == 'Status Code 404: NotFoundError: Recording not-a-real-recording-id was not found'


@responses.activate
def test_delete_recording(meetings):
    stub(
        responses.DELETE,
        'https://api-eu.vonage.com/beta/meetings/recordings/e5b73c98-c087-4ee5-b61b-0ea08204fc65',
        fixture_path='meetings/delete_recording.json',
    )

    assert meetings.delete_recording(recording_id='e5b73c98-c087-4ee5-b61b-0ea08204fc65') == None


@responses.activate
def test_delete_recording_not_uploaded(meetings, client):
    stub(
        responses.DELETE,
        'https://api-eu.vonage.com/beta/meetings/recordings/881f0dbe-3d91-4fd6-aeea-0eca4209b512',
        fixture_path='meetings/delete_recording_not_found.json',
        status_code=500,
    )

    with pytest.raises(ServerError) as err:
        meetings.delete_recording(recording_id='881f0dbe-3d91-4fd6-aeea-0eca4209b512')
    assert str(err.value) == f'500 response from {client.meetings_api_host()}'


@responses.activate
def test_delete_recording_not_found(meetings):
    stub(
        responses.DELETE,
        'https://api-eu.vonage.com/beta/meetings/recordings/not-a-real-recording-id',
        fixture_path='meetings/delete_recording_not_found.json',
        status_code=404,
    )

    with pytest.raises(ClientError) as err:
        meetings.delete_recording(recording_id='not-a-real-recording-id')
    assert str(err.value) == 'Status Code 404: NotFoundError: Could not find recording'


@responses.activate
def test_get_session_recordings(meetings):
    stub(
        responses.GET,
        'https://api-eu.vonage.com/beta/meetings/sessions/1_MX40NjMzOTg5Mn5-MTY3NDYxNDI4NjY5M35WM0xaVXBSc1lpT3hKWE1XQ2diM1B3cXB-fn4/recordings',
        fixture_path='meetings/get_session_recordings.json',
    )

    session = meetings.get_session_recordings(
        session_id='1_MX40NjMzOTg5Mn5-MTY3NDYxNDI4NjY5M35WM0xaVXBSc1lpT3hKWE1XQ2diM1B3cXB-fn4'
    )
    assert session['_embedded']['recordings'][0]['id'] == 'e5b73c98-c087-4ee5-b61b-0ea08204fc65'
    assert session['_embedded']['recordings'][0]['started_at'] == '2023-01-25T02:38:31.000Z'
    assert session['_embedded']['recordings'][0]['status'] == 'uploaded'


@responses.activate
def test_get_session_recordings_not_found(meetings):
    stub(
        responses.GET,
        'https://api-eu.vonage.com/beta/meetings/sessions/not-a-real-session-id/recordings',
        fixture_path='meetings/get_session_recordings_not_found.json',
        status_code=404,
    )

    with pytest.raises(ClientError) as err:
        meetings.get_session_recordings(session_id='not-a-real-session-id')
    assert (
        str(err.value)
        == 'Status Code 404: NotFoundError: Failed to find session recordings by id: not-a-real-session-id'
    )

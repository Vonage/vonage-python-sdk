from util import *
from vonage.errors import MeetingsError, ClientError

import responses
import json
from pytest import raises


@responses.activate
def test_create_instant_room(meetings, dummy_data):
    stub(
        responses.POST,
        "https://api-eu.vonage.com/v1/meetings/rooms",
        fixture_path='meetings/meeting_room.json',
    )

    params = {'display_name': 'my_test_room'}
    meeting = meetings.create_room(params)

    assert isinstance(meeting, dict)
    assert request_user_agent() == dummy_data.user_agent
    assert meeting['id'] == 'b3142c46-d1c1-4405-baa6-85683827ed69'
    assert meeting['display_name'] == 'my_test_room'
    assert meeting['expires_at'] == '2023-01-24T03:30:38.629Z'
    assert meeting['join_approval_level'] == 'none'


def test_create_instant_room_error_expiry(meetings, dummy_data):
    params = {'display_name': 'my_test_room', 'expires_at': '2023-01-24T03:30:38.629Z'}
    with raises(MeetingsError) as err:
        meetings.create_room(params)
    assert str(err.value) == 'Cannot set "expires_at" for an instant room.'


@responses.activate
def test_create_long_term_room(meetings, dummy_data):
    stub(
        responses.POST,
        "https://api-eu.vonage.com/v1/meetings/rooms",
        fixture_path='meetings/long_term_room.json',
    )

    params = {
        'display_name': 'test_long_term_room',
        'type': 'long_term',
        'expires_at': '2023-01-30T00:47:04+0000',
    }
    meeting = meetings.create_room(params)

    assert isinstance(meeting, dict)
    assert request_user_agent() == dummy_data.user_agent
    assert meeting['id'] == '33791484-231c-421b-8349-96e1a44e27d2'
    assert meeting['display_name'] == 'test_long_term_room'
    assert meeting['expires_at'] == '2023-01-30T00:47:04.000Z'


def test_create_room_error(meetings):
    with raises(MeetingsError) as err:
        meetings.create_room()
        assert (
            str(err.value)
            == 'You must include a value for display_name as a field in the params dict when creating a meeting room.'
        )


def test_create_long_term_room_error(meetings):
    params = {
        'display_name': 'test_long_term_room',
        'type': 'long_term',
    }
    with raises(MeetingsError) as err:
        meetings.create_room(params)
    assert str(err.value) == 'You must set a value for "expires_at" for a long-term room.'


@responses.activate
def test_get_room(meetings):
    stub(
        responses.GET,
        'https://api-eu.vonage.com/v1/meetings/rooms/b3142c46-d1c1-4405-baa6-85683827ed69',
        fixture_path='meetings/meeting_room.json',
    )
    meeting = meetings.get_room(room_id='b3142c46-d1c1-4405-baa6-85683827ed69')

    assert isinstance(meeting, dict)
    assert meeting['id'] == 'b3142c46-d1c1-4405-baa6-85683827ed69'
    assert meeting['display_name'] == 'my_test_room'
    assert meeting['expires_at'] == '2023-01-24T03:30:38.629Z'
    assert meeting['join_approval_level'] == 'none'
    assert meeting['ui_settings']['language'] == 'default'
    assert meeting['available_features']['is_locale_switcher_available'] == False
    assert meeting['available_features']['is_captions_available'] == False


def test_get_room_error_no_room_specified(meetings):
    with raises(TypeError):
        meetings.get_room()


@responses.activate
def test_list_rooms(meetings):
    stub(
        responses.GET,
        'https://api-eu.vonage.com/v1/meetings/rooms',
        fixture_path='meetings/multiple_rooms.json',
    )
    response = meetings.list_rooms()

    assert isinstance(response, dict)
    assert response['_embedded'][0]['id'] == '4814804d-7c2d-4846-8c7d-4f6fae1f910a'
    assert response['_embedded'][1]['id'] == 'de34416a-2a4c-4a59-a16a-8cd7d3121ea0'
    assert response['_embedded'][2]['id'] == 'd44529db-d1fa-48d5-bba0-43034bf91ae4'
    assert response['_embedded'][3]['id'] == '4f7dc750-6049-42ef-a25f-e7afa4953e32'
    assert response['_embedded'][4]['id'] == 'b3142c46-d1c1-4405-baa6-85683827ed69'
    assert response['total_items'] == 5


@responses.activate
def test_list_rooms_with_page_size(meetings):
    stub(
        responses.GET,
        'https://api-eu.vonage.com/v1/meetings/rooms',
        fixture_path='meetings/multiple_fewer_rooms.json',
    )
    response = meetings.list_rooms(page_size=2)

    assert isinstance(response, dict)
    assert response['_embedded'][0]['id'] == '4814804d-7c2d-4846-8c7d-4f6fae1f910a'
    assert response['_embedded'][1]['id'] == 'de34416a-2a4c-4a59-a16a-8cd7d3121ea0'
    assert response['page_size'] == 2
    assert response['total_items'] == 2


@responses.activate
def test_error_unauthorized(meetings):
    stub(
        responses.GET,
        'https://api-eu.vonage.com/v1/meetings/rooms',
        fixture_path='meetings/unauthorized.json',
        status_code=401,
    )
    with raises(ClientError) as err:
        meetings.list_rooms()
    assert str(err.value) == 'Authentication failed.'


@responses.activate
def test_update_room(meetings):
    stub(
        responses.PATCH,
        'https://api-eu.vonage.com/v1/meetings/rooms/b3142c46-d1c1-4405-baa6-85683827ed69',
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
def test_add_theme_to_room(meetings):
    stub(
        responses.PATCH,
        'https://api-eu.vonage.com/v1/meetings/rooms/33791484-231c-421b-8349-96e1a44e27d2',
        fixture_path='meetings/long_term_room_with_theme.json',
    )

    meeting = meetings.add_theme_to_room(
        room_id='33791484-231c-421b-8349-96e1a44e27d2',
        theme_id='90a21428-b74a-4221-adc3-783935d654db',
    )

    assert meeting['id'] == '33791484-231c-421b-8349-96e1a44e27d2'
    assert meeting['theme_id'] == '90a21428-b74a-4221-adc3-783935d654db'


@responses.activate
def test_update_room_error_no_room_specified(meetings):
    stub(
        responses.PATCH,
        'https://api-eu.vonage.com/v1/meetings/rooms/b3142c46-d1c1-4405-baa6-85683827ed69',
        fixture_path='meetings/update_room_type_error.json',
        status_code=400,
    )
    with raises(ClientError) as err:
        meetings.update_room(room_id='b3142c46-d1c1-4405-baa6-85683827ed69', params={})
    assert (
        str(err.value)
        == 'Status Code 400: BadRequestError: The room with id: b3142c46-d1c1-4405-baa6-85683827ed69 could not be updated because of its type: temporary'
    )


@responses.activate
def test_update_room_error_no_params_specified(meetings):
    stub(
        responses.PATCH,
        'https://api-eu.vonage.com/v1/meetings/rooms/33791484-231c-421b-8349-96e1a44e27d2',
        fixture_path='meetings/update_room_type_error.json',
        status_code=400,
    )
    with raises(TypeError) as err:
        meetings.update_room(room_id='33791484-231c-421b-8349-96e1a44e27d2')
    assert "update_room() missing 1 required positional argument: 'params'" in str(err.value)


@responses.activate
def test_get_recording(meetings):
    stub(
        responses.GET,
        'https://api-eu.vonage.com/v1/meetings/recordings/e5b73c98-c087-4ee5-b61b-0ea08204fc65',
        fixture_path='meetings/get_recording.json',
    )

    recording = meetings.get_recording(recording_id='e5b73c98-c087-4ee5-b61b-0ea08204fc65')
    assert (
        recording['session_id']
        == '1_MX40NjMzOTg5Mn5-MTY3NDYxNDI4NjY5M35WM0xaVXBSc1lpT3hKWE1XQ2diM1B3cXB-fn4'
    )
    assert recording['started_at'] == '2023-01-25T02:38:31.000Z'
    assert recording['status'] == 'uploaded'


@responses.activate
def test_get_recording_not_found(meetings):
    stub(
        responses.GET,
        'https://api-eu.vonage.com/v1/meetings/recordings/not-a-real-recording-id',
        fixture_path='meetings/get_recording_not_found.json',
        status_code=404,
    )

    with raises(ClientError) as err:
        meetings.get_recording(recording_id='not-a-real-recording-id')
    assert (
        str(err.value)
        == 'Status Code 404: NotFoundError: Recording not-a-real-recording-id was not found'
    )


@responses.activate
def test_delete_recording(meetings):
    stub(
        responses.DELETE,
        'https://api-eu.vonage.com/v1/meetings/recordings/e5b73c98-c087-4ee5-b61b-0ea08204fc65',
        fixture_path='no_content.json',
    )

    assert meetings.delete_recording(recording_id='e5b73c98-c087-4ee5-b61b-0ea08204fc65') == None


@responses.activate
def test_delete_recording_not_uploaded(meetings, client):
    stub(
        responses.DELETE,
        'https://api-eu.vonage.com/v1/meetings/recordings/881f0dbe-3d91-4fd6-aeea-0eca4209b512',
        fixture_path='meetings/delete_recording_not_found.json',
        status_code=404,
    )

    with raises(ClientError) as err:
        meetings.delete_recording(recording_id='881f0dbe-3d91-4fd6-aeea-0eca4209b512')
    assert str(err.value) == 'Status Code 404: NotFoundError: Could not find recording'


@responses.activate
def test_get_session_recordings(meetings):
    stub(
        responses.GET,
        'https://api-eu.vonage.com/v1/meetings/sessions/1_MX40NjMzOTg5Mn5-MTY3NDYxNDI4NjY5M35WM0xaVXBSc1lpT3hKWE1XQ2diM1B3cXB-fn4/recordings',
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
        'https://api-eu.vonage.com/v1/meetings/sessions/not-a-real-session-id/recordings',
        fixture_path='meetings/get_session_recordings_not_found.json',
        status_code=404,
    )

    with raises(ClientError) as err:
        meetings.get_session_recordings(session_id='not-a-real-session-id')
    assert (
        str(err.value)
        == 'Status Code 404: NotFoundError: Failed to find session recordings by id: not-a-real-session-id'
    )


@responses.activate
def test_list_dial_in_numbers(meetings):
    stub(
        responses.GET,
        'https://api-eu.vonage.com/v1/meetings/dial-in-numbers',
        fixture_path='meetings/list_dial_in_numbers.json',
    )

    numbers = meetings.list_dial_in_numbers()
    assert numbers[0]['number'] == '541139862166'
    assert numbers[0]['display_name'] == 'Argentina'
    assert numbers[1]['number'] == '442381924626'
    assert numbers[1]['locale'] == 'en-GB'


@responses.activate
def test_list_themes(meetings):
    stub(
        responses.GET,
        'https://api-eu.vonage.com/v1/meetings/themes',
        fixture_path='meetings/list_themes.json',
    )

    themes = meetings.list_themes()
    assert themes[0]['theme_id'] == '1fc39568-bc50-464f-82dc-01e13bed0908'
    assert themes[0]['main_color'] == '#FF0000'
    assert themes[0]['brand_text'] == 'My Other Company'
    assert themes[1]['theme_id'] == '90a21428-b74a-4221-adc3-783935d654db'
    assert themes[1]['main_color'] == '#12f64e'
    assert themes[1]['brand_text'] == 'My Company'


@responses.activate
def test_list_themes_no_themes(meetings):
    stub(
        responses.GET,
        'https://api-eu.vonage.com/v1/meetings/themes',
        fixture_path='meetings/empty_themes.json',
    )

    assert meetings.list_themes() == {}


@responses.activate
def test_create_theme(meetings):
    stub(
        responses.POST,
        "https://api-eu.vonage.com/v1/meetings/themes",
        fixture_path='meetings/theme.json',
    )

    params = {
        'theme_name': 'my_theme',
        'main_color': '#12f64e',
        'brand_text': 'My Company',
        'short_company_url': 'my-company',
    }

    theme = meetings.create_theme(params)
    assert theme['theme_id'] == '90a21428-b74a-4221-adc3-783935d654db'
    assert theme['main_color'] == '#12f64e'
    assert theme['brand_text'] == 'My Company'
    assert theme['domain'] == 'VCP'


def test_create_theme_missing_required_params(meetings):
    with raises(MeetingsError) as err:
        meetings.create_theme({})
    assert str(err.value) == 'Values for "main_color" and "brand_text" must be specified'


@responses.activate
def test_create_theme_name_already_in_use(meetings):
    stub(
        responses.POST,
        "https://api-eu.vonage.com/v1/meetings/themes",
        fixture_path='meetings/theme_name_in_use.json',
        status_code=409,
    )

    params = {
        'theme_name': 'my_theme',
        'main_color': '#12f64e',
        'brand_text': 'My Company',
    }

    with raises(ClientError) as err:
        meetings.create_theme(params)
    assert (
        str(err.value) == 'Status Code 409: ConflictError: theme_name already exists in application'
    )


@responses.activate
def test_get_theme(meetings):
    stub(
        responses.GET,
        "https://api-eu.vonage.com/v1/meetings/themes/90a21428-b74a-4221-adc3-783935d654db",
        fixture_path='meetings/theme.json',
    )

    theme = meetings.get_theme('90a21428-b74a-4221-adc3-783935d654db')
    assert theme['main_color'] == '#12f64e'
    assert theme['brand_text'] == 'My Company'


@responses.activate
def test_get_theme_not_found(meetings):
    stub(
        responses.GET,
        "https://api-eu.vonage.com/v1/meetings/themes/90a21428-b74a-4221-adc3-783935d654dc",
        fixture_path='meetings/theme_not_found.json',
        status_code=404,
    )

    with raises(ClientError) as err:
        meetings.get_theme('90a21428-b74a-4221-adc3-783935d654dc')
    assert (
        str(err.value)
        == 'Status Code 404: NotFoundError: could not find theme 90a21428-b74a-4221-adc3-783935d654dc'
    )


@responses.activate
def test_delete_theme(meetings):
    stub(
        responses.DELETE,
        "https://api-eu.vonage.com/v1/meetings/themes/90a21428-b74a-4221-adc3-783935d654db",
        fixture_path='no_content.json',
    )

    theme = meetings.delete_theme('90a21428-b74a-4221-adc3-783935d654db')
    assert theme == None


@responses.activate
def test_delete_theme_not_found(meetings):
    stub(
        responses.DELETE,
        "https://api-eu.vonage.com/v1/meetings/themes/90a21428-b74a-4221-adc3-783935d654dc",
        fixture_path='meetings/theme_not_found.json',
        status_code=404,
    )

    with raises(ClientError) as err:
        meetings.delete_theme('90a21428-b74a-4221-adc3-783935d654dc')
    assert (
        str(err.value)
        == 'Status Code 404: NotFoundError: could not find theme 90a21428-b74a-4221-adc3-783935d654dc'
    )


@responses.activate
def test_delete_theme_in_use(meetings):
    stub(
        responses.DELETE,
        "https://api-eu.vonage.com/v1/meetings/themes/90a21428-b74a-4221-adc3-783935d654db",
        fixture_path='meetings/delete_theme_in_use.json',
        status_code=400,
    )

    with raises(ClientError) as err:
        meetings.delete_theme('90a21428-b74a-4221-adc3-783935d654db')
    assert (
        str(err.value)
        == 'Status Code 400: BadRequestError: could not delete theme\nError: Theme 90a21428-b74a-4221-adc3-783935d654db is used by 1 room'
    )


@responses.activate
def test_update_theme(meetings):
    stub(
        responses.PATCH,
        "https://api-eu.vonage.com/v1/meetings/themes/90a21428-b74a-4221-adc3-783935d654db",
        fixture_path='meetings/updated_theme.json',
    )

    params = {
        'update_details': {
            'theme_name': 'updated_theme',
            'main_color': '#FF0000',
            'brand_text': 'My Updated Company Name',
            'short_company_url': 'updated_company_url',
        }
    }

    theme = meetings.update_theme('90a21428-b74a-4221-adc3-783935d654db', params)
    assert theme['theme_id'] == '90a21428-b74a-4221-adc3-783935d654db'
    assert theme['main_color'] == '#FF0000'
    assert theme['brand_text'] == 'My Updated Company Name'
    assert theme['short_company_url'] == 'updated_company_url'


@responses.activate
def test_update_theme_no_keys(meetings):
    stub(
        responses.PATCH,
        "https://api-eu.vonage.com/v1/meetings/themes/90a21428-b74a-4221-adc3-783935d654db",
        fixture_path='meetings/update_no_keys.json',
        status_code=400,
    )

    with raises(ClientError) as err:
        meetings.update_theme('90a21428-b74a-4221-adc3-783935d654db', {'update_details': {}})
    assert (
        str(err.value)
        == 'Status Code 400: InputValidationError: "update_details" must have at least 1 key'
    )


@responses.activate
def test_update_theme_not_found(meetings):
    stub(
        responses.PATCH,
        "https://api-eu.vonage.com/v1/meetings/themes/90a21428-b74a-4221-adc3-783935d654dc",
        fixture_path='meetings/theme_not_found.json',
        status_code=404,
    )

    with raises(ClientError) as err:
        meetings.update_theme(
            '90a21428-b74a-4221-adc3-783935d654dc',
            {'update_details': {'theme_name': 'my_new_name'}},
        )
    assert (
        str(err.value)
        == 'Status Code 404: NotFoundError: could not find theme 90a21428-b74a-4221-adc3-783935d654dc'
    )


@responses.activate
def test_update_theme_name_already_exists(meetings):
    stub(
        responses.PATCH,
        'https://api-eu.vonage.com/v1/meetings/themes/90a21428-b74a-4221-adc3-783935d654db',
        fixture_path='meetings/update_theme_already_exists.json',
        status_code=409,
    )

    with raises(ClientError) as err:
        meetings.update_theme(
            '90a21428-b74a-4221-adc3-783935d654db',
            {'update_details': {'theme_name': 'my_other_theme'}},
        )
    assert (
        str(err.value) == 'Status Code 409: ConflictError: theme_name already exists in application'
    )


@responses.activate
def test_list_rooms_with_options(meetings):
    stub(
        responses.GET,
        'https://api-eu.vonage.com/v1/meetings/themes/90a21428-b74a-4221-adc3-783935d654db/rooms',
        fixture_path='meetings/list_rooms_with_theme_id.json',
    )

    rooms = meetings.list_rooms_with_theme_id(
        '90a21428-b74a-4221-adc3-783935d654db',
        page_size=5,
        start_id=0,
        end_id=99999999,
    )
    assert rooms['_embedded'][0]['id'] == '33791484-231c-421b-8349-96e1a44e27d2'
    assert rooms['_embedded'][0]['display_name'] == 'test_long_term_room'
    assert rooms['_embedded'][0]['theme_id'] == '90a21428-b74a-4221-adc3-783935d654db'
    assert rooms['page_size'] == 5
    assert (
        rooms['_links']['self']['href']
        == 'api-eu.vonage.com/meetings/rooms?page_size=20&start_id=2009870'
    )


@responses.activate
def test_list_rooms_with_theme_id_not_found(meetings):
    stub(
        responses.GET,
        'https://api-eu.vonage.com/v1/meetings/themes/90a21428-b74a-4221-adc3-783935d654dc/rooms',
        fixture_path='meetings/list_rooms_theme_id_not_found.json',
        status_code=404,
    )

    with raises(ClientError) as err:
        meetings.list_rooms_with_theme_id(
            '90a21428-b74a-4221-adc3-783935d654dc', start_id=0, end_id=99999999
        )
    assert (
        str(err.value)
        == 'Status Code 404: NotFoundError: Failed to get rooms because theme id 90a21428-b74a-4221-adc3-783935d654dc not found'
    )


@responses.activate
def test_update_application_theme(meetings):
    stub(
        responses.PATCH,
        'https://api-eu.vonage.com/v1/meetings/applications',
        fixture_path='meetings/update_application_theme.json',
    )

    response = meetings.update_application_theme(theme_id='90a21428-b74a-4221-adc3-783935d654db')
    assert response['application_id'] == 'my-application-id'
    assert response['account_id'] == 'my-account-id'
    assert response['default_theme_id'] == '90a21428-b74a-4221-adc3-783935d654db'


@responses.activate
def test_update_application_theme_bad_request(meetings):
    stub(
        responses.PATCH,
        'https://api-eu.vonage.com/v1/meetings/applications',
        fixture_path='meetings/update_application_theme_id_not_found.json',
        status_code=400,
    )

    with raises(ClientError) as err:
        meetings.update_application_theme(theme_id='not-a-real-theme-id')
    assert (
        str(err.value)
        == 'Status Code 400: BadRequestError: Failed to update application because theme id not-a-real-theme-id not found'
    )


@responses.activate
def test_upload_logo_to_theme(meetings):
    stub(
        responses.GET,
        'https://api-eu.vonage.com/v1/meetings/themes/logos-upload-urls',
        fixture_path='meetings/list_logo_upload_urls.json',
    )
    stub(
        responses.POST,
        'https://s3.amazonaws.com/roomservice-whitelabel-logos-prod',
        fixture_path='no_content.json',
        status_code=204,
    )
    stub_bytes(
        responses.PUT,
        'https://api-eu.vonage.com/v1/meetings/themes/90a21428-b74a-4221-adc3-783935d654db/finalizeLogos',
        body=b'OK',
    )

    response = meetings.upload_logo_to_theme(
        theme_id='90a21428-b74a-4221-adc3-783935d654db',
        path_to_image='tests/data/meetings/transparent_logo.png',
        logo_type='white',
    )
    assert response == 'Logo upload to theme: 90a21428-b74a-4221-adc3-783935d654db was successful.'


@responses.activate
def test_get_logo_upload_url(meetings):
    stub(
        responses.GET,
        'https://api-eu.vonage.com/v1/meetings/themes/logos-upload-urls',
        fixture_path='meetings/list_logo_upload_urls.json',
    )

    url_w = meetings._get_logo_upload_url('white')
    assert url_w['url'] == 'https://s3.amazonaws.com/roomservice-whitelabel-logos-prod'
    assert url_w['fields']['X-Amz-Credential'] == 'some-credential'
    assert (
        url_w['fields']['key']
        == 'auto-expiring-temp/logos/white/d92b31ae-fbf1-4709-a729-c0fa75368c25'
    )
    assert url_w['fields']['logoType'] == 'white'
    url_c = meetings._get_logo_upload_url('colored')
    assert (
        url_c['fields']['key']
        == 'auto-expiring-temp/logos/colored/c4e00bac-781b-4bf0-bd5f-b9ff2cbc1b6c'
    )
    assert url_c['fields']['logoType'] == 'colored'
    url_f = meetings._get_logo_upload_url('favicon')
    assert (
        url_f['fields']['key']
        == 'auto-expiring-temp/logos/favicon/d7a81477-38f7-460c-b51f-1462b8426df5'
    )
    assert url_f['fields']['logoType'] == 'favicon'

    with raises(MeetingsError) as err:
        meetings._get_logo_upload_url('not-a-valid-option')
    assert str(err.value) == 'Cannot find the upload URL for the specified logo type.'


@responses.activate
def test_upload_to_aws(meetings):
    stub(
        responses.POST,
        'https://s3.amazonaws.com/roomservice-whitelabel-logos-prod',
        fixture_path='no_content.json',
        status_code=204,
    )

    with open('tests/data/meetings/list_logo_upload_urls.json') as file:
        urls = json.load(file)
    params = urls[0]
    meetings._upload_to_aws(params, 'tests/data/meetings/transparent_logo.png')


@responses.activate
def test_upload_to_aws_error(meetings):
    stub(
        responses.POST,
        'https://s3.amazonaws.com/not-a-valid-url',
        status_code=403,
        fixture_path='meetings/upload_to_aws_error.xml',
    )

    with open('tests/data/meetings/list_logo_upload_urls.json') as file:
        urls = json.load(file)

    params = urls[0]
    params['url'] = 'https://s3.amazonaws.com/not-a-valid-url'
    with raises(MeetingsError) as err:
        meetings._upload_to_aws(params, 'tests/data/meetings/transparent_logo.png')
    assert (
        str(err.value)
        == 'Logo upload process failed. b\'<?xml version="1.0" encoding="UTF-8"?>\\\\n<Error><Code>SignatureDoesNotMatch</Code><Message>The request signature we calculated does not match the signature you provided. Check your key and signing method.</Message><AWSAccessKeyId>ASIA5NAYMMB6M7A2QEAR</AWSAccessKeyId><StringToSign></StringToSign><SignatureProvided>b2f311449e26692a174ab2c7ca2afab24bd19c509cc611a4cef7cb2c5bb2ea9a</SignatureProvided><StringToSignBytes></StringToSignBytes><RequestId>5ZS7MSFN46X89NXA</RequestId><HostId>f+HV7uSpeawLv5lFvN+QiYP6swbiTMd/XaJeVGC+/pqKHlwlgKZ6vg+qBjV/ufb1e5WS/bxBM/Y=</HostId></Error>\''
    )


@responses.activate
def test_add_logo_to_theme(meetings):
    stub_bytes(
        responses.PUT,
        'https://api-eu.vonage.com/v1/meetings/themes/90a21428-b74a-4221-adc3-783935d654db/finalizeLogos',
        body=b'OK',
    )

    response = meetings._add_logo_to_theme(
        theme_id='90a21428-b74a-4221-adc3-783935d654db',
        key='auto-expiring-temp/logos/white/d92b31ae-fbf1-4709-a729-c0fa75368c25',
    )
    assert response == b'OK'


@responses.activate
def test_add_logo_to_theme_key_error(meetings):
    stub(
        responses.PUT,
        'https://api-eu.vonage.com/v1/meetings/themes/90a21428-b74a-4221-adc3-783935d654dc/finalizeLogos',
        fixture_path='meetings/logo_key_error.json',
        status_code=400,
    )

    with raises(ClientError) as err:
        meetings._add_logo_to_theme(
            theme_id='90a21428-b74a-4221-adc3-783935d654dc',
            key='an-invalid-key',
        )
    assert (
        str(err.value)
        == "Status Code 400: BadRequestError: could not finalize logos\nError: {'logoKey': 'not-a-key', 'code': 'key_not_found'}"
    )


@responses.activate
def test_add_logo_to_theme_not_found_error(meetings):
    stub(
        responses.PUT,
        'https://api-eu.vonage.com/v1/meetings/themes/90a21428-b74a-4221-adc3-783935d654dc/finalizeLogos',
        fixture_path='meetings/theme_not_found.json',
        status_code=404,
    )

    with raises(ClientError) as err:
        meetings._add_logo_to_theme(
            theme_id='90a21428-b74a-4221-adc3-783935d654dc',
            key='auto-expiring-temp/logos/white/d92b31ae-fbf1-4709-a729-c0fa75368c25',
        )
    assert (
        str(err.value)
        == 'Status Code 404: NotFoundError: could not find theme 90a21428-b74a-4221-adc3-783935d654dc'
    )

from os.path import abspath

import responses
from vonage_http_client.errors import NotFoundError
from vonage_http_client.http_client import HttpClient
from vonage_users import Users
from vonage_users.common import *
from vonage_users.requests import ListUsersFilter

from testutils import build_response, get_mock_jwt_auth

path = abspath(__file__)

users = Users(HttpClient(get_mock_jwt_auth()))


def test_create_list_users_request():
    params = {
        'page_size': 20,
        'order': 'desc',
        'cursor': '7EjDNQrAcipmOnc0HCzpQRkhBULzY44ljGUX4lXKyUIVfiZay5pv9wg=',
        'name': 'my_user',
    }
    list_users_request = ListUsersFilter(**params)

    assert list_users_request.model_dump() == params


@responses.activate
def test_list_users():
    build_response(path, 'GET', 'https://api.nexmo.com/v1/users', 'list_users.json')
    users_list, _ = users.list_users()
    assert len(users_list) == 7
    assert users_list[0].id == 'USR-2af4d3c5-ec49-4c4a-b74c-ec13ab560af9'
    assert users_list[0].name == 'NAM-6dd4ea1f-3841-47cb-a3d3-e271f5c1e33d'
    assert users_list[3].id == 'USR-5ab17d58-b8b3-427d-ac42-c31dab7ef423'
    assert users_list[3].name == 'my_user_name'
    assert users_list[3].display_name == 'My User Name'
    assert (
        users_list[0].link
        == 'https://api-us-3.vonage.com/v1/users/USR-2af4d3c5-ec49-4c4a-b74c-ec13ab560af9'
    )
    assert (
        users_list[6].link
        == 'https://api-us-3.vonage.com/v1/users/USR-c4ef37cd-26d3-4b05-bbf3-a70d56d074e2'
    )


@responses.activate
def test_list_users_options():
    build_response(
        path, 'GET', 'https://api.nexmo.com/v1/users', 'list_users_options.json'
    )

    params = ListUsersFilter(
        page_size=2,
        order='asc',
        cursor='zAmuSchIBsUF1QaaohGdaf32NgHOkP130XeQrZkoOPEuGPnIxFb0Xj3iqCfOzxSSq9Es/S/2h+HYumKt3HS0V9ewjis+j74oMcsvYBLN1PwFEupI6ENEWHYC7lk=',
    )
    users_list, next = users.list_users(params)

    assert users_list[0].id == 'USR-37a8299f-eaad-417c-a0b3-431b6555c4be'
    assert users_list[0].name == 'my_other_user_name'
    assert users_list[0].display_name == 'My Other User Name'
    assert (
        users_list[0].link
        == 'https://api-us-3.vonage.com/v1/users/USR-37a8299f-eaad-417c-a0b3-431b6555c4be'
    )
    assert users_list[1].id == 'USR-5ab17d58-b8b3-427d-ac42-c31dab7ef422'
    assert (
        next
        == 'Rv1d7qE3lDuOuwSFjRGHJ2JpKG28CdI1iNjSKNwy0NIr7uicrn7SGpIyaDtvkEEBfyH5xyjSonpeoYNLdw19SQ=='
    )


def test_create_user_model_from_dict():
    user_dict = {
        'name': 'my_user_name',
        'display_name': 'My User Name',
        'image_url': 'https://example.com/image.jpg',
        'properties': {'custom_data': {'key': 'value'}},
        'channels': {
            'sms': [{'number': '1234567890'}],
            'mms': [{'number': '1234567890'}],
            'whatsapp': [{'number': '1234567890'}],
            'viber': [{'number': '1234567890'}],
            'messenger': [{'id': 'asdf1234'}],
            'pstn': [{'number': 1234}],
            'sip': [
                {
                    'uri': 'sip:4442138907@sip.example.com;transport=tls',
                    'username': 'My User SIP',
                    'password': 'Password',
                }
            ],
            'websocket': [
                {
                    'uri': 'wss://example.com/socket',
                    'content-type': 'audio/l16;rate=16000',
                    'headers': {'customer_id': 'ABC123'},
                }
            ],
            'vbc': [{'extension': '403'}],
        },
    }

    user = User(**user_dict)
    assert user.model_dump(by_alias=True, exclude_none=True) == user_dict


def test_create_user_model_from_models():
    user = User(
        name='my_user_name',
        display_name='My User Name',
        properties={'custom_key': 'custom_value'},
        channels=Channels(sms=[SmsChannel(number='1234567890')]),
    )
    assert user.model_dump(exclude_none=True) == {
        'name': 'my_user_name',
        'display_name': 'My User Name',
        'properties': {},
        'channels': {'sms': [{'number': '1234567890'}]},
    }


@responses.activate
def test_create_user():
    build_response(path, 'POST', 'https://api.nexmo.com/v1/users', 'user.json', 201)
    user_params = User(
        name='my_user_name',
        display_name='My User Name',
        properties={'custom_key': 'custom_value'},
        channels=Channels(sms=[SmsChannel(number='1234567890')]),
    )
    user = users.create_user(user_params)
    assert user.id == 'USR-87e3e6b0-cd7b-45ef-a0a7-bcd5566a672b'
    assert user.name == 'my_user_name'
    assert user.display_name == 'My User Name'
    assert user.channels.sms[0].number == '1234567890'
    assert (
        user.link
        == 'https://api-us-3.vonage.com/v1/users/USR-87e3e6b0-cd7b-45ef-a0a7-bcd5566a672b'
    )


@responses.activate
def test_get_user():
    build_response(
        path,
        'GET',
        'https://api.nexmo.com/v1/users/USR-87e3e6b0-cd7b-45ef-a0a7-bcd5566a672b',
        'user.json',
        200,
    )

    user = users.get_user('USR-87e3e6b0-cd7b-45ef-a0a7-bcd5566a672b')
    assert user.id == 'USR-87e3e6b0-cd7b-45ef-a0a7-bcd5566a672b'
    assert user.name == 'my_user_name'
    assert user.display_name == 'My User Name'
    assert (
        user.link
        == 'https://api-us-3.vonage.com/v1/users/USR-87e3e6b0-cd7b-45ef-a0a7-bcd5566a672b'
    )


@responses.activate
def test_get_user_not_found_error():
    build_response(
        path,
        'GET',
        'https://api.nexmo.com/v1/users/USR-87e3e6b0-cd7b-45ef-a0a7-bcd5566a672b',
        'user_not_found.json',
        404,
    )

    try:
        users.get_user('USR-87e3e6b0-cd7b-45ef-a0a7-bcd5566a672b')
    except NotFoundError as err:
        assert (
            '404 response from https://api.nexmo.com/v1/users/USR-87e3e6b0-cd7b-45ef-a0a7-bcd5566a672b.'
            in err.message
        )


@responses.activate
def test_update_user():
    build_response(
        path,
        'PATCH',
        'https://api.nexmo.com/v1/users/USR-87e3e6b0-cd7b-45ef-a0a7-bcd5566a672b',
        'updated_user.json',
        200,
    )
    user_params = User(
        name='new name!',
        display_name='My New Renamed User Name',
        properties={'custom_key': 'custom_value'},
        channels=Channels(
            sms=[SmsChannel(number='1234567890')], pstn=[PstnChannel(number=123456)]
        ),
    )
    user = users.update_user(
        id='USR-87e3e6b0-cd7b-45ef-a0a7-bcd5566a672b', params=user_params
    )
    assert user.id == 'USR-87e3e6b0-cd7b-45ef-a0a7-bcd5566a672b'
    assert user.name == 'new name!'
    assert user.display_name == 'My New Renamed User Name'
    assert user.channels.sms[0].number == '1234567890'
    assert user.channels.pstn[0].number == 123456
    assert (
        user.link
        == 'https://api-us-3.vonage.com/v1/users/USR-87e3e6b0-cd7b-45ef-a0a7-bcd5566a672b'
    )


@responses.activate
def test_update_user_not_found_error():
    build_response(
        path,
        'PATCH',
        'https://api.nexmo.com/v1/users/USR-87e3e6b0-cd7b-45ef-a0a7-bcd5566a672b',
        'user_not_found.json',
        404,
    )

    try:
        users.update_user(
            id='USR-87e3e6b0-cd7b-45ef-a0a7-bcd5566a672b',
            params=User(
                name='new name!',
                display_name='My New Renamed User Name',
                properties={'custom_key': 'custom_value'},
                channels=Channels(
                    sms=[SmsChannel(number='1234567890')],
                    pstn=[PstnChannel(number=123456)],
                ),
            ),
        )
    except NotFoundError as err:
        assert (
            '404 response from https://api.nexmo.com/v1/users/USR-87e3e6b0-cd7b-45ef-a0a7-bcd5566a672b.'
            in err.message
        )


@responses.activate
def test_delete_user():
    responses.add(
        responses.DELETE,
        'https://api.nexmo.com/v1/users/USR-87e3e6b0-cd7b-45ef-a0a7-bcd5566a672b',
        status=204,
    )
    assert users.delete_user('USR-87e3e6b0-cd7b-45ef-a0a7-bcd5566a672b') is None


def test_http_client_property():
    http_client = users.http_client
    assert isinstance(http_client, HttpClient)

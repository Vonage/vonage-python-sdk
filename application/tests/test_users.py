from os.path import abspath

import responses
from vonage_application.application import Application
from vonage_http_client.errors import NotFoundError
from vonage_http_client.http_client import HttpClient
from vonage_users.requests import ListUsersFilter

from testutils import build_response, get_mock_jwt_auth

path = abspath(__file__)

application = Application(HttpClient(get_mock_jwt_auth()))


def test_http_client_property():
    http_client = application.http_client
    assert isinstance(http_client, HttpClient)


@responses.activate
def test_list_users():
    build_response(path, 'GET', 'https://api.nexmo.com/v1/users', 'list_users.json')
    users_list, _ = users.list_users()
    assert len(users_list) == 7
    assert users_list[0].id == 'USR-2af4d3c5-ec49-4c4a-b74c-ec13ab560af9'


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
        'channels': {
            'sms': [{'number': '1234567890'}],
            'mms': [{'number': '1234567890'}],
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

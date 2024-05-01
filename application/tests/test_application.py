from os.path import abspath

import responses
from vonage_application.application import Application
from vonage_application.requests import ApplicationOptions
from vonage_http_client.http_client import HttpClient

from testutils import build_response, get_mock_api_key_auth

path = abspath(__file__)

application = Application(HttpClient(get_mock_api_key_auth()))


def test_http_client_property():
    http_client = application.http_client
    assert isinstance(http_client, HttpClient)


@responses.activate
def test_create_application_basic():
    build_response(
        path,
        'POST',
        'https://api.nexmo.com/v2/applications',
        'create_application_basic.json',
    )
    app = application.create_application(ApplicationOptions(name='My Application'))

    assert app.id == 'ba1a6aa3-8ac6-487d-ac5c-be469e77ddb7'
    assert app.name == 'My Application'
    assert (
        app.keys.public_key
        == '-----BEGIN PUBLIC KEY-----\npublic_key_info_goes_here\n-----END PUBLIC KEY-----\n'
    )
    assert app.link == '/v2/applications/ba1a6aa3-8ac6-487d-ac5c-be469e77ddb7'


@responses.activate
def test_create_application_options():
    build_response(
        path,
        'POST',
        'https://api.nexmo.com/v2/applications',
        'create_application_options.json',
    )
    app = application.create_application(
        ApplicationOptions(
            name='My Application',
            keys={'public_key': 'public_key_info_goes_here'},
        )
    )

    assert app.id == 'ba1a6aa3-8ac6-487d-ac5c-be469e77ddb7'
    assert app.name == 'My Application'


# @responses.activate
# def test_list_users_options():
#     build_response(
#         path, 'GET', 'https://api.nexmo.com/v1/users', 'list_users_options.json'
#     )

#     params = ListUsersFilter(
#         page_size=2,
#         order='asc',
#         cursor='zAmuSchIBsUF1QaaohGdaf32NgHOkP130XeQrZkoOPEuGPnIxFb0Xj3iqCfOzxSSq9Es/S/2h+HYumKt3HS0V9ewjis+j74oMcsvYBLN1PwFEupI6ENEWHYC7lk=',
#     )
#     users_list, next = users.list_users(params)

#     assert users_list[0].id == 'USR-37a8299f-eaad-417c-a0b3-431b6555c4be'
#     assert users_list[0].name == 'my_other_user_name'
#     assert users_list[0].display_name == 'My Other User Name'
#     assert (
#         users_list[0].link
#         == 'https://api-us-3.vonage.com/v1/users/USR-37a8299f-eaad-417c-a0b3-431b6555c4be'
#     )
#     assert users_list[1].id == 'USR-5ab17d58-b8b3-427d-ac42-c31dab7ef422'
#     assert (
#         next
#         == 'Rv1d7qE3lDuOuwSFjRGHJ2JpKG28CdI1iNjSKNwy0NIr7uicrn7SGpIyaDtvkEEBfyH5xyjSonpeoYNLdw19SQ=='
#     )


# def test_create_user_model_from_dict():
#     user_dict = {
#         'name': 'my_user_name',
#         'channels': {
#             'sms': [{'number': '1234567890'}],
#             'mms': [{'number': '1234567890'}],
#         },
#     }

#     user = User(**user_dict)
#     assert user.model_dump(by_alias=True, exclude_none=True) == user_dict


# def test_create_user_model_from_models():
#     user = User(
#         name='my_user_name',
#         display_name='My User Name',
#         properties={'custom_key': 'custom_value'},
#         channels=Channels(sms=[SmsChannel(number='1234567890')]),
#     )
#     assert user.model_dump(exclude_none=True) == {
#         'name': 'my_user_name',
#         'display_name': 'My User Name',
#         'properties': {},
#         'channels': {'sms': [{'number': '1234567890'}]},
#     }


# @responses.activate
# def test_get_user_not_found_error():
#     build_response(
#         path,
#         'GET',
#         'https://api.nexmo.com/v1/users/USR-87e3e6b0-cd7b-45ef-a0a7-bcd5566a672b',
#         'user_not_found.json',
#         404,
#     )

#     try:
#         users.get_user('USR-87e3e6b0-cd7b-45ef-a0a7-bcd5566a672b')
#     except NotFoundError as err:
#         assert (
#             '404 response from https://api.nexmo.com/v1/users/USR-87e3e6b0-cd7b-45ef-a0a7-bcd5566a672b.'
#             in err.message
#         )

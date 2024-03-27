from os.path import abspath

import responses
from vonage_http_client.http_client import HttpClient
from vonage_users import Users
from vonage_users.requests import ListUsersRequest

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
    list_users_request = ListUsersRequest(**params)

    assert list_users_request.model_dump() == params


@responses.activate
def test_list_users():
    build_response(path, 'GET', 'https://api.nexmo.com/v1/users', 'list_users.json')
    users_generator = users.list_users()
    print(next(users_generator))
    # for user in users_generator:
    #     print(user)
    assert 0

    # assert response.page_size == 10
    # assert response.embedded.users[0].id == 'USR-82e028d9-5201-4f1e-8188-604b2d3471fd'
    # assert response.embedded.users[0].name == 'my_user_name'
    # assert response.embedded.users[0].display_name == 'My User Name'
    # assert (
    #     response.embedded.users[0].links.self.href
    #     == 'https://api.nexmo.com/v1/users/USR-82e028d9-5201-4f1e-8188-604b2d3471fd'
    # )
    # assert (
    #     response.links.self.href
    #     == 'https://api.nexmo.com/v1/users?order=desc&page_size=10&cursor=7EjDNQrAcipmOnc0HCzpQRkhBULzY44ljGUX4lXKyUIVfiZay5pv9wg='
    # )

    # print(response.model_dump_json(indent=2))

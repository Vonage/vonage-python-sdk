from vonage import Client, Users
from util import *
from vonage.errors import UsersError, ClientError, ServerError

from pytest import raises
import responses

client = Client()
users = Users(client)
host = client.api_host()


@responses.activate
def test_list_users_basic():
    stub(
        responses.GET,
        f'https://{host}/v1/users',
        fixture_path='users/list_users_basic.json',
    )

    all_users = users.list_users()
    assert all_users['page_size'] == 10
    assert all_users['_embedded']['users'][0]['name'] == 'NAM-6dd4ea1f-3841-47cb-a3d3-e271f5c1e33c'
    assert all_users['_embedded']['users'][1]['name'] == 'NAM-ecb938f2-13e0-40c1-9d3b-b16ebb4ef3d1'
    assert all_users['_embedded']['users'][2]['name'] == 'my_user_name'


@responses.activate
def test_list_users_options():
    stub(
        responses.GET,
        f'https://{host}/v1/users',
        fixture_path='users/list_users_options.json',
    )

    all_users = users.list_users(page_size=2, order='desc')
    assert all_users['page_size'] == 2
    assert all_users['_embedded']['users'][0]['name'] == 'my_user_name'
    assert all_users['_embedded']['users'][1]['name'] == 'NAM-ecb938f2-13e0-40c1-9d3b-b16ebb4ef3d1'


def test_list_users_order_error():
    with raises(UsersError) as err:
        users.list_users(order='Why, ascending of course!')
    assert (
        str(err.value) == 'Invalid order parameter. Must be one of: "asc", "desc", "ASC", "DESC".'
    )


@responses.activate
def test_list_users_400():
    stub(
        responses.GET,
        f'https://{host}/v1/users',
        fixture_path='users/list_users_400.json',
        status_code=400,
    )

    with raises(ClientError) as err:
        users.list_users(page_size='asdf')
    assert 'Input validation failure.' in str(err.value)


@responses.activate
def test_list_users_404():
    stub(
        responses.GET,
        f'https://{host}/v1/users',
        fixture_path='users/list_users_404.json',
        status_code=404,
    )

    with raises(ClientError) as err:
        users.list_users(name='asdf')
    assert 'User does not exist, or you do not have access.' in str(err.value)


@responses.activate
def test_list_users_429():
    stub(
        responses.GET,
        f'https://{host}/v1/users',
        fixture_path='users/rate_limit.json',
        status_code=429,
    )

    with raises(ClientError) as err:
        users.list_users()
    assert 'You have exceeded your request limit. You can try again shortly.' in str(err.value)


@responses.activate
def test_list_users_500():
    stub(
        responses.GET,
        f'https://{host}/v1/users',
        fixture_path='users/list_users_500.json',
        status_code=500,
    )

    with raises(ServerError) as err:
        users.list_users()
    assert str(err.value) == '500 response from api.nexmo.com'


@responses.activate
def test_create_user_basic():
    stub(
        responses.POST,
        f'https://{host}/v1/users',
        fixture_path='users/user_basic.json',
        status_code=201,
    )

    user = users.create_user()
    assert user['id'] == 'USR-d3cc6a55-aa7b-4916-8244-2fedb554afd5'
    assert user['name'] == 'NAM-ecb938f2-13e0-40c1-9d3b-b16ebb4ef3d1'
    assert (
        user['_links']['self']['href']
        == 'https://api-us-3.vonage.com/v1/users/USR-d3cc6a55-aa7b-4916-8244-2fedb554afd5'
    )


@responses.activate
def test_create_user_options():
    stub(
        responses.POST,
        f'https://{host}/v1/users',
        fixture_path='users/user_options.json',
        status_code=201,
    )

    params = {
        "id": "USR-5ab17d58-b8b3-427d-ac42-c31dab7ef422",
        "name": "my_user_name",
        "image_url": "https://example.com/image.png",
        "display_name": "My User Name",
        "properties": {"custom_data": {"custom_key": "custom_value"}},
        "_links": {
            "self": {
                "href": "https://api-us-3.vonage.com/v1/users/USR-5ab17d58-b8b3-427d-ac42-c31dab7ef422"
            }
        },
        "channels": {
            "pstn": [{"number": 123457}],
            "sip": [
                {
                    "uri": "sip:4442138907@sip.example.com;transport=tls",
                    "username": "New SIP",
                    "password": "Password",
                }
            ],
            "vbc": [{"extension": "403"}],
            "websocket": [
                {
                    "uri": "wss://example.com/socket",
                    "content-type": "audio/l16;rate=16000",
                    "headers": {"customer_id": "ABC123"},
                }
            ],
            "sms": [{"number": "447700900000"}],
            "mms": [{"number": "447700900000"}],
            "whatsapp": [{"number": "447700900000"}],
            "viber": [{"number": "447700900000"}],
            "messenger": [{"id": "12345abcd"}],
        },
    }

    user = users.create_user(params)
    assert user['id'] == 'USR-5ab17d58-b8b3-427d-ac42-c31dab7ef422'
    assert user['name'] == 'my_user_name'
    assert user['display_name'] == 'My User Name'
    assert user['properties']['custom_data']['custom_key'] == 'custom_value'
    assert (
        user['_links']['self']['href']
        == 'https://api-us-3.vonage.com/v1/users/USR-5ab17d58-b8b3-427d-ac42-c31dab7ef422'
    )
    assert user['channels']['vbc'][0]['extension'] == '403'


@responses.activate
def test_create_user_400():
    stub(
        responses.POST,
        f'https://{host}/v1/users',
        fixture_path='users/user_400.json',
        status_code=400,
    )

    with raises(ClientError) as err:
        users.create_user(params={'name': 1234})
    assert 'Input validation failure.' in str(err.value)


@responses.activate
def test_create_user_429():
    stub(
        responses.POST,
        f'https://{host}/v1/users',
        fixture_path='users/rate_limit.json',
        status_code=429,
    )

    with raises(ClientError) as err:
        users.create_user()
    assert 'You have exceeded your request limit. You can try again shortly.' in str(err.value)


@responses.activate
def test_get_user():
    user_id = 'USR-d3cc6a55-aa7b-4916-8244-2fedb554afd5'
    stub(
        responses.GET,
        f'https://{host}/v1/users/{user_id}',
        fixture_path='users/user_basic.json',
    )

    user = users.get_user(user_id)
    assert user['name'] == 'NAM-ecb938f2-13e0-40c1-9d3b-b16ebb4ef3d1'
    assert user['properties']['custom_data'] == {}
    assert (
        user['_links']['self']['href']
        == 'https://api-us-3.vonage.com/v1/users/USR-d3cc6a55-aa7b-4916-8244-2fedb554afd5'
    )


@responses.activate
def test_get_user_404():
    user_id = 'USR-d3cc6a55-aa7b-4916-8244-2fedb554afd5'
    stub(
        responses.GET,
        f'https://{host}/v1/users/{user_id}',
        status_code=404,
        fixture_path='users/user_404.json',
    )

    with raises(ClientError) as err:
        users.get_user(user_id)
    assert 'User does not exist, or you do not have access.' in str(err.value)


@responses.activate
def test_get_user_429():
    user_id = 'USR-d3cc6a55-aa7b-4916-8244-2fedb554afd5'
    stub(
        responses.GET,
        f'https://{host}/v1/users/{user_id}',
        fixture_path='users/rate_limit.json',
        status_code=429,
    )

    with raises(ClientError) as err:
        users.get_user(user_id)
    assert 'You have exceeded your request limit. You can try again shortly.' in str(err.value)


@responses.activate
def test_update_user():
    user_id = 'USR-d3cc6a55-aa7b-4916-8244-2fedb554afd5'
    stub(
        responses.PATCH,
        f'https://{host}/v1/users/{user_id}',
        fixture_path='users/user_updated.json',
    )

    params = {
        'name': 'updated_name',
        'channels': {
            'whatsapp': [
                {'number': '447700900000'},
            ]
        },
    }
    user = users.update_user(user_id, params)
    assert user['name'] == 'updated_name'
    assert (
        user['_links']['self']['href']
        == 'https://api-us-3.vonage.com/v1/users/USR-d3cc6a55-aa7b-4916-8244-2fedb554afd5'
    )
    assert user['channels']['whatsapp'][0]['number'] == '447700900000'


@responses.activate
def test_update_user_400():
    user_id = 'USR-d3cc6a55-aa7b-4916-8244-2fedb554afd5'
    stub(
        responses.PATCH,
        f'https://{host}/v1/users/{user_id}',
        fixture_path='users/user_400.json',
        status_code=400,
    )

    with raises(ClientError) as err:
        users.update_user(user_id, params={'name': 1234})
    assert 'Input validation failure.' in str(err.value)


@responses.activate
def test_update_user_404():
    user_id = 'USR-d3cc6a55-aa7b-4916-8244-2fedb554afd5'
    stub(
        responses.PATCH,
        f'https://{host}/v1/users/{user_id}',
        status_code=404,
        fixture_path='users/user_404.json',
    )

    with raises(ClientError) as err:
        users.update_user(user_id, params={'name': 'updated_user_name'})
    assert 'User does not exist, or you do not have access.' in str(err.value)


@responses.activate
def test_update_user_429():
    user_id = 'USR-d3cc6a55-aa7b-4916-8244-2fedb554afd5'
    stub(
        responses.PATCH,
        f'https://{host}/v1/users/{user_id}',
        fixture_path='users/rate_limit.json',
        status_code=429,
    )

    with raises(ClientError) as err:
        users.update_user(user_id, params={'name': 'updated_user_name'})
    assert 'You have exceeded your request limit. You can try again shortly.' in str(err.value)


@responses.activate
def test_delete_user():
    user_id = 'USR-d3cc6a55-aa7b-4916-8244-2fedb554afd5'
    stub(
        responses.DELETE,
        f'https://{host}/v1/users/{user_id}',
        status_code=204,
        fixture_path='no_content.json',
    )

    response = users.delete_user(user_id)
    assert response == None


@responses.activate
def test_delete_user_404():
    user_id = 'USR-d3cc6a55-aa7b-4916-8244-2fedb554afd5'
    stub(
        responses.DELETE,
        f'https://{host}/v1/users/{user_id}',
        status_code=404,
        fixture_path='users/user_404.json',
    )

    with raises(ClientError) as err:
        users.delete_user(user_id)
    assert 'User does not exist, or you do not have access.' in str(err.value)


@responses.activate
def test_delete_user_429():
    user_id = 'USR-d3cc6a55-aa7b-4916-8244-2fedb554afd5'
    stub(
        responses.DELETE,
        f'https://{host}/v1/users/{user_id}',
        fixture_path='users/rate_limit.json',
        status_code=429,
    )

    with raises(ClientError) as err:
        users.delete_user(user_id)
    assert 'You have exceeded your request limit. You can try again shortly.' in str(err.value)

from json import loads
from os.path import abspath, dirname, join

import responses
from pytest import raises
from requests import Response
from vonage_http_client.auth import Auth
from vonage_http_client.errors import (
    AuthenticationError,
    HttpRequestError,
    InvalidHttpClientOptionsError,
    RateLimitedError,
    ServerError,
)
from vonage_http_client.http_client import HttpClient

from testutils import build_response

path = abspath(__file__)


def read_file(path):
    with open(join(dirname(__file__), path)) as input_file:
        return input_file.read()


application_id = 'asdfzxcv'
private_key = read_file('data/dummy_private_key.txt')


def test_create_http_client():
    client = HttpClient(Auth())
    assert type(client) == HttpClient
    assert client.api_host == 'api.nexmo.com'
    assert client.rest_host == 'rest.nexmo.com'


def test_create_http_client_options():
    client_options = {
        'api_host': 'api.nexmo.com',
        'rest_host': 'rest.nexmo.com',
        'timeout': 30,
        'pool_connections': 5,
        'pool_maxsize': 12,
        'max_retries': 5,
    }
    client = HttpClient(Auth(), client_options)
    assert client.http_client_options.model_dump() == client_options


def test_create_http_client_invalid_options_error():
    with raises(InvalidHttpClientOptionsError):
        HttpClient(Auth(), [])


@responses.activate
def test_make_get_request():
    build_response(path, 'GET', 'https://example.com/get_json', 'example_get.json')
    client = HttpClient(
        Auth(application_id=application_id, private_key=private_key),
        http_client_options={'api_host': 'example.com'},
    )
    res = client.get(host='example.com', request_path='/get_json')

    assert res['hello'] == 'world'
    assert responses.calls[0].request.headers['User-Agent'] == client._user_agent


@responses.activate
def test_make_get_request_no_content():
    build_response(path, 'GET', 'https://example.com/get_json', status_code=204)
    client = HttpClient(
        Auth('asdfqwer', 'asdfqwer1234'),
        http_client_options={'api_host': 'example.com'},
    )
    res = client.get(host='example.com', request_path='/get_json', auth_type='basic')
    assert res == None


@responses.activate
def test_make_post_request():
    build_response(path, 'POST', 'https://example.com/post_json', 'example_post.json')
    client = HttpClient(
        Auth(application_id=application_id, private_key=private_key),
        http_client_options={'api_host': 'example.com'},
    )
    params = {
        'test': 'post request',
        'testing': 'http client',
    }

    res = client.post(host='example.com', request_path='/post_json', params=params)
    assert res['hello'] == 'world!'

    assert loads(responses.calls[0].request.body) == params


@responses.activate
def test_make_post_request_with_signature():
    build_response(
        path, 'POST', 'https://example.com/post_signed_params', 'example_post.json'
    )
    client = HttpClient(
        Auth(
            api_key='asdfzxcv', signature_secret='qwerasdfzxcv', signature_method='sha256'
        ),
        http_client_options={'api_host': 'example.com'},
    )
    params = {
        'test': 'post request',
        'testing': 'http client',
    }

    res = client.post(
        host='example.com',
        request_path='/post_signed_params',
        params=params,
        auth_type='signature',
    )
    assert res['hello'] == 'world!'

    assert loads(responses.calls[0].request.body) == params


@responses.activate
def test_http_response_general_error():
    build_response(path, 'GET', 'https://example.com/get_json', '400.json', 400)

    client = HttpClient(Auth())
    try:
        client.get(host='example.com', request_path='/get_json', auth_type='basic')
    except HttpRequestError as err:
        assert err.response.json()['Error'] == 'Bad Request'
        assert '400 response from https://example.com/get_json.' in err.message


@responses.activate
def test_http_response_general_text_error():
    build_response(path, 'GET', 'https://example.com/get', '400.txt', 400, 'text/plain')

    client = HttpClient(Auth())
    try:
        client.get(host='example.com', request_path='/get', auth_type='basic')
    except HttpRequestError as err:
        assert err.response.text == 'Error: Bad Request'
        assert '400 response from https://example.com/get.' in err.message


@responses.activate
def test_authentication_error():
    build_response(path, 'GET', 'https://example.com/get_json', '401.json', 401)

    client = HttpClient(Auth(application_id=application_id, private_key=private_key))
    try:
        client.get(host='example.com', request_path='/get_json')
    except AuthenticationError as err:
        assert err.response.json()['title'] == 'Unauthorized'


@responses.activate
def test_authentication_error_no_content():
    build_response(path, 'GET', 'https://example.com/get_json', status_code=401)

    client = HttpClient(Auth())
    try:
        client.get(host='example.com', request_path='/get_json', auth_type='basic')
    except AuthenticationError as err:
        assert type(err.response) == Response


@responses.activate
def test_rate_limited_error():
    build_response(path, 'GET', 'https://example.com/get_json', '429.json', 429)

    client = HttpClient(Auth())
    try:
        client.get(host='example.com', request_path='/get_json', auth_type='basic')
    except RateLimitedError as err:
        assert err.response.json()['title'] == 'Rate Limit Hit'


@responses.activate
def test_server_error():
    build_response(path, 'GET', 'https://example.com/get_json', '500.json', 500)

    client = HttpClient(Auth(application_id=application_id, private_key=private_key))
    try:
        client.get(host='example.com', request_path='/get_json')
    except ServerError as err:
        assert err.response.json()['title'] == 'Internal Server Error'


def test_append_to_user_agent():
    client = HttpClient(Auth())
    client.append_to_user_agent('TestAgent')
    assert 'TestAgent' in client.user_agent

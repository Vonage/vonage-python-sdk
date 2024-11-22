from json import loads
from os.path import abspath, dirname, join

import responses
from pytest import raises
from requests import PreparedRequest, Response
from responses import matchers
from vonage_http_client.auth import Auth
from vonage_http_client.errors import (
    AuthenticationError,
    FileStreamingError,
    ForbiddenError,
    HttpRequestError,
    InvalidHttpClientOptionsError,
    RateLimitedError,
    ServerError,
)
from vonage_http_client.http_client import HttpClient

from testutils import build_response, get_mock_jwt_auth

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
        'video_host': 'video.api.vonage.com',
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
def test_make_get_request_and_last_request_and_response():
    build_response(
        path, 'GET', 'https://example.com/get_json?key=value', 'example_get.json'
    )
    client = HttpClient(
        Auth(application_id=application_id, private_key=private_key),
        http_client_options={'api_host': 'example.com'},
    )
    res = client.get(
        host='example.com', request_path='/get_json', params={'key': 'value'}
    )

    assert res['hello'] == 'world'
    assert responses.calls[0].request.headers['User-Agent'] == client._user_agent

    assert type(client.last_request) == PreparedRequest
    assert client.last_request.method == 'GET'
    assert client.last_request.url == 'https://example.com/get_json?key=value'
    assert client.last_request.body == None

    assert type(client.last_response) == Response
    assert client.last_response.status_code == 200
    assert client.last_response.json() == res
    assert client.last_response.headers == {'Content-Type': 'application/json'}


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
    params = {
        'test': 'post request',
        'testing': 'http client',
        'timestamp': '1234567890',
    }

    build_response(
        path,
        'POST',
        'https://example.com/post_signed_params',
        'example_post.json',
        match=[
            matchers.urlencoded_params_matcher(
                {
                    **params,
                    'api_key': 'asdfzxcv',
                    'sig': '237b06fd1f994a9ec2f3283a4a0239f35b56d64639d6485b45cffedcb385b033',
                }
            )
        ],
    )
    client = HttpClient(
        Auth(
            api_key='asdfzxcv', signature_secret='qwerasdfzxcv', signature_method='sha256'
        ),
        http_client_options={'api_host': 'example.com'},
    )

    res = client.post(
        host='example.com',
        request_path='/post_signed_params',
        params=params,
        auth_type='signature',
        sent_data_type='form',
    )
    assert res['hello'] == 'world!'


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
def test_forbidden_error():
    build_response(path, 'GET', 'https://example.com/get_json', '403.json', 403)

    client = HttpClient(Auth())
    try:
        client.get(host='example.com', request_path='/get_json', auth_type='basic')
    except ForbiddenError as err:
        assert err.response.json()['title'] == 'Forbidden'
        assert (
            err.response.json()['detail']
            == 'Your account does not have permission to perform this action.'
        )


@responses.activate
def test_not_found_error():
    build_response(path, 'GET', 'https://example.com/get_json', '404.json', 404)

    client = HttpClient(Auth())
    try:
        client.get(host='example.com', request_path='/get_json', auth_type='basic')
    except HttpRequestError as err:
        assert err.response.json()['title'] == 'Not found.'


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


@responses.activate
def test_download_file_stream():
    build_response(
        path,
        'GET',
        'https://api.nexmo.com/v1/files/aaaaaaaa-bbbb-cccc-dddd-0123456789ab',
        'file_stream.mp3',
    )

    client = HttpClient(get_mock_jwt_auth())
    client.download_file_stream(
        url='https://api.nexmo.com/v1/files/aaaaaaaa-bbbb-cccc-dddd-0123456789ab',
        file_path='file.mp3',
    )

    with open('file.mp3', 'rb') as file:
        file_content = file.read()
        assert file_content.startswith(b'ID3')


@responses.activate
def test_download_file_stream_error():
    build_response(
        path,
        'GET',
        'https://api.nexmo.com/v1/files/aaaaaaaa-bbbb-cccc-dddd-0123456789ab',
        status_code=400,
    )

    client = HttpClient(get_mock_jwt_auth())
    try:
        client.download_file_stream(
            url='https://api.nexmo.com/v1/files/aaaaaaaa-bbbb-cccc-dddd-0123456789ab',
            file_path='file.mp3',
        )
    except FileStreamingError as err:
        assert '400 response from' in err.message
        assert err.response.status_code == 400
        assert err.response.json()['title'] == 'Bad Request'

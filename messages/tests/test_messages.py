from os.path import abspath

import responses
from pytest import raises
from vonage_http_client.errors import HttpRequestError
from vonage_http_client.http_client import HttpClient, HttpClientOptions
from vonage_messages.messages import Messages
from vonage_messages.models import Sms
from vonage_messages.models.messenger import (
    MessengerImage,
    MessengerOptions,
    MessengerResource,
)
from vonage_messages.responses import SendMessageResponse

from testutils import build_response, get_mock_jwt_auth

path = abspath(__file__)


messages = Messages(HttpClient(get_mock_jwt_auth()))


@responses.activate
def test_send_message():
    build_response(
        path, 'POST', 'https://api.nexmo.com/v1/messages', 'send_message.json', 202
    )
    sms = Sms(
        from_='Vonage APIs',
        to='1234567890',
        text='Hello, World!',
    )
    response = messages.send(sms)
    assert type(response) == SendMessageResponse
    assert response.message_uuid == 'd8f86df1-dec6-442f-870a-2241be27d721'


@responses.activate
def test_send_message_low_balance_error():
    build_response(
        path,
        'POST',
        'https://api.nexmo.com/v1/messages',
        'low_balance_error.json',
        402,
    )

    with raises(HttpRequestError) as e:
        messages.send(Sms(from_='Vonage APIs', to='1234567890', text='Hello, World!'))

    assert e.value.response.status_code == 402
    assert e.value.response.json()['title'] == 'Low balance'


@responses.activate
def test_send_message_invalid_error():
    build_response(
        path,
        'POST',
        'https://api.nexmo.com/v1/messages',
        'invalid_error.json',
        422,
    )

    messenger = MessengerImage(
        to='1234567890',
        from_='1234567890',
        image=MessengerResource(url='https://example.com/image.jpg'),
        messenger=MessengerOptions(category='message_tag', tag='invalid_tag'),
    )

    with raises(HttpRequestError) as e:
        messages.send(messenger)

    assert e.value.response.status_code == 422
    assert e.value.response.json()['title'] == 'Invalid params'


def test_http_client_property():
    http_client = HttpClient(get_mock_jwt_auth())
    messages = Messages(http_client)
    assert messages.http_client == http_client


@responses.activate
def test_mark_whatsapp_message_read():
    responses.add(
        responses.PATCH,
        'https://api-eu.vonage.com/v1/messages/1234567890',
    )
    messages = Messages(
        HttpClient(get_mock_jwt_auth(), HttpClientOptions(api_host='api-eu.vonage.com'))
    )
    messages.http_client.http_client_options.api_host = 'api-eu.vonage.com'
    messages.mark_whatsapp_message_read('1234567890')


@responses.activate
def test_mark_whatsapp_message_read_not_found():
    build_response(
        path,
        'PATCH',
        'https://api-eu.vonage.com/v1/messages/asdf',
        'not_found.json',
        404,
    )
    messages = Messages(
        HttpClient(get_mock_jwt_auth(), HttpClientOptions(api_host='api-eu.vonage.com'))
    )
    with raises(HttpRequestError) as e:
        messages.mark_whatsapp_message_read('asdf')

    assert e.value.response.status_code == 404
    assert e.value.response.json()['title'] == 'Not Found'


@responses.activate
def test_revoke_rcs_message():
    responses.add(
        responses.PATCH,
        'https://api-eu.vonage.com/v1/messages/asdf',
    )
    messages = Messages(
        HttpClient(get_mock_jwt_auth(), HttpClientOptions(api_host='api-eu.vonage.com'))
    )
    messages.http_client.http_client_options.api_host = 'api-eu.vonage.com'
    messages.revoke_rcs_message('asdf')


@responses.activate
def test_revoke_rcs_message_not_found():
    build_response(
        path,
        'PATCH',
        'https://api-eu.vonage.com/v1/messages/asdf',
        'not_found.json',
        404,
    )
    messages = Messages(
        HttpClient(get_mock_jwt_auth(), HttpClientOptions(api_host='api-eu.vonage.com'))
    )
    with raises(HttpRequestError) as e:
        messages.revoke_rcs_message('asdf')

    assert e.value.response.status_code == 404
    assert e.value.response.json()['title'] == 'Not Found'

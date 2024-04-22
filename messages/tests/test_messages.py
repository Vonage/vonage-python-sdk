from os.path import abspath

import responses
from pytest import raises
from vonage_http_client.errors import HttpRequestError
from vonage_http_client.http_client import HttpClient
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

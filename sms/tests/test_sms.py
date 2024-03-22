from os.path import abspath

from pydantic import ValidationError
from pytest import raises
import responses

from testutils import build_response
from vonage_http_client.auth import Auth
from vonage_http_client.http_client import HttpClient
from vonage_sms import Sms
from vonage_sms.models import SmsMessage


path = abspath(__file__)

api_key = 'qwerasdf'
api_secret = '1234qwerasdfzxcv'
signature_secret = 'signature_secret'
signature_method = 'sha256'

sms = Sms(HttpClient(Auth(api_key=api_key, api_secret=api_secret)))


def test_create_valid_SmsMessage():
    valid_message = {
        'to': '1234567890',
        'from_': 'Acme Inc.',
        'text': 'Hello, World!',
    }
    SmsMessage(**valid_message)

    valid_message = {
        'to': '1234567890',
        'from_': 'Acme Inc.',
        'text': 'Hello, World!',
        'sig': 'asdfqwerzxcv12345678',
        'client_ref': 'ref123',
        'type': 'binary',
        'ttl': 3000000,
        'status_report_req': True,
        'callback': 'https://example.com/callback',
        'message_class': 0,
        'body': 'some binary data',
        'udh': 'udh123',
        'protocol_id': 127,
        'account_ref': 'account123',
        'entity_id': 'entity123',
        'content_id': 'content123',
    }
    SmsMessage(**valid_message)


def test_create_invalid_SmsMessage():
    # Missing required fields
    invalid_message = {'to': '1234567890', 'text': 'Hello, World!'}
    with raises(ValidationError):
        SmsMessage(**invalid_message)

    # Invalid body for non-binary type
    invalid_message = {
        'to': '1234567890',
        'from_': 'Acme Inc.',
        'text': 'Hello, World!',
        'type': 'text',
        'body': 'binary data',
    }
    with raises(ValidationError):
        SmsMessage(**invalid_message)

    # Missing body and udh for binary type
    invalid_message = {
        'to': '1234567890',
        'from_': 'Acme Inc.',
        'text': 'Hello, World!',
        'type': 'binary',
    }
    with raises(ValidationError):
        SmsMessage(**invalid_message)


# @responses.activate
def test_send_message():
    sms = Sms(HttpClient(Auth(api_key='', api_secret='')))
    build_response(path, 'POST', 'https://rest.nexmo.com/sms/json', 'send_sms.json')
    message = SmsMessage(to='', from_='Acme Inc.', text='Hello, World!')
    response = sms.send(message)
    print(response)
    assert response.message_count == 1
    assert response.messages[0].status == '0'

    # assert response.status == '0'
    # assert response.to == '1234567890'
    # assert response.message_id
    # assert response.remaining_balance
    # assert response.message_price
    # assert response.network

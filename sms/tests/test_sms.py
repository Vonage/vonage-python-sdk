from os.path import abspath

import responses
from pydantic import ValidationError
from pytest import raises
from vonage_http_client.auth import Auth
from vonage_http_client.errors import HttpRequestError
from vonage_http_client.http_client import HttpClient
from vonage_sms import Sms
from vonage_sms.errors import PartialFailureError, SmsError
from vonage_sms.requests import SmsMessage

from testutils import build_response

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
        'trusted_sender': True,
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


@responses.activate
def test_send_message():
    build_response(path, 'POST', 'https://rest.nexmo.com/sms/json', 'send_sms.json')
    message = SmsMessage(to='1234567890', from_='Acme Inc.', text='Hello, World!')
    response = sms.send(message)
    assert response.message_count == '1'
    assert response.messages[0].to == '1234567890'
    assert response.messages[0].message_id == '3295d748-4e14-4681-af78-166dca3c5aab'
    assert response.messages[0].status == '0'
    assert response.messages[0].remaining_balance == '38.07243628'
    assert response.messages[0].message_price == '0.04120000'
    assert response.messages[0].network == '23420'


@responses.activate
def test_send_long_message():
    build_response(path, 'POST', 'https://rest.nexmo.com/sms/json', 'send_long_sms.json')
    message = SmsMessage(to='1234567890', from_='Acme Inc.', text='Hello, World!')
    response = sms.send(message)
    assert response.message_count == '2'
    assert response.messages[0].message_id == '62dfdf68-6c7c-479a-a190-5c52f798a787'
    assert response.messages[1].message_id == '72ff9536-62d6-455a-9f0b-65f3c265b423'


@responses.activate
def test_send_message_with_signature():
    sms = Sms(
        HttpClient(
            Auth(
                api_key=api_key,
                signature_secret=signature_secret,
                signature_method=signature_method,
            )
        )
    )
    build_response(path, 'POST', 'https://rest.nexmo.com/sms/json', 'send_sms.json')
    message = SmsMessage(to='1234567890', from_='Acme Inc.', text='Hello, World!')
    response = sms.send(message)
    assert response.message_count == '1'
    assert response.messages[0].status == '0'


@responses.activate
def test_send_message_partial_failure():
    build_response(
        path, 'POST', 'https://rest.nexmo.com/sms/json', 'send_sms_partial_error.json'
    )
    message = SmsMessage(to='1234567890', from_='Acme Inc.', text='Hello, World!')
    try:
        sms.send(message)
    except PartialFailureError as err:
        assert err.response['message-count'] == '2'
        assert err.response['messages'][1]['error-text'] == 'Throttled'


@responses.activate
def test_send_message_error():
    build_response(path, 'POST', 'https://rest.nexmo.com/sms/json', 'send_sms_error.json')
    message = SmsMessage(to='1234567890', from_='Acme Inc.', text='Hello, World!')
    try:
        sms.send(message)
    except SmsError as err:
        assert (
            str(err) == 'Sms.send_message method failed with error code 7: Number barred.'
        )


@responses.activate
def test_submit_sms_conversion():
    build_response(
        path,
        'POST',
        'https://api.nexmo.com/conversions/sms',
        'null',
    )
    response = sms.submit_sms_conversion('3295d748-4e14-4681-af78-166dca3c5aab')
    assert response is None


@responses.activate
def test_submit_sms_conversion_402():
    build_response(
        path,
        'POST',
        'https://api.nexmo.com/conversions/sms',
        'conversion_not_enabled.html',
        status_code=402,
    )
    try:
        sms.submit_sms_conversion('3295d748-4e14-4681-af78-166dca3c5aab')
    except HttpRequestError as err:
        assert '402 response from https://api.nexmo.com/conversions/sms.' in err.message


def test_http_client_property():
    sms = Sms(HttpClient(Auth(api_key='qwerasdf', api_secret='1234qwerasdfzxcv')))
    assert isinstance(sms.http_client, HttpClient)

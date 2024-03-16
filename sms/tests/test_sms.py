from os.path import abspath

from pydantic import ValidationError
from pytest import raises
from vonage_http_client.auth import Auth
from vonage_http_client.http_client import HttpClient
from vonage_sms.sms import Sms, SmsMessage

path = abspath(__file__)

sms = Sms(HttpClient(Auth('key', 'secret')))


# def test_fraud_check_request_invalid_phone():
#     with raises(InvalidPhoneNumberError):
#         FraudCheckRequest(phone='invalid_phone')
#     with raises(InvalidPhoneNumberError):
#         FraudCheckRequest(phone='123')
#     with raises(InvalidPhoneNumberError):
#         FraudCheckRequest(phone='12345678901234567890')


# def test_fraud_check_request_invalid_insights():
#     with raises(ValidationError):
#         FraudCheckRequest(phone='1234567890', insights=['invalid_insight'])


# @responses.activate
# def test_ni2_defaults():
#     build_response(path, 'POST', 'https://api.nexmo.com/v2/ni', 'default.json')
#     request = FraudCheckRequest(phone='1234567890')
#     response = ni2.fraud_check(request)
#     assert type(response) == FraudCheckResponse
#     assert response.request_id == '2c2f5d3f-93ac-42b1-9083-4b14f0d583d3'
#     assert response.phone.carrier == 'Verizon Wireless'
#     assert response.fraud_score.risk_score == '0'
#     assert response.sim_swap.status == 'completed'


# @responses.activate
# def test_ni2_fraud_score_only():
#     build_response(path, 'POST', 'https://api.nexmo.com/v2/ni', 'fraud_score.json')
#     request = FraudCheckRequest(phone='1234567890', insights=['fraud_score'])
#     response = ni2.fraud_check(request)
#     assert type(response) == FraudCheckResponse
#     assert response.request_id == '2c2f5d3f-93ac-42b1-9083-4b14f0d583d3'
#     assert response.phone.carrier == 'Verizon Wireless'
#     assert response.fraud_score.risk_score == '0'
#     assert response.sim_swap is None

#     clear_response = asdict(response, dict_factory=remove_none_values)
#     print(clear_response)
#     assert 'fraud_score' in clear_response
#     assert 'sim_swap' not in clear_response


# @responses.activate
# def test_ni2_sim_swap_only():
#     build_response(path, 'POST', 'https://api.nexmo.com/v2/ni', 'sim_swap.json')
#     request = FraudCheckRequest(phone='1234567890', insights='sim_swap')
#     response = ni2.fraud_check(request)
#     assert type(response) == FraudCheckResponse
#     assert response.request_id == 'db5282b6-8046-4217-9c0e-d9c55d8696e9'
#     assert response.phone.phone == '1234567890'
#     assert response.fraud_score is None
#     assert response.sim_swap.status == 'completed'
#     assert response.sim_swap.swapped is False

#     clear_response = asdict(response, dict_factory=remove_none_values)
#     assert 'fraud_score' not in clear_response
#     assert 'sim_swap' in clear_response
#     assert 'reason' not in clear_response['sim_swap']


def test_validate_full_message():
    valid_message = {
        'to': '1234567890',
        'from_': '9876543210',
        'text': 'Hello, World!',
        'sig': 'asdfqwerzxcv12345678',
        'client_ref': 'ref123',
        'type': 'text',
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
    try:
        SmsMessage(**valid_message)
    except ValidationError:
        assert False, 'Validation error occurred for a valid SmsMessage'

    # Invalid SmsMessage - missing required fields
    invalid_message = {'to': '+1234567890', 'text': 'Hello, World!'}
    with raises(ValidationError):
        SmsMessage(**invalid_message)

    # Invalid SmsMessage - invalid type value
    invalid_message = {
        'to': '+1234567890',
        'from_': '+9876543210',
        'text': 'Hello, World!',
        'type': 'invalid_type',
    }
    with raises(ValidationError):
        SmsMessage(**invalid_message)

    # Invalid SmsMessage - invalid body for non-binary type
    invalid_message = {
        'to': '+1234567890',
        'from_': '+9876543210',
        'text': 'Hello, World!',
        'type': 'text',
        'body': 'binary data',
    }
    with raises(ValidationError):
        SmsMessage(**invalid_message)

    # Invalid SmsMessage - missing body for binary type
    invalid_message = {
        'to': '+1234567890',
        'from_': '+9876543210',
        'text': 'Hello, World!',
        'type': 'binary',
    }
    with raises(ValidationError):
        SmsMessage(**invalid_message)

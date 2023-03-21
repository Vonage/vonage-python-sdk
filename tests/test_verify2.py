from vonage import Client, Verify2
from util import *
from vonage.errors import ClientError

import responses
from pytest import raises

verify2 = Verify2(Client())


@responses.activate
def test_new_request_sms_basic(dummy_data):
    stub(responses.POST, 'https://api.nexmo.com/v2/verify', fixture_path='verify2/create_request.json')

    params = {'brand': 'ACME, Inc', 'workflow': [{'channel': 'sms', 'to': '447700900000'}]}
    verify_request = verify2.new_request(params)

    assert isinstance(verify_request, dict)
    assert request_user_agent() == dummy_data.user_agent
    assert verify_request['request_id'] == 'c11236f4-00bf-4b89-84ba-88b25df97315'


@responses.activate
def test_new_request_sms_full():
    stub(responses.POST, 'https://api.nexmo.com/v2/verify', fixture_path='verify2/create_request.json')

    params = {
        'locale': 'en-gb',
        'channel_timeout': 120,
        'client_ref': 'my client ref',
        'code_length': 8,
        'brand': 'ACME, Inc',
        'workflow': [{'channel': 'sms', 'to': '447700900000', 'app_hash': 'asdfghjklqw'}],
    }
    verify_request = verify2.new_request(params)

    assert isinstance(verify_request, dict)
    assert verify_request['request_id'] == 'c11236f4-00bf-4b89-84ba-88b25df97315'


@responses.activate
def test_new_request_error_conflict():
    stub(responses.POST, 'https://api.nexmo.com/v2/verify', fixture_path='verify2/error_conflict.json', status_code=409)
    params = {'brand': 'ACME, Inc', 'workflow': [{'channel': 'sms', 'to': '447700900000'}]}

    with raises(ClientError) as err:
        verify2.new_request(params)
    assert (
        str(err.value)
        == "Conflict: Concurrent verifications to the same number are not allowed. (https://www.developer.vonage.com/api-errors/verify#conflict)"
    )

from vonage import Client, Verify2
from util import *
from vonage.errors import ClientError, Verify2Error

from pydantic import ValidationError
from pytest import raises
import responses

verify2 = Verify2(Client())


@responses.activate
def test_new_request_sms_basic(dummy_data):
    stub(responses.POST, 'https://api.nexmo.com/v2/verify', fixture_path='verify2/create_request.json', status_code=202)

    params = {'brand': 'ACME, Inc', 'workflow': [{'channel': 'sms', 'to': '447700900000'}]}
    verify_request = verify2.new_request(params)

    assert request_user_agent() == dummy_data.user_agent
    assert verify_request['request_id'] == 'c11236f4-00bf-4b89-84ba-88b25df97315'


@responses.activate
def test_new_request_sms_full():
    stub(responses.POST, 'https://api.nexmo.com/v2/verify', fixture_path='verify2/create_request.json', status_code=202)

    params = {
        'locale': 'en-gb',
        'channel_timeout': 120,
        'client_ref': 'my client ref',
        'code_length': 8,
        'fraud_check': False,
        'brand': 'ACME, Inc',
        'workflow': [{'channel': 'sms', 'to': '447700900000', 'app_hash': 'asdfghjklqw'}],
    }
    verify_request = verify2.new_request(params)

    assert verify_request['request_id'] == 'c11236f4-00bf-4b89-84ba-88b25df97315'


@responses.activate
def test_new_request_sms_custom_code(dummy_data):
    stub(responses.POST, 'https://api.nexmo.com/v2/verify', fixture_path='verify2/create_request.json', status_code=202)

    params = {'brand': 'ACME, Inc', 'code': 'asdfghjk', 'workflow': [{'channel': 'sms', 'to': '447700900000'}]}
    verify_request = verify2.new_request(params)

    assert request_user_agent() == dummy_data.user_agent
    assert verify_request['request_id'] == 'c11236f4-00bf-4b89-84ba-88b25df97315'


@responses.activate
def test_new_request_error_fraud_check_invalid_account(dummy_data):
    stub(
        responses.POST,
        'https://api.nexmo.com/v2/verify',
        fixture_path='verify2/fraud_check_invalid_account.json',
        status_code=403,
    )

    params = {'brand': 'ACME, Inc', 'fraud_check': False, 'workflow': [{'channel': 'sms', 'to': '447700900000'}]}

    with raises(ClientError) as err:
        verify2.new_request(params)
    assert (
        str(err.value)
        == 'Forbidden: Your account does not have permission to perform this action. (https://developer.nexmo.com/api-errors#forbidden)'
    )


def test_new_request_sms_custom_code_length_error():
    params = {
        'code_length': 4,
        'brand': 'ACME, Inc',
        'code': 'a',
        'workflow': [{'channel': 'sms', 'to': '447700900000'}],
    }

    with raises(ValidationError) as err:
        verify2.new_request(params)
    assert 'ensure this value has at least 4 characters' in str(err.value)


def test_new_request_sms_custom_code_character_error():
    params = {
        'code_length': 4,
        'brand': 'ACME, Inc',
        'code': '?!@%',
        'workflow': [{'channel': 'sms', 'to': '447700900000'}],
    }

    with raises(ValidationError) as err:
        verify2.new_request(params)
    assert 'string does not match regex' in str(err.value)


def test_new_request_invalid_channel_error():
    params = {
        'code_length': 4,
        'brand': 'ACME, Inc',
        'workflow': [{'channel': 'carrier_pigeon', 'to': '447700900000'}],
    }

    with raises(Verify2Error) as err:
        verify2.new_request(params)
    assert (
        str(err.value)
        == 'You must specify a valid verify channel inside the "workflow" object, one of: "[\'sms\', \'whatsapp\', \'whatsapp_interactive\', \'voice\', \'email\', \'silent_auth\']"'
    )


def test_new_request_code_length_error():
    params = {
        'code_length': 1000,
        'brand': 'ACME, Inc',
        'workflow': [{'channel': 'sms', 'to': '447700900000'}],
    }

    with raises(ValidationError) as err:
        verify2.new_request(params)
    assert 'ensure this value is less than or equal to 10' in str(err.value)


def test_new_request_to_error():
    params = {
        'brand': 'ACME, Inc',
        'workflow': [{'channel': 'sms', 'to': '123'}],
    }

    with raises(Verify2Error) as err:
        verify2.new_request(params)
    assert 'You must specify a valid "to" value for channel "sms"' in str(err.value)


def test_new_request_sms_app_hash_error():
    params = {
        'brand': 'ACME, Inc',
        'workflow': [{'channel': 'sms', 'to': '447700900000', 'app_hash': '00'}],
    }

    with raises(Verify2Error) as err:
        verify2.new_request(params)
    assert 'Invalid "app_hash" specified.' in str(err.value)


def test_new_request_whatsapp_app_hash_error():
    params = {
        'brand': 'ACME, Inc',
        'workflow': [{'channel': 'whatsapp', 'to': '447700900000', 'app_hash': 'asdfqwerzxc'}],
    }

    with raises(Verify2Error) as err:
        verify2.new_request(params)
    assert str(err.value) == 'Cannot specify a value for "app_hash" unless using SMS for authentication.'


@responses.activate
def test_new_request_whatsapp():
    stub(responses.POST, 'https://api.nexmo.com/v2/verify', fixture_path='verify2/create_request.json', status_code=202)

    params = {'brand': 'ACME, Inc', 'workflow': [{'channel': 'whatsapp', 'to': '447700900000'}]}
    verify_request = verify2.new_request(params)

    assert verify_request['request_id'] == 'c11236f4-00bf-4b89-84ba-88b25df97315'


@responses.activate
def test_new_request_whatsapp_custom_code():
    stub(responses.POST, 'https://api.nexmo.com/v2/verify', fixture_path='verify2/create_request.json', status_code=202)

    params = {'brand': 'ACME, Inc', 'code': 'asdfghjk', 'workflow': [{'channel': 'whatsapp', 'to': '447700900000'}]}
    verify_request = verify2.new_request(params)

    assert verify_request['request_id'] == 'c11236f4-00bf-4b89-84ba-88b25df97315'


@responses.activate
def test_new_request_whatsapp_from_field():
    stub(responses.POST, 'https://api.nexmo.com/v2/verify', fixture_path='verify2/create_request.json', status_code=202)

    params = {'brand': 'ACME, Inc', 'workflow': [{'channel': 'whatsapp', 'to': '447700900000', 'from': '447000000000'}]}
    verify_request = verify2.new_request(params)

    assert verify_request['request_id'] == 'c11236f4-00bf-4b89-84ba-88b25df97315'


@responses.activate
def test_new_request_whatsapp_invalid_sender_error():
    stub(responses.POST, 'https://api.nexmo.com/v2/verify', fixture_path='verify2/invalid_sender.json', status_code=422)

    params = {
        'brand': 'ACME, Inc',
        'workflow': [{'channel': 'whatsapp', 'to': '447700900000', 'from': 'asdfghjkl'}],
    }
    with pytest.raises(ClientError) as err:
        verify2.new_request(params)
    assert str(err.value) == 'You must specify a valid "from" value if included.'


@responses.activate
def test_new_request_whatsapp_sender_unregistered_error():
    stub(responses.POST, 'https://api.nexmo.com/v2/verify', fixture_path='verify2/invalid_sender.json', status_code=422)

    params = {
        'brand': 'ACME, Inc',
        'workflow': [{'channel': 'whatsapp', 'to': '447700900000', 'from': '447999999999'}],
    }
    with pytest.raises(ClientError) as err:
        verify2.new_request(params)
    assert (
        str(err.value)
        == 'Invalid sender: The `from` parameter is invalid. (https://developer.nexmo.com/api-errors#invalid-param)'
    )


@responses.activate
def test_new_request_whatsapp_interactive():
    stub(responses.POST, 'https://api.nexmo.com/v2/verify', fixture_path='verify2/create_request.json', status_code=202)

    params = {'brand': 'ACME, Inc', 'workflow': [{'channel': 'whatsapp_interactive', 'to': '447700900000'}]}
    verify_request = verify2.new_request(params)

    assert verify_request['request_id'] == 'c11236f4-00bf-4b89-84ba-88b25df97315'


@responses.activate
def test_new_request_voice():
    stub(responses.POST, 'https://api.nexmo.com/v2/verify', fixture_path='verify2/create_request.json', status_code=202)

    params = {'brand': 'ACME, Inc', 'workflow': [{'channel': 'voice', 'to': '447700900000'}]}
    verify_request = verify2.new_request(params)

    assert verify_request['request_id'] == 'c11236f4-00bf-4b89-84ba-88b25df97315'


@responses.activate
def test_new_request_voice_custom_code():
    stub(responses.POST, 'https://api.nexmo.com/v2/verify', fixture_path='verify2/create_request.json', status_code=202)

    params = {'brand': 'ACME, Inc', 'code': 'asdfhjkl', 'workflow': [{'channel': 'voice', 'to': '447700900000'}]}
    verify_request = verify2.new_request(params)

    assert verify_request['request_id'] == 'c11236f4-00bf-4b89-84ba-88b25df97315'


@responses.activate
def test_new_request_email():
    stub(responses.POST, 'https://api.nexmo.com/v2/verify', fixture_path='verify2/create_request.json', status_code=202)

    params = {'brand': 'ACME, Inc', 'workflow': [{'channel': 'email', 'to': 'recipient@example.com'}]}
    verify_request = verify2.new_request(params)

    assert verify_request['request_id'] == 'c11236f4-00bf-4b89-84ba-88b25df97315'


@responses.activate
def test_new_request_email_additional_fields():
    stub(responses.POST, 'https://api.nexmo.com/v2/verify', fixture_path='verify2/create_request.json', status_code=202)

    params = {
        'locale': 'en-gb',
        'channel_timeout': 120,
        'client_ref': 'my client ref',
        'code_length': 8,
        'brand': 'ACME, Inc',
        'code': 'asdfhjkl',
        'workflow': [{'channel': 'email', 'to': 'recipient@example.com', 'from': 'sender@example.com'}],
    }
    verify_request = verify2.new_request(params)

    assert verify_request['request_id'] == 'c11236f4-00bf-4b89-84ba-88b25df97315'


@responses.activate
def test_new_request_email_error():
    stub(responses.POST, 'https://api.nexmo.com/v2/verify', fixture_path='verify2/invalid_email.json', status_code=422)

    params = {
        'brand': 'ACME, Inc',
        'workflow': [{'channel': 'email', 'to': 'not-an-email-address'}],
    }
    with pytest.raises(ClientError) as err:
        verify2.new_request(params)
    assert (
        str(err.value)
        == 'Invalid params: The value of one or more parameters is invalid (https://www.nexmo.com/messages/Errors#InvalidParams)'
    )


@responses.activate
def test_new_request_silent_auth():
    stub(responses.POST, 'https://api.nexmo.com/v2/verify', fixture_path='verify2/create_request.json', status_code=202)

    params = {'brand': 'ACME, Inc', 'workflow': [{'channel': 'silent_auth', 'to': '447700900000'}]}
    verify_request = verify2.new_request(params)

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


@responses.activate
def test_new_request_rate_limit():
    stub(responses.POST, 'https://api.nexmo.com/v2/verify', fixture_path='verify2/rate_limit.json', status_code=429)
    params = {'brand': 'ACME, Inc', 'workflow': [{'channel': 'sms', 'to': '447700900000'}]}

    with raises(ClientError) as err:
        verify2.new_request(params)
    assert (
        str(err.value)
        == "Rate Limit Hit: Please wait, then retry your request (https://www.developer.vonage.com/api-errors#throttled)"
    )


@responses.activate
def test_check_code():
    stub(
        responses.POST,
        'https://api.nexmo.com/v2/verify/c11236f4-00bf-4b89-84ba-88b25df97315',
        fixture_path='verify2/check_code.json',
    )

    response = verify2.check_code('c11236f4-00bf-4b89-84ba-88b25df97315', '1234')
    assert response['request_id'] == 'e043d872-459b-4750-a20c-d33f91d6959f'
    assert response['status'] == 'completed'


@responses.activate
def test_check_code_invalid_code():
    stub(
        responses.POST,
        'https://api.nexmo.com/v2/verify/c11236f4-00bf-4b89-84ba-88b25df97315',
        fixture_path='verify2/invalid_code.json',
        status_code=400,
    )

    with pytest.raises(ClientError) as err:
        verify2.check_code('c11236f4-00bf-4b89-84ba-88b25df97315', '5678')

    assert (
        str(err.value)
        == 'Invalid Code: The code you provided does not match the expected value. (https://developer.nexmo.com/api-errors#bad-request)'
    )


@responses.activate
def test_check_code_already_verified():
    stub(
        responses.POST,
        'https://api.nexmo.com/v2/verify/c11236f4-00bf-4b89-84ba-88b25df97315',
        fixture_path='verify2/already_verified.json',
        status_code=404,
    )

    with pytest.raises(ClientError) as err:
        verify2.check_code('c11236f4-00bf-4b89-84ba-88b25df97315', '5678')

    assert (
        str(err.value)
        == "Not Found: Request '5fcc26ef-1e54-48a6-83ab-c47546a19824' was not found or it has been verified already. (https://developer.nexmo.com/api-errors#not-found)"
    )


@responses.activate
def test_check_code_workflow_not_supported():
    stub(
        responses.POST,
        'https://api.nexmo.com/v2/verify/c11236f4-00bf-4b89-84ba-88b25df97315',
        fixture_path='verify2/code_not_supported.json',
        status_code=409,
    )

    with pytest.raises(ClientError) as err:
        verify2.check_code('c11236f4-00bf-4b89-84ba-88b25df97315', '5678')

    assert (
        str(err.value)
        == 'Conflict: The current Verify workflow step does not support a code. (https://developer.nexmo.com/api-errors#conflict)'
    )


@responses.activate
def test_check_code_too_many_invalid_code_attempts():
    stub(
        responses.POST,
        'https://api.nexmo.com/v2/verify/c11236f4-00bf-4b89-84ba-88b25df97315',
        fixture_path='verify2/too_many_code_attempts.json',
        status_code=410,
    )

    with pytest.raises(ClientError) as err:
        verify2.check_code('c11236f4-00bf-4b89-84ba-88b25df97315', '5678')

    assert (
        str(err.value)
        == 'Invalid Code: An incorrect code has been provided too many times. Workflow terminated. (https://developer.nexmo.com/api-errors#gone)'
    )


@responses.activate
def test_check_code_rate_limit():
    stub(
        responses.POST,
        'https://api.nexmo.com/v2/verify/c11236f4-00bf-4b89-84ba-88b25df97315',
        fixture_path='verify2/rate_limit.json',
        status_code=429,
    )

    with raises(ClientError) as err:
        verify2.check_code('c11236f4-00bf-4b89-84ba-88b25df97315', '5678')
    assert (
        str(err.value)
        == "Rate Limit Hit: Please wait, then retry your request (https://www.developer.vonage.com/api-errors#throttled)"
    )


@responses.activate
def test_cancel_verification():
    stub(
        responses.DELETE,
        'https://api.nexmo.com/v2/verify/c11236f4-00bf-4b89-84ba-88b25df97315',
        fixture_path='no_content.json',
        status_code=204,
    )

    assert verify2.cancel_verification('c11236f4-00bf-4b89-84ba-88b25df97315') == None


@responses.activate
def test_cancel_verification_error_not_found():
    stub(
        responses.DELETE,
        'https://api.nexmo.com/v2/verify/c11236f4-00bf-4b89-84ba-88b25df97315',
        fixture_path='verify2/request_not_found.json',
        status_code=404,
    )

    with raises(ClientError) as err:
        verify2.cancel_verification('c11236f4-00bf-4b89-84ba-88b25df97315')
    assert (
        str(err.value)
        == "Not Found: Request 'c11236f4-00bf-4b89-84ba-88b25df97315' was not found or it has been verified already. (https://developer.nexmo.com/api-errors#not-found)"
    )


def test_remove_unnecessary_fraud_check():
    params = {'brand': 'ACME, Inc', 'workflow': [{'channel': 'sms', 'to': '447700900000'}], 'fraud_check': True}
    verify2._remove_unnecessary_fraud_check(params)

    assert 'fraud_check' not in params

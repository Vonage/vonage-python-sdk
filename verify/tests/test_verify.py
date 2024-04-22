from os.path import abspath

import responses
from pytest import raises
from vonage_http_client.errors import NotFoundError
from vonage_http_client.http_client import HttpClient
from vonage_verify.errors import VerifyError
from vonage_verify.language_codes import LanguageCode, Psd2LanguageCode
from vonage_verify.requests import Psd2Request, VerifyRequest
from vonage_verify.responses import NetworkUnblockStatus, VerifyControlStatus
from vonage_verify.verify import Verify

from testutils import build_response, get_mock_api_key_auth

path = abspath(__file__)


verify = Verify(HttpClient(get_mock_api_key_auth()))

data = {
    'number': '1234567890',
    'country': 'US',
    'code_length': 6,
    'pin_expiry': 600,
    'next_event_wait': 150,
    'workflow_id': 2,
}


def test_create_verify_request_model():
    params = {'brand': 'Acme Inc.', 'sender_id': 'Acme', 'lg': LanguageCode.en_us, **data}
    request = VerifyRequest(**params)

    assert request.model_dump(exclude_none=True) == params


def test_create_psd2_request_model():
    params = {'payee': 'Acme Inc.', 'amount': 99.99, 'lg': Psd2LanguageCode.en_gb, **data}
    request = Psd2Request(**params)

    assert request.model_dump(exclude_none=True) == params


def test_create_verify_request_model_invalid_pin_expiry(caplog):
    data['pin_expiry'] = 301
    data['next_event_wait'] = 150
    params = {'brand': 'Acme Inc.', 'sender_id': 'Acme', **data}
    VerifyRequest(**params)

    assert 'The current values are: pin_expiry=301, next_event_wait=150.' in caplog.text


@responses.activate
def test_make_verify_request():
    build_response(
        path, 'POST', 'https://api.nexmo.com/verify/json', 'verify_request.json'
    )
    params = {'number': '1234567890', 'brand': 'Acme Inc.'}
    request = VerifyRequest(**params)

    response = verify.start_verification(request)
    assert response.request_id == 'abcdef0123456789abcdef0123456789'
    assert response.status == '0'


@responses.activate
def test_make_psd2_request():
    build_response(
        path, 'POST', 'https://api.nexmo.com/verify/psd2/json', 'verify_request.json'
    )
    params = {'number': '1234567890', 'payee': 'Acme Inc.', 'amount': 99.99}
    request = Psd2Request(**params)

    response = verify.start_psd2_verification(request)
    assert response.request_id == 'abcdef0123456789abcdef0123456789'
    assert response.status == '0'


@responses.activate
def test_verify_request_error():
    build_response(
        path, 'POST', 'https://api.nexmo.com/verify/json', 'verify_request_error.json'
    )
    params = {'number': '1234567890', 'brand': 'Acme Inc.'}
    request = VerifyRequest(**params)

    with raises(VerifyError) as e:
        verify.start_verification(request)

    assert e.match(
        "'error_text': 'Concurrent verifications to the same number are not allowed'"
    )


@responses.activate
def test_verify_request_error_with_network():
    build_response(
        path,
        'POST',
        'https://api.nexmo.com/verify/json',
        'verify_request_error_with_network.json',
    )
    params = {'number': '1234567890', 'brand': 'Acme Inc.'}
    request = VerifyRequest(**params)

    with raises(VerifyError) as e:
        verify.start_verification(request)

    assert e.match("'network': '244523'")


@responses.activate
def test_check_code():
    build_response(
        path, 'POST', 'https://api.nexmo.com/verify/check/json', 'check_code.json'
    )
    response = verify.check_code(
        request_id='c5037cb8b47449158ed6611afde58990', code='1234'
    )
    assert response.request_id == 'c5037cb8b47449158ed6611afde58990'
    assert response.status == '0'
    assert response.event_id == '390f7296-aeff-45ba-8931-84a13f3f76d7'
    assert response.price == '0.05000000'
    assert response.currency == 'EUR'
    assert response.estimated_price_messages_sent == '0.04675'


@responses.activate
def test_check_code_error():
    build_response(
        path, 'POST', 'https://api.nexmo.com/verify/check/json', 'check_code_error.json'
    )

    with raises(VerifyError) as e:
        verify.check_code(request_id='c5037cb8b47449158ed6611afde58990', code='1234')

    assert e.match(
        "'status': '16', 'error_text': 'The code provided does not match the expected value'"
    )


@responses.activate
def test_search():
    build_response(
        path, 'GET', 'https://api.nexmo.com/verify/search/json', 'search_request.json'
    )
    response = verify.search('c5037cb8b47449158ed6611afde58990')

    assert response.request_id == 'cc121958d8fb4368aa3bb762bb9a0f74'
    assert response.account_id == 'abcdef01'
    assert response.status == 'EXPIRED'
    assert response.number == '1234567890'
    assert response.price == '0'
    assert response.currency == 'EUR'
    assert response.sender_id == 'Acme Inc.'
    assert response.date_submitted == '2024-04-03 02:22:37'
    assert response.date_finalized == '2024-04-03 02:27:38'
    assert response.first_event_date == '2024-04-03 02:22:37'
    assert response.last_event_date == '2024-04-03 02:24:38'
    assert response.estimated_price_messages_sent == '0.09350'
    assert response.checks[0].date_received == '2024-04-03 02:23:04'
    assert response.checks[0].code == '1234'
    assert response.checks[0].status == 'INVALID'
    assert response.checks[0].ip_address == ''
    assert response.events[0].type == 'sms'
    assert response.events[0].id == '23f3a13d-6d03-4262-8f4d-67f12a56e1c8'


@responses.activate
def test_search_list_of_ids():
    build_response(
        path,
        'GET',
        'https://api.nexmo.com/verify/search/json',
        'search_request_list.json',
    )
    response0, response1 = verify.search(
        ['cc121958d8fb4368aa3bb762bb9a0f75', 'c5037cb8b47449158ed6611afde58990']
    )
    assert response0.request_id == 'cc121958d8fb4368aa3bb762bb9a0f74'
    assert response1.request_id == 'c5037cb8b47449158ed6611afde58990'
    assert response1.status == 'SUCCESS'
    assert response1.checks[0].status == 'VALID'


@responses.activate
def test_search_error():
    build_response(
        path,
        'GET',
        'https://api.nexmo.com/verify/search/json',
        'search_request_error.json',
    )

    with raises(VerifyError) as e:
        verify.search('c5037cb8b47449158ed6611afde58990')

    assert e.match("{'status': '101', 'error_text': 'No response found'}")


@responses.activate
def test_cancel_verification():
    build_response(
        path,
        'POST',
        'https://api.nexmo.com/verify/control/json',
        'cancel_verification.json',
    )
    response = verify.cancel_verification('c5037cb8b47449158ed6611afde58990')

    assert type(response) == VerifyControlStatus
    assert response.status == '0'
    assert response.command == 'cancel'


@responses.activate
def test_cancel_verification_error():
    build_response(
        path,
        'POST',
        'https://api.nexmo.com/verify/control/json',
        'cancel_verification_error.json',
    )

    with raises(VerifyError) as e:
        verify.cancel_verification('c5037cb8b47449158ed6611afde58990')

    assert e.match(
        "The requestId 'cc121958d8fb4368aa3bb762bb9a0f75' does not exist or its no longer active."
    )


@responses.activate
def test_trigger_next_event():
    build_response(
        path,
        'POST',
        'https://api.nexmo.com/verify/control/json',
        'trigger_next_event.json',
    )
    response = verify.trigger_next_event('c5037cb8b47449158ed6611afde58990')

    assert type(response) == VerifyControlStatus
    assert response.status == '0'
    assert response.command == 'trigger_next_event'


@responses.activate
def test_trigger_next_event_error():
    build_response(
        path,
        'POST',
        'https://api.nexmo.com/verify/control/json',
        'trigger_next_event_error.json',
    )

    with raises(VerifyError) as e:
        verify.trigger_next_event('2c021d25cf2e47a9b277a996f4325b81')

    assert e.match("'status': '19")
    assert e.match('No more events are left to execute for the request')


@responses.activate
def test_request_network_unblock():
    build_response(
        path,
        'POST',
        'https://api.nexmo.com/verify/network-unblock',
        'network_unblock.json',
        202,
    )

    response = verify.request_network_unblock('23410')

    assert verify._http_client.last_response.status_code == 202
    assert type(response) == NetworkUnblockStatus
    assert response.network == '23410'
    assert response.unblocked_until == '2024-04-22T08:34:58Z'


@responses.activate
def test_request_network_unblock_error():
    build_response(
        path,
        'POST',
        'https://api.nexmo.com/verify/network-unblock',
        'network_unblock_error.json',
        404,
    )

    try:
        verify.request_network_unblock('23410')
    except NotFoundError as e:
        assert (
            e.response.json()['detail']
            == 'The network you provided does not have an active block.'
        )
        assert e.response.json()['title'] == 'Not Found'


def test_http_client_property():
    verify = Verify(HttpClient(get_mock_api_key_auth()))
    assert isinstance(verify.http_client, HttpClient)

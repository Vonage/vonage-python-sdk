from os.path import abspath

import responses
from vonage_http_client.http_client import HttpClient
from vonage_verify.language_codes import LanguageCode, Psd2LanguageCode
from vonage_verify.requests import Psd2Request, VerifyRequest
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


def test_create_valid_verify_request_model():
    params = {'brand': 'Acme Inc.', 'sender_id': 'Acme', 'lg': LanguageCode.en_us, **data}
    request = VerifyRequest(**params)

    assert request.model_dump(exclude_none=True) == params


def test_create_valid_psd2_request_model():
    params = {'payee': 'Acme Inc.', 'amount': 99.99, 'lg': Psd2LanguageCode.en_gb, **data}
    request = Psd2Request(**params)

    assert request.model_dump(exclude_none=True) == params


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

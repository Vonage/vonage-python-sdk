from os.path import abspath

import responses
from pytest import raises
from vonage_http_client.errors import HttpRequestError
from vonage_http_client.http_client import HttpClient
from vonage_verify_v2.requests import *
from vonage_verify_v2.verify_v2 import VerifyV2

from testutils import build_response, get_mock_jwt_auth

path = abspath(__file__)


verify = VerifyV2(HttpClient(get_mock_jwt_auth()))


@responses.activate
def test_make_verify_request():
    build_response(
        path, 'POST', 'https://api.nexmo.com/v2/verify', 'verify_request.json', 202
    )
    silent_auth_channel = SilentAuthChannel(
        channel=ChannelType.SILENT_AUTH, to='1234567890'
    )
    sms_channel = SmsChannel(channel=ChannelType.SMS, to='1234567890', from_='Vonage')
    params = {
        'brand': 'Vonage',
        'workflow': [silent_auth_channel, sms_channel],
    }
    request = VerifyRequest(**params)

    response = verify.start_verification(request)
    assert response.request_id == '2c59e3f4-a047-499f-a14f-819cd1989d2e'
    assert (
        response.check_url
        == 'https://api-eu-3.vonage.com/v2/verify/cfbc9a3b-27a2-40d4-a4e0-0c59b3b41901/silent-auth/redirect'
    )
    assert verify._http_client.last_response.status_code == 202


@responses.activate
def test_verify_request_concurrent_verifications_error():
    build_response(
        path,
        'POST',
        'https://api.nexmo.com/v2/verify',
        'verify_request_error.json',
        409,
    )
    sms_channel = SmsChannel(channel=ChannelType.SMS, to='1234567890', from_='Vonage')
    params = {
        'brand': 'Vonage',
        'workflow': [sms_channel],
    }
    request = VerifyRequest(**params)

    with raises(HttpRequestError) as e:
        verify.start_verification(request)

    assert e.value.response.status_code == 409
    assert e.value.response.json()['title'] == 'Conflict'
    assert (
        e.value.response.json()['detail']
        == 'Concurrent verifications to the same number are not allowed'
    )

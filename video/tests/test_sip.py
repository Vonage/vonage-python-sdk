from os.path import abspath

import responses
from vonage_http_client import HttpClient

from vonage_video.models.sip import SipAuth, SipOptions, InitiateSipRequest
from vonage_video.models.token import TokenOptions
from vonage_video.video import Video

from testutils import build_response, get_mock_jwt_auth

path = abspath(__file__)


video = Video(HttpClient(get_mock_jwt_auth()))


def test_sip_params_model():
    sip_request_params = InitiateSipRequest(
        session_id='test_session_id',
        token='test_token',
        sip=SipOptions(
            uri='sip:user@sip.partner.com;transport=tls',
            from_='example@example.com',
            headers={'header_key': 'header_value'},
            auth=SipAuth(username='username', password='password'),
            secure=True,
            video=True,
            observe_force_mute=True,
        ),
    )

    assert sip_request_params.model_dump(by_alias=True) == {
        'sessionId': 'test_session_id',
        'token': 'test_token',
        'sip': {
            'uri': 'sip:user@sip.partner.com;transport=tls',
            'from': 'example@example.com',
            'headers': {'header_key': 'header_value'},
            'auth': {'username': 'username', 'password': 'password'},
            'secure': True,
            'video': True,
            'observeForceMute': True,
        },
    }


@responses.activate
def test_initiate_sip_call():
    build_response(
        path,
        'POST',
        'https://video.api.vonage.com/v2/project/test_application_id/dial',
        'sip.json',
        200,
    )

    sip_request_params = InitiateSipRequest(
        session_id='test_session_id',
        token='test_token',
        sip=SipOptions(
            uri='sip:user@sip.partner.com;transport=tls',
            from_='example@example.com',
            headers={'header_key': 'header_value'},
            auth=SipAuth(username='username', password='password'),
            secure=True,
            video=True,
            observe_force_mute=True,
        ),
    )

    sip_call = video.initiate_sip_call(sip_request_params)

    assert sip_call.id == ''
    assert sip_call.connection_id == ''
    assert sip_call.stream_id == ''

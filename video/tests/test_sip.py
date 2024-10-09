from os.path import abspath

import responses
from pytest import raises
from vonage_http_client import HttpClient
from vonage_video.errors import RoutedSessionRequiredError
from vonage_video.models.sip import InitiateSipRequest, SipAuth, SipOptions
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
        'initiate_sip_call.json',
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

    assert sip_call.id == '0022f6ba-c3a7-44db-843e-dd5ffa9d0493'
    assert sip_call.project_id == '29f760f8-7ce1-46c9-ade3-f2dedee4ed5f'
    assert sip_call.connection_id == '4baf5788-fa5d-4b8d-b344-7315194ebc7d'
    assert sip_call.stream_id == 'de7d4fde-1773-4c7f-a0f8-3e1e2956d739'


@responses.activate
def test_initiate_sip_call_error():
    build_response(
        path,
        'POST',
        'https://video.api.vonage.com/v2/project/test_application_id/dial',
        status_code=409,
    )

    sip_request_params = InitiateSipRequest(
        session_id='test_session_id',
        token='test_token',
        sip=SipOptions(uri='sip:example@example.com;transport=tls'),
    )

    with raises(RoutedSessionRequiredError):
        video.initiate_sip_call(sip_request_params)

    assert video.http_client.last_response.status_code == 409


@responses.activate
def test_play_dtmf():
    build_response(
        path,
        'POST',
        'https://video.api.vonage.com/v2/project/test_application_id/session/test_session_id/play-dtmf',
        status_code=200,
    )

    video.play_dtmf('test_session_id', '01234#*p')

    assert video.http_client.last_response.status_code == 200

    build_response(
        path,
        'POST',
        'https://video.api.vonage.com/v2/project/test_application_id/session/test_session_id/connection/test_connection_id/play-dtmf',
        status_code=200,
    )

    video.play_dtmf(
        session_id='test_session_id',
        digits='01234#*p',
        connection_id='test_connection_id',
    )

    assert video.http_client.last_response.status_code == 200

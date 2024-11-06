from os.path import abspath

import responses
from vonage_http_client import HttpClient
from vonage_video.video import Video

from testutils import build_response, get_mock_jwt_auth

path = abspath(__file__)


video = Video(HttpClient(get_mock_jwt_auth()))


@responses.activate
def test_disconnect_client():
    build_response(
        path,
        'DELETE',
        'https://video.api.vonage.com/v2/project/test_application_id/session/test_session_id/connection/test_connection_id',
        status_code=204,
    )

    video.disconnect_client(
        session_id='test_session_id', connection_id='test_connection_id'
    )

    assert responses.calls[0].response.status_code == 204


@responses.activate
def test_mute_stream():
    build_response(
        path,
        'POST',
        'https://video.api.vonage.com/v2/project/test_application_id/session/test_session_id/stream/test_stream_id/mute',
    )

    video.mute_stream(session_id='test_session_id', stream_id='test_stream_id')

    assert responses.calls[0].response.status_code == 200


@responses.activate
def test_mute_all_streams():
    build_response(
        path,
        'POST',
        'https://video.api.vonage.com/v2/project/test_application_id/session/test_session_id/mute',
    )

    video.mute_all_streams(session_id='test_session_id')
    assert responses.calls[0].response.status_code == 200

    video.disable_mute_all_streams(session_id='test_session_id')
    assert responses.calls[1].response.status_code == 200


@responses.activate
def test_mute_all_streams_excluded_stream_ids():
    build_response(
        path,
        'POST',
        'https://video.api.vonage.com/v2/project/test_application_id/session/test_session_id/mute',
    )

    video.mute_all_streams(
        session_id='test_session_id', excluded_stream_ids=['test_stream_id']
    )
    assert responses.calls[0].response.status_code == 200

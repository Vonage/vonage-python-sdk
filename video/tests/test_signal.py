from os.path import abspath

import responses
from vonage_http_client import HttpClient
from vonage_video.models.signal import SignalData
from vonage_video.video import Video

from testutils import build_response, get_mock_jwt_auth

path = abspath(__file__)


video = Video(HttpClient(get_mock_jwt_auth()))


@responses.activate
def test_send_signal_all():
    build_response(
        path,
        'POST',
        'https://video.api.vonage.com/v2/project/test_application_id/session/test_session_id/signal',
        status_code=204,
    )

    video.send_signal(
        session_id='test_session_id', data=SignalData(type='msg', data='Hello, World!')
    )

    assert responses.calls[0].response.status_code == 204


@responses.activate
def test_send_signal_to_connection_id():
    build_response(
        path,
        'POST',
        'https://video.api.vonage.com/v2/project/test_application_id/session/test_session_id/connection/test_connection_id/signal',
        status_code=204,
    )

    video.send_signal(
        session_id='test_session_id',
        data=SignalData(type='msg', data='Hello, World!'),
        connection_id='test_connection_id',
    )

    assert responses.calls[0].response.status_code == 204

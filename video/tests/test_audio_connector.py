from os.path import abspath

import responses
from vonage_http_client import HttpClient
from vonage_video import (
    AudioConnectorOptions,
    AudioConnectorWebSocket,
    AudioSampleRate,
    TokenOptions,
    TokenRole,
    Video,
)

from testutils import build_response, get_mock_jwt_auth

path = abspath(__file__)


video = Video(HttpClient(get_mock_jwt_auth()))


def test_audio_connector_options_model():
    options = AudioConnectorOptions(
        session_id='test_session_id',
        token='test_token',
        websocket=AudioConnectorWebSocket(
            uri='test_uri',
            streams=['test_stream_id'],
            headers={'test_header': 'test_value'},
            audio_rate=AudioSampleRate.KHZ_16,
        ),
    )

    assert options.model_dump(by_alias=True) == {
        'sessionId': 'test_session_id',
        'token': 'test_token',
        'websocket': {
            'uri': 'test_uri',
            'streams': ['test_stream_id'],
            'headers': {'test_header': 'test_value'},
            'audioRate': 16000,
        },
    }


@responses.activate
def test_start_audio_connector():
    build_response(
        path,
        'POST',
        'https://video.api.vonage.com/v2/project/test_application_id/connect',
        'audio_connector.json',
        200,
    )

    session_id = 'test_session_id'
    options = AudioConnectorOptions(
        session_id=session_id,
        token=video.generate_client_token(
            TokenOptions(session_id=session_id, role=TokenRole.MODERATOR)
        ),
        websocket=AudioConnectorWebSocket(
            uri='wss://example.com/ws',
            audio_rate=AudioSampleRate.KHZ_16,
        ),
    )

    audio_connector = video.start_audio_connector(options)

    assert audio_connector.id == 'b3cd31f4-020e-4ba3-9a2a-12d98b8a184f'
    assert audio_connector.connection_id == '1bf530df-97f4-4437-b6c9-2a66200200c8'

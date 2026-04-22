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
from vonage_video.models.audio_connector import AudioTransportConfig
from vonage_video.models.enums import AudioEncoding, AudioTransport

from testutils import build_response, get_mock_jwt_auth

path = abspath(__file__)


video = Video(HttpClient(get_mock_jwt_auth()))


def test_audio_connector_options_model():
    options_no_flag = AudioConnectorOptions(
        session_id='test_session_id',
        token='test_token',
        websocket=AudioConnectorWebSocket(
            uri='test_uri',
            streams=['test_stream_id'],
            headers={'test_header': 'test_value'},
            audio_rate=AudioSampleRate.KHZ_16,
        ),
    )
    websocket_dict = options_no_flag.model_dump(by_alias=True)["websocket"]
    assert "bidirectional" not in websocket_dict
    options = AudioConnectorOptions(
        session_id='test_session_id',
        token='test_token',
        websocket=AudioConnectorWebSocket(
            uri='test_uri',
            streams=['test_stream_id'],
            headers={'test_header': 'test_value'},
            audio_rate=AudioSampleRate.KHZ_16,
            bidirectional=True,
        ),
    )

    actual = options.model_dump(by_alias=True)
    expected = {
        'sessionId': 'test_session_id',
        'token': 'test_token',
        'websocket': {
            'uri': 'test_uri',
            'streams': ['test_stream_id'],
            'headers': {'test_header': 'test_value'},
            'audioRate': 16000,
            'bidirectional': True,
        },
    }
    assert actual == expected


def test_audio_connector_options_with_audio_transport():
    options = AudioConnectorOptions(
        session_id='test_session_id',
        token='test_token',
        websocket=AudioConnectorWebSocket(
            uri='test_uri',
            streams=['test_stream_id'],
            headers={'test_header': 'test_value'},
            audio_rate=AudioSampleRate.KHZ_16,
            audio_transport=AudioTransportConfig(
                transport=AudioTransport.JSON,
                encoding=AudioEncoding.BASE64,
            ),
        ),
    )

    actual = options.model_dump(by_alias=True, exclude_none=True)
    assert actual['websocket']['audioTransport'] == '{"transport":"json","encoding":"base64"}'
    assert 'audio_transport' not in actual['websocket']


def test_audio_connector_options_with_audio_transport_full():
    options = AudioConnectorOptions(
        session_id='test_session_id',
        token='test_token',
        websocket=AudioConnectorWebSocket(
            uri='test_uri',
            audio_transport=AudioTransportConfig(
                transport=AudioTransport.JSON,
                encoding=AudioEncoding.BASE64,
                audio_field='data',
                static_fields={'event': 'media'},
            ),
        ),
    )

    actual = options.model_dump(by_alias=True, exclude_none=True)
    transport_json = actual['websocket']['audioTransport']
    import json

    parsed = json.loads(transport_json)
    assert parsed['transport'] == 'json'
    assert parsed['encoding'] == 'base64'
    assert parsed['audio_field'] == 'data'
    assert parsed['static_fields'] == {'event': 'media'}


def test_audio_connector_options_with_binary_transport():
    options = AudioConnectorOptions(
        session_id='test_session_id',
        token='test_token',
        websocket=AudioConnectorWebSocket(
            uri='test_uri',
            audio_transport=AudioTransportConfig(
                transport=AudioTransport.BINARY,
            ),
        ),
    )

    actual = options.model_dump(by_alias=True, exclude_none=True)
    assert actual['websocket']['audioTransport'] == '{"transport":"binary"}'


def test_audio_connector_options_without_audio_transport():
    options = AudioConnectorOptions(
        session_id='test_session_id',
        token='test_token',
        websocket=AudioConnectorWebSocket(
            uri='test_uri',
        ),
    )

    actual = options.model_dump(by_alias=True, exclude_none=True)
    assert 'audioTransport' not in actual['websocket']
    assert 'audio_transport' not in actual['websocket']


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

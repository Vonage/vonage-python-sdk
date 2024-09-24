from os.path import abspath

import responses
from vonage_http_client import HttpClient
from vonage_video.models.stream import StreamLayout, StreamLayoutOptions
from vonage_video.video import Video

from testutils import build_response, get_mock_jwt_auth

path = abspath(__file__)


video = Video(HttpClient(get_mock_jwt_auth()))


def test_stream_layout_model():
    stream_layout = StreamLayout(
        id='e08ff3f4-d04b-4363-bd6c-31bd29648ec8', layout_class_list=['full']
    )

    stream_layout_options = StreamLayoutOptions(items=[stream_layout])

    assert stream_layout.id == 'e08ff3f4-d04b-4363-bd6c-31bd29648ec8'
    assert stream_layout.layout_class_list == ['full']
    assert stream_layout_options.items == [stream_layout]


@responses.activate
def test_list_streams():
    build_response(
        path,
        'GET',
        'https://video.api.vonage.com/v2/project/test_application_id/session/test_session_id/stream',
        'list_streams.json',
    )

    streams = video.list_streams(session_id='test_session_id')

    assert len(streams) == 1
    assert streams[0].id == 'e08ff3f4-d04b-4363-bd6c-31bd29648ec8'
    assert streams[0].video_type == 'camera'
    assert streams[0].name == ''
    assert streams[0].layout_class_list == []


@responses.activate
def test_get_stream():
    build_response(
        path,
        'GET',
        'https://video.api.vonage.com/v2/project/test_application_id/session/test_session_id/stream/e08ff3f4-d04b-4363-bd6c-31bd29648ec8',
        'get_stream.json',
    )

    stream = video.get_stream(
        session_id='test_session_id', stream_id='e08ff3f4-d04b-4363-bd6c-31bd29648ec8'
    )

    assert stream.id == 'e08ff3f4-d04b-4363-bd6c-31bd29648ec8'
    assert stream.video_type == 'camera'
    assert stream.name == ''
    assert stream.layout_class_list == []


@responses.activate
def test_change_stream_layout():
    build_response(
        path,
        'PUT',
        'https://video.api.vonage.com/v2/project/test_application_id/session/test_session_id/stream',
        'change_stream_layout.json',
    )

    layout = StreamLayoutOptions(
        items=[
            StreamLayout(
                id='e08ff3f4-d04b-4363-bd6c-31bd29648ec8', layout_class_list=['full']
            )
        ]
    )

    streams = video.change_stream_layout(
        session_id='test_session_id', stream_layout_options=layout
    )

    assert len(streams) == 1
    assert streams[0].id == 'e08ff3f4-d04b-4363-bd6c-31bd29648ec8'
    assert streams[0].video_type == 'camera'
    assert streams[0].name == ''
    assert streams[0].layout_class_list == ['full']

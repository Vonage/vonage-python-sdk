from os.path import abspath

import responses
from pytest import raises
from vonage_http_client.errors import HttpRequestError
from vonage_http_client.http_client import HttpClient
from vonage_video.errors import (
    InvalidBroadcastStateError,
    InvalidHlsOptionsError,
    InvalidOutputOptionsError,
)
from vonage_video.models.broadcast import (
    BroadcastHls,
    BroadcastOutputSettings,
    BroadcastRtmp,
    CreateBroadcastRequest,
    ListBroadcastsFilter,
)
from vonage_video.models.common import AddStreamRequest, ComposedLayout
from vonage_video.models.enums import LayoutType, StreamMode, VideoResolution
from vonage_video.video import Video

from testutils import build_response, get_mock_jwt_auth

path = abspath(__file__)

video = Video(HttpClient(get_mock_jwt_auth()))


def test_broadcast_hls_invalid():
    with raises(InvalidHlsOptionsError):
        BroadcastHls(dvr=True, low_latency=True)


def test_broadcast_output_settings_invalid():
    with raises(InvalidOutputOptionsError):
        BroadcastOutputSettings()


def test_create_broadcast_request_valid():
    request = CreateBroadcastRequest(
        session_id="1_MX40NTY3NjYzMn5-MTQ4MTY3NjYzMn5",
        layout=ComposedLayout(type="bestFit"),
        max_duration=3600,
        outputs=BroadcastOutputSettings(hls=BroadcastHls(dvr=True)),
        resolution=VideoResolution.RES_1280x720,
        stream_mode=StreamMode.AUTO,
        multi_broadcast_tag="test_multi_broadcast_tag",
        max_bitrate=2000000,
    )
    assert request.session_id == "1_MX40NTY3NjYzMn5-MTQ4MTY3NjYzMn5"
    assert request.layout.type == "bestFit"
    assert request.max_duration == 3600
    assert request.outputs.hls.dvr is True
    assert request.resolution == VideoResolution.RES_1280x720
    assert request.stream_mode == StreamMode.AUTO
    assert request.multi_broadcast_tag == "test_multi_broadcast_tag"
    assert request.max_bitrate == 2000000


@responses.activate
def test_list_broadcasts():
    build_response(
        path,
        'GET',
        'https://video.api.vonage.com/v2/project/test_application_id/broadcast',
        'list_broadcasts.json',
    )

    filter = ListBroadcastsFilter(offset=0, page_size=10, session_id='test_session_id')
    broadcasts, count, next_page = video.list_broadcasts(filter)

    assert count == 2
    assert next_page is None
    assert broadcasts[0].id == '32cd16ee-715b-4025-bbc6-f314c1459e2f'
    assert broadcasts[0].status == 'started'
    assert broadcasts[0].resolution == '1280x720'
    assert (
        broadcasts[0].broadcast_urls.rtmp[0].server_url
        == 'rtmp://a.rtmp.youtube.com/live2'
    )
    assert broadcasts[0].broadcast_urls.hls == 'https://example.com/hls.m3u8'
    assert broadcasts[0].broadcast_urls.hls_status == 'ready'
    assert broadcasts[1].multi_broadcast_tag == 'test-broadcast'
    assert broadcasts[1].settings.hls.dvr is True
    assert broadcasts[1].settings.hls.low_latency is False


@responses.activate
def test_list_broadcasts_next_page():
    build_response(
        path,
        'GET',
        'https://video.api.vonage.com/v2/project/test_application_id/broadcast',
        'list_broadcasts_next_page.json',
    )

    filter = ListBroadcastsFilter(offset=0, page_size=1)
    broadcasts, count, next_page = video.list_broadcasts(filter)

    assert count == 2
    assert next_page == 1
    assert broadcasts[0].id == '32cd16ee-715b-4025-bbc6-f314c1459e2f'


@responses.activate
def test_list_broadcasts_empty_response():
    build_response(
        path,
        'GET',
        'https://video.api.vonage.com/v2/project/test_application_id/broadcast',
        'nothing.json',
    )

    filter = ListBroadcastsFilter(offset=0, page_size=10)
    broadcasts, count, next_page = video.list_broadcasts(filter)

    assert count == 0
    assert next_page is None
    assert broadcasts == []


@responses.activate
def test_start_broadcast():
    build_response(
        path,
        'POST',
        'https://video.api.vonage.com/v2/project/test_application_id/broadcast',
        'broadcast.json',
    )

    broadcast_options = CreateBroadcastRequest(
        session_id='test_session_id',
        layout=ComposedLayout(
            type=LayoutType.BEST_FIT, screenshare_type=LayoutType.HORIZONTAL_PRESENTATION
        ),
        max_duration=3600,
        outputs=BroadcastOutputSettings(
            hls=BroadcastHls(dvr=True, low_latency=False),
            rtmp=[
                BroadcastRtmp(
                    id='test',
                    server_url='rtmp://a.rtmp.youtube.com/live2',
                    stream_name='stream-key',
                )
            ],
        ),
        resolution=VideoResolution.RES_1280x720,
        stream_mode=StreamMode.AUTO,
        multi_broadcast_tag='test-broadcast-5',
        max_bitrate=1_000_000,
    )

    broadcast = video.start_broadcast(broadcast_options)

    assert broadcast.id == 'f03fad17-4591-4422-8bd3-00a4df1e616a'
    assert broadcast.session_id == 'test_session_id'
    assert broadcast.application_id == 'test_application_id'
    assert broadcast.updated_at == 1728039361511
    assert broadcast.status == 'started'
    assert (
        broadcast.broadcast_urls.rtmp[0].server_url == 'rtmp://a.rtmp.youtube.com/live2'
    )
    assert broadcast.resolution == '1280x720'


@responses.activate
def test_start_broadcast_conflict_error():
    build_response(
        path,
        'POST',
        'https://video.api.vonage.com/v2/project/test_application_id/broadcast',
        'start_broadcast_error.json',
        status_code=409,
    )

    with raises(InvalidBroadcastStateError) as e:
        broadcast_options = CreateBroadcastRequest(
            session_id='test_session_id',
            outputs=BroadcastOutputSettings(hls=BroadcastHls(dvr=True)),
        )
        video.start_broadcast(broadcast_options)

    assert 'broadcast has already started for the session' in str(e.value)


@responses.activate
def test_start_broadcast_timeout_error():
    build_response(
        path,
        'POST',
        'https://video.api.vonage.com/v2/project/test_application_id/broadcast',
        'stop_broadcast_timeout_error.json',
        status_code=408,
    )

    with raises(HttpRequestError) as e:
        video.start_broadcast(
            options=CreateBroadcastRequest(
                session_id='test_session_id',
                outputs=BroadcastOutputSettings(hls=BroadcastHls()),
            )
        )

    assert 'Request timed out.' in str(e.value)


@responses.activate
def test_get_broadcast():
    build_response(
        path,
        'GET',
        'https://video.api.vonage.com/v2/project/test_application_id/broadcast/f03fad17-4591-4422-8bd3-00a4df1e616a',
        'broadcast.json',
    )

    broadcast = video.get_broadcast('f03fad17-4591-4422-8bd3-00a4df1e616a')

    assert broadcast.id == 'f03fad17-4591-4422-8bd3-00a4df1e616a'
    assert broadcast.session_id == 'test_session_id'
    assert broadcast.updated_at == 1728039361511
    assert broadcast.status == 'started'
    assert (
        broadcast.broadcast_urls.rtmp[0].server_url == 'rtmp://a.rtmp.youtube.com/live2'
    )
    assert broadcast.resolution == '1280x720'


@responses.activate
def test_stop_broadcast():
    build_response(
        path,
        'POST',
        'https://video.api.vonage.com/v2/project/test_application_id/broadcast/f03fad17-4591-4422-8bd3-00a4df1e616a/stop',
        'stop_broadcast.json',
    )

    broadcast = video.stop_broadcast('f03fad17-4591-4422-8bd3-00a4df1e616a')

    assert broadcast.id == 'f03fad17-4591-4422-8bd3-00a4df1e616a'
    assert broadcast.status == 'stopped'


@responses.activate
def test_change_broadcast_layout():
    build_response(
        path,
        'PUT',
        'https://video.api.vonage.com/v2/project/test_application_id/broadcast/f03fad17-4591-4422-8bd3-00a4df1e616a/layout',
        'broadcast.json',
    )

    layout = ComposedLayout(type=LayoutType.BEST_FIT, screenshare_type=LayoutType.PIP)
    broadcast = video.change_broadcast_layout(
        'f03fad17-4591-4422-8bd3-00a4df1e616a', layout
    )

    assert broadcast.id == 'f03fad17-4591-4422-8bd3-00a4df1e616a'
    assert video.http_client.last_response.status_code == 200


@responses.activate
def test_add_stream_to_broadcast():
    build_response(
        path,
        'PATCH',
        'https://video.api.vonage.com/v2/project/test_application_id/broadcast/test_broadcast_id/streams',
        status_code=204,
    )

    params = AddStreamRequest(
        stream_id='47ce017c-28aa-40d0-b094-2e5dc437746c', has_audio=True, has_video=True
    )
    video.add_stream_to_broadcast(broadcast_id='test_broadcast_id', params=params)

    assert video.http_client.last_response.status_code == 204


@responses.activate
def test_remove_stream_from_broadcast():
    build_response(
        path,
        'PATCH',
        'https://video.api.vonage.com/v2/project/test_application_id/broadcast/test_broadcast_id/streams',
        status_code=204,
    )

    video.remove_stream_from_broadcast(
        broadcast_id='test_broadcast_id', stream_id='47ce017c-28aa-40d0-b094-2e5dc437746c'
    )

    assert video.http_client.last_response.status_code == 204

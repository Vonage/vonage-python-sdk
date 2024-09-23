from os.path import abspath

import responses
from vonage_http_client import HttpClient
from vonage_video.models.enums import ArchiveMode, MediaMode
from vonage_video.models.session import SessionOptions
from vonage_video.video import Video

from testutils import build_response, get_mock_jwt_auth

path = abspath(__file__)


video = Video(HttpClient(get_mock_jwt_auth()))


def test_session_options_model():
    session_options = SessionOptions(
        media_mode=MediaMode.ROUTED,
        archive_mode=ArchiveMode.ALWAYS,
        location='192.168.0.1',
        e2ee=True,
    )

    assert session_options.media_mode == MediaMode.ROUTED
    assert session_options.archive_mode == ArchiveMode.ALWAYS
    assert session_options.location == '192.168.0.1'
    assert session_options.e2ee is True
    assert session_options.p2p_preference == 'disabled'


def test_session_options_model_set_params():
    session_options = SessionOptions(
        media_mode=MediaMode.RELAYED,
        e2ee=True,
    )

    assert session_options.p2p_preference == 'always'


@responses.activate
def test_create_session():
    build_response(
        path,
        'POST',
        'https://video.api.vonage.com/session/create',
        'create_session.json',
    )

    session = video.create_session()
    assert (
        session.session_id
        == '1_MX4yOWY3NjBmOC03Y2UxLTQ2YzktYWRlMy1mMmRlZGVlNGVkNWZ-fjE3MjY0NjI1ODg2NDd-MTF4TGExYmJoelBlR1FHbVhzbWd4STBrfn5-'
    )
    assert session.archive_mode is None
    assert session.media_mode is None
    assert session.location is None

    build_response(
        path,
        'POST',
        'https://video.api.vonage.com/session/create',
        'create_session.json',
    )

    session_options = SessionOptions(
        media_mode=MediaMode.ROUTED,
        archive_mode=ArchiveMode.ALWAYS,
        location='192.168.0.1',
        e2ee=True,
    )
    session = video.create_session(session_options)

    assert (
        session.session_id
        == '1_MX4yOWY3NjBmOC03Y2UxLTQ2YzktYWRlMy1mMmRlZGVlNGVkNWZ-fjE3MjY0NjI1ODg2NDd-MTF4TGExYmJoelBlR1FHbVhzbWd4STBrfn5-'
    )
    assert session.archive_mode == ArchiveMode.ALWAYS
    assert session.media_mode == MediaMode.ROUTED
    assert session.location == '192.168.0.1'

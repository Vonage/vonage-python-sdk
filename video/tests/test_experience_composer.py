from os.path import abspath

import responses
from vonage_http_client import HttpClient
from vonage_video.models.enums import TokenRole, VideoResolution
from vonage_video.models.experience_composer import (
    ExperienceComposerOptions,
    ExperienceComposerProperties,
    ListExperienceComposersFilter,
)
from vonage_video.models.token import TokenOptions
from vonage_video.video import Video

from testutils import build_response, get_mock_jwt_auth

path = abspath(__file__)


video = Video(HttpClient(get_mock_jwt_auth()))


def test_experience_composer_model():
    options = ExperienceComposerOptions(
        session_id='test_session_id',
        token='test_token',
        url='https://example.com',
        max_duration=3600,
        resolution=VideoResolution.RES_1280x720,
        properties=ExperienceComposerProperties(name='test_experience_composer'),
    )

    assert options.model_dump(by_alias=True) == {
        'sessionId': 'test_session_id',
        'token': 'test_token',
        'url': 'https://example.com',
        'maxDuration': 3600,
        'resolution': '1280x720',
        'properties': {'name': 'test_experience_composer'},
    }


@responses.activate
def test_start_experience_composer():
    build_response(
        path,
        'POST',
        'https://video.api.vonage.com/v2/project/test_application_id/render',
        'start_experience_composer.json',
        202,
    )

    session_id = 'test_session_id'
    options = ExperienceComposerOptions(
        session_id=session_id,
        token=video.generate_client_token(
            TokenOptions(session_id=session_id, role=TokenRole.MODERATOR)
        ),
        url='https://example.com',
        max_duration=3600,
        resolution=VideoResolution.RES_1280x720,
        properties=ExperienceComposerProperties(name='test_experience_composer'),
    )
    ec = video.start_experience_composer(options)

    assert ec.id == '80c3d2d8-0848-41b2-be14-1a5b8936c87d'
    assert ec.session_id == session_id
    assert ec.application_id == 'test_application_id'
    assert ec.created_at == 1727781191064
    assert ec.url == 'https://example.com'
    assert ec.status == 'starting'
    assert ec.name == 'test_experience_composer'
    assert ec.resolution == '1280x720'


@responses.activate
def test_list_experience_composers():
    build_response(
        path,
        'GET',
        'https://video.api.vonage.com/v2/project/test_application_id/render',
        'list_experience_composers.json',
    )

    ec_filter = ListExperienceComposersFilter(offset=0, page_size=3)
    ec_list, count, next_page_offset = video.list_experience_composers(filter=ec_filter)

    assert len(ec_list) == 3
    assert count == 3
    assert next_page_offset == None

    assert ec_list[0].id == 'be7712a4-3a63-4ed7-a2c6-7ffaebefd4a6'
    assert ec_list[0].session_id == 'test_session_id'
    assert ec_list[0].created_at == 1727784741000
    assert ec_list[0].url == 'https://developer.vonage.com'
    assert ec_list[1].status == 'started'
    assert ec_list[1].stream_id == 'F9C3BCD5-850F-4DB7-B6C1-97F615CA9E79'
    assert ec_list[1].resolution == '1280x720'
    assert ec_list[2].status == 'stopped'
    assert ec_list[2].reason == 'Max duration exceeded'


@responses.activate
def test_get_experience_composer():
    build_response(
        path,
        'GET',
        'https://video.api.vonage.com/v2/project/test_application_id/render/be7712a4-3a63-4ed7-a2c6-7ffaebefd4a6',
        'get_experience_composer.json',
    )

    ec = video.get_experience_composer('be7712a4-3a63-4ed7-a2c6-7ffaebefd4a6')

    assert ec.id == 'be7712a4-3a63-4ed7-a2c6-7ffaebefd4a6'
    assert ec.session_id == 'test_session_id'
    assert ec.created_at == 1727784741000
    assert ec.url == 'https://developer.vonage.com'
    assert ec.status == 'stopped'
    assert ec.stream_id == 'C1B0E149-8169-4AFD-9397-882516EE9430'
    assert ec.resolution == '1280x720'


@responses.activate
def test_stop_experience_composer():
    build_response(
        path,
        'DELETE',
        'https://video.api.vonage.com/v2/project/test_application_id/render/be7712a4-3a63-4ed7-a2c6-7ffaebefd4a6',
        status_code=204,
    )
    video.stop_experience_composer('be7712a4-3a63-4ed7-a2c6-7ffaebefd4a6')

    assert video.http_client.last_response.status_code == 204

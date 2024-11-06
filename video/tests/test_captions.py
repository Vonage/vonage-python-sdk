from os.path import abspath

import responses
from pytest import raises
from vonage_http_client import HttpClient
from vonage_http_client.errors import HttpRequestError
from vonage_video.models.captions import CaptionsData, CaptionsOptions
from vonage_video.models.enums import LanguageCode, TokenRole
from vonage_video.models.token import TokenOptions
from vonage_video.video import Video

from testutils import build_response, get_mock_jwt_auth

path = abspath(__file__)


video = Video(HttpClient(get_mock_jwt_auth()))


def test_captions_options_model():
    options = CaptionsOptions(
        session_id='test_session_id',
        token='test_token',
        language_code=LanguageCode.EN_GB,
        max_duration=300,
        partial_captions=True,
        status_callback_url='example.com/status',
    )

    assert options.model_dump(by_alias=True) == {
        'sessionId': 'test_session_id',
        'token': 'test_token',
        'languageCode': 'en-GB',
        'maxDuration': 300,
        'partialCaptions': True,
        'statusCallbackUrl': 'example.com/status',
    }


@responses.activate
def test_start_captions():
    build_response(
        path,
        'POST',
        'https://video.api.vonage.com/v2/project/test_application_id/captions',
        'start_captions.json',
        202,
    )

    session_id = 'test_session_id'
    options = CaptionsOptions(
        session_id=session_id,
        token=video.generate_client_token(
            TokenOptions(session_id=session_id, role=TokenRole.MODERATOR)
        ),
        language_code=LanguageCode.EN_GB,
        max_duration=300,
        partial_captions=True,
        status_callback_url='https://example.com/status',
    )
    captions = video.start_captions(options)

    assert captions.captions_id == 'bc01a6b7-0e8e-4aa0-bb4e-2390f7cb18a1'


@responses.activate
def test_start_captions_error_already_enabled():
    build_response(
        path,
        'POST',
        'https://video.api.vonage.com/v2/project/test_application_id/captions',
        'captions_error_already_enabled.json',
        409,
    )

    session_id = 'test_session_id'
    options = CaptionsOptions(
        session_id=session_id,
        token=video.generate_client_token(
            TokenOptions(session_id=session_id, role=TokenRole.MODERATOR)
        ),
    )

    with raises(HttpRequestError) as e:
        video.start_captions(options)
    assert 'Audio captioning is already enabled' in e.value.message


@responses.activate
def test_stop_captions():
    build_response(
        path,
        'POST',
        'https://video.api.vonage.com/v2/project/test_application_id/captions/test_captions_id/stop',
        status_code=202,
    )

    video.stop_captions(CaptionsData(captions_id='test_captions_id'))

    assert responses.calls[0].response.status_code == 202

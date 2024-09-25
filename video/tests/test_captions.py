from os.path import abspath

import responses
from vonage_http_client import HttpClient
from vonage_video.models.captions import CaptionsOptions
from vonage_video.video import Video

from testutils import build_response, get_mock_jwt_auth

path = abspath(__file__)


video = Video(HttpClient(get_mock_jwt_auth()))


@responses.activate
def test_start_captions():
    build_response(
        path,
        'POST',
        'https://video.api.vonage.com/v2/project/test_application_id/captions',
        'start_captions.json',
        202,
    )

    options = CaptionsOptions()

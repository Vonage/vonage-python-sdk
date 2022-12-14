import vonage
from util import *
from vonage.errors import InvalidAuthenticationTypeError


def test_client_doesnt_require_api_key(dummy_data):
    client = vonage.Client(application_id="myid", private_key=dummy_data.private_key)
    assert client is not None
    assert client.api_key is None
    assert client.api_secret is None


@responses.activate
def test_client_can_make_application_requests_without_api_key(dummy_data):
    stub(responses.POST, "https://api.nexmo.com/v1/calls")

    client = vonage.Client(application_id="myid", private_key=dummy_data.private_key)
    voice = vonage.Voice(client)
    voice.create_call("123455")


def test_invalid_auth_type_raises_error(client):
    with pytest.raises(InvalidAuthenticationTypeError):
        client.get(client.host(), 'my/request/uri', auth_type='magic')

@responses.activate
def test_timeout_is_set_on_client_calls(dummy_data):
    stub(responses.POST, "https://api.nexmo.com/v1/calls")

    client = vonage.Client(application_id="myid", private_key=dummy_data.private_key, timeout=1)
    voice = vonage.Voice(client)
    voice.create_call("123455")

    assert len(responses.calls) == 1
    assert responses.calls[0].request.req_kwargs["timeout"] == 1


def test_setting_video_api_host(client):
    assert client._video_host == 'video.api.vonage.com'
    client.video_host('new.video.url')
    assert client._video_host == 'new.video.url'

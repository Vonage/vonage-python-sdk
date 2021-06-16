import os.path
import time

import jwt
import requests

import vonage
from util import *


@responses.activate
def test_create_call(voice, dummy_data):
    stub(responses.POST, "https://api.nexmo.com/v1/calls")

    params = {
        "to": [{"type": "phone", "number": "14843331234"}],
        "from": {"type": "phone", "number": "14843335555"},
        "answer_url": ["https://example.com/answer"],
    }

    assert isinstance(voice.create_call(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == "application/json"

@responses.activate
def test_params_with_random_number(voice):
    url = "https://api.nexmo.com/v1/calls" 

    params = {
        "to": [{"type": "phone", "number": "14843331234"}],
        "from": {"type": "phone"},
        "random_from_number": True,
        "answer_url": ["https://example.com/answer"],
    }
    
    response_body = voice.create_call(params)

    responses.add(
        method=responses.POST,
        url=url,
        body=response_body,
        content_type='application/json'
    )

    response = requests.post(url, params=params)
    assert responses.calls[0].request.params == params


@responses.activate
def test_get_calls(voice, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/v1/calls")

    assert isinstance(voice.get_calls(), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert_re(r"\ABearer ", request_authorization())


@responses.activate
def test_get_call(voice, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/v1/calls/xx-xx-xx-xx")

    assert isinstance(voice.get_call("xx-xx-xx-xx"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert_re(r"\ABearer ", request_authorization())


@responses.activate
def test_update_call(voice, dummy_data):
    stub(responses.PUT, "https://api.nexmo.com/v1/calls/xx-xx-xx-xx")

    assert isinstance(voice.update_call("xx-xx-xx-xx", action="hangup"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == "application/json"
    assert request_body() == b'{"action": "hangup"}'


@responses.activate
def test_send_audio(voice, dummy_data):
    stub(responses.PUT, "https://api.nexmo.com/v1/calls/xx-xx-xx-xx/stream")

    assert isinstance(
        voice.send_audio("xx-xx-xx-xx", stream_url="http://example.com/audio.mp3"),
        dict,
    )
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == "application/json"
    assert request_body() == b'{"stream_url": "http://example.com/audio.mp3"}'


@responses.activate
def test_stop_audio(voice, dummy_data):
    stub(responses.DELETE, "https://api.nexmo.com/v1/calls/xx-xx-xx-xx/stream")

    assert isinstance(voice.stop_audio("xx-xx-xx-xx"), dict)
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_send_speech(voice, dummy_data):
    stub(responses.PUT, "https://api.nexmo.com/v1/calls/xx-xx-xx-xx/talk")

    assert isinstance(voice.send_speech("xx-xx-xx-xx", text="Hello"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == "application/json"
    assert request_body() == b'{"text": "Hello"}'


@responses.activate
def test_stop_speech(voice, dummy_data):
    stub(responses.DELETE, "https://api.nexmo.com/v1/calls/xx-xx-xx-xx/talk")

    assert isinstance(voice.stop_speech("xx-xx-xx-xx"), dict)
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_send_dtmf(voice, dummy_data):
    stub(responses.PUT, "https://api.nexmo.com/v1/calls/xx-xx-xx-xx/dtmf")

    assert isinstance(voice.send_dtmf("xx-xx-xx-xx", digits="1234"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == "application/json"
    assert request_body() == b'{"digits": "1234"}'


@responses.activate
def test_user_provided_authorization(client, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/v1/calls/xx-xx-xx-xx")

    application_id = "different-nexmo-application-id"
    nbf = int(time.time())
    exp = nbf + 3600

    client.auth(application_id=application_id, nbf=nbf, exp=exp)
    voice = vonage.Voice(client)
    voice.get_call("xx-xx-xx-xx")

    token = request_authorization().split()[1]

    token = jwt.decode(token, dummy_data.public_key, algorithms="RS256")

    assert token["application_id"] == application_id
    assert token["nbf"] == nbf
    assert token["exp"] == exp


@responses.activate
def test_authorization_with_private_key_path(dummy_data):
    stub(responses.GET, "https://api.nexmo.com/v1/calls/xx-xx-xx-xx")

    private_key = os.path.join(os.path.dirname(__file__), "data/private_key.txt")

    client = vonage.Client(
        key=dummy_data.api_key,
        secret=dummy_data.api_secret,
        application_id=dummy_data.application_id,
        private_key=private_key,
    )
    voice = vonage.Voice(client)
    voice.get_call("xx-xx-xx-xx")

    token = jwt.decode(
        request_authorization().split()[1], dummy_data.public_key, algorithms="RS256"
    )
    assert token["application_id"] == dummy_data.application_id


@responses.activate
def test_authorization_with_private_key_object(voice, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/v1/calls/xx-xx-xx-xx")

    voice.get_call("xx-xx-xx-xx")

    token = jwt.decode(
        request_authorization().split()[1], dummy_data.public_key, algorithms="RS256"
    )
    assert token["application_id"] == dummy_data.application_id


@responses.activate
def test_deprecated_create_call(client, dummy_data):
    stub(responses.POST, "https://api.nexmo.com/v1/calls")

    params = {
        "to": [{"type": "phone", "number": "14843331234"}],
        "from": {"type": "phone", "number": "14843335555"},
        "answer_url": ["https://example.com/answer"],
    }

    assert isinstance(client.create_call(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == "application/json"


@responses.activate
def test_deprecated_get_calls(client, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/v1/calls")

    assert isinstance(client.get_calls(), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert_re(r"\ABearer ", request_authorization())


@responses.activate
def test_deprecated_get_call(client, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/v1/calls/xx-xx-xx-xx")

    assert isinstance(client.get_call("xx-xx-xx-xx"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert_re(r"\ABearer ", request_authorization())


@responses.activate
def test_deprecated_update_call(client, dummy_data):
    stub(responses.PUT, "https://api.nexmo.com/v1/calls/xx-xx-xx-xx")

    assert isinstance(client.update_call("xx-xx-xx-xx", action="hangup"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == "application/json"
    assert request_body() == b'{"action": "hangup"}'


@responses.activate
def test_deprecated_send_audio(client, dummy_data):
    stub(responses.PUT, "https://api.nexmo.com/v1/calls/xx-xx-xx-xx/stream")

    assert isinstance(
        client.send_audio("xx-xx-xx-xx", stream_url="http://example.com/audio.mp3"),
        dict,
    )
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == "application/json"
    assert request_body() == b'{"stream_url": "http://example.com/audio.mp3"}'


@responses.activate
def test_deprecated_stop_audio(client, dummy_data):
    stub(responses.DELETE, "https://api.nexmo.com/v1/calls/xx-xx-xx-xx/stream")

    assert isinstance(client.stop_audio("xx-xx-xx-xx"), dict)
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_deprecated_send_speech(client, dummy_data):
    stub(responses.PUT, "https://api.nexmo.com/v1/calls/xx-xx-xx-xx/talk")

    assert isinstance(client.send_speech("xx-xx-xx-xx", text="Hello"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == "application/json"
    assert request_body() == b'{"text": "Hello"}'


@responses.activate
def test_deprecated_stop_speech(client, dummy_data):
    stub(responses.DELETE, "https://api.nexmo.com/v1/calls/xx-xx-xx-xx/talk")

    assert isinstance(client.stop_speech("xx-xx-xx-xx"), dict)
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_deprecated_send_dtmf(client, dummy_data):
    stub(responses.PUT, "https://api.nexmo.com/v1/calls/xx-xx-xx-xx/dtmf")

    assert isinstance(client.send_dtmf("xx-xx-xx-xx", digits="1234"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == "application/json"
    assert request_body() == b'{"digits": "1234"}'


@responses.activate
def test_deprecated_user_provided_authorization(client, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/v1/calls/xx-xx-xx-xx")

    application_id = "different-nexmo-application-id"
    nbf = int(time.time())
    exp = nbf + 3600

    client.auth(application_id=application_id, nbf=nbf, exp=exp)
    client.get_call("xx-xx-xx-xx")

    token = request_authorization().split()[1]

    token = jwt.decode(token, dummy_data.public_key, algorithms="RS256")

    assert token["application_id"] == application_id
    assert token["nbf"] == nbf
    assert token["exp"] == exp


@responses.activate
def test_deprecated_authorization_with_private_key_path(dummy_data):
    stub(responses.GET, "https://api.nexmo.com/v1/calls/xx-xx-xx-xx")

    private_key = os.path.join(os.path.dirname(__file__), "data/private_key.txt")

    client = vonage.Client(
        key=dummy_data.api_key,
        secret=dummy_data.api_secret,
        application_id=dummy_data.application_id,
        private_key=private_key,
    )
    client.get_call("xx-xx-xx-xx")

    token = jwt.decode(
        request_authorization().split()[1], dummy_data.public_key, algorithms="RS256"
    )
    assert token["application_id"] == dummy_data.application_id


@responses.activate
def test_deprecated_authorization_with_private_key_object(client, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/v1/calls/xx-xx-xx-xx")

    client.get_call("xx-xx-xx-xx")

    token = jwt.decode(
        request_authorization().split()[1], dummy_data.public_key, algorithms="RS256"
    )
    assert token["application_id"] == dummy_data.application_id

import os.path
import time
import jwt
from unittest.mock import patch

from vonage import Client, Voice, Ncco
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
def test_params_with_random_number(voice, dummy_data):
    stub(responses.POST, "https://api.nexmo.com/v1/calls")

    params = {
        "to": [{"type": "phone", "number": "14843331234"}],
        "random_from_number": True,
        "answer_url": ["https://example.com/answer"],
    }

    assert isinstance(voice.create_call(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == "application/json"


@responses.activate
def test_create_call_with_ncco_builder(voice, dummy_data):
    stub(responses.POST, "https://api.nexmo.com/v1/calls")

    talk = Ncco.Talk(
        text='Hello from Vonage!',
        bargeIn=True,
        loop=3,
        level=0.5,
        language='en-GB',
        style=1,
        premium=True,
    )
    ncco = Ncco.build_ncco(talk)
    voice.create_call(
        {
            'to': [{'type': 'phone', 'number': '447449815316'}],
            'from': {'type': 'phone', 'number': '447418370240'},
            'ncco': ncco,
        }
    )
    assert (
        request_body()
        == b'{"to": [{"type": "phone", "number": "447449815316"}], "from": {"type": "phone", "number": "447418370240"}, "ncco": [{"action": "talk", "text": "Hello from Vonage!", "bargeIn": true, "loop": 3, "level": 0.5, "language": "en-GB", "style": 1, "premium": true}]}'
    )
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == "application/json"


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
def test_user_provided_authorization(dummy_data):
    stub(responses.GET, "https://api.nexmo.com/v1/calls/xx-xx-xx-xx")

    application_id = "different-application-id"
    client = Client(application_id=application_id, private_key=dummy_data.private_key)

    nbf = int(time.time())
    exp = nbf + 3600

    client.auth(nbf=nbf, exp=exp)
    client.voice.get_call("xx-xx-xx-xx")

    token = request_authorization().split()[1]

    token = jwt.decode(token, dummy_data.public_key, algorithms="RS256")
    print(token)
    assert token["application_id"] == application_id
    assert token["nbf"] == nbf
    assert token["exp"] == exp


@responses.activate
def test_authorization_with_private_key_path(dummy_data):
    stub(responses.GET, "https://api.nexmo.com/v1/calls/xx-xx-xx-xx")

    private_key = os.path.join(os.path.dirname(__file__), "data/private_key.txt")

    client = Client(
        key=dummy_data.api_key,
        secret=dummy_data.api_secret,
        application_id=dummy_data.application_id,
        private_key=private_key,
    )
    voice = Voice(client)
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
def test_get_recording(voice, dummy_data):
    stub_bytes(
        responses.GET,
        "https://api.nexmo.com/v1/files/d6e47a2e-3414-11e8-8c2c-2f8b643ed957",
        body=b'THISISANMP3',
    )

    assert isinstance(
        voice.get_recording("https://api.nexmo.com/v1/files/d6e47a2e-3414-11e8-8c2c-2f8b643ed957"),
        bytes,
    )
    assert request_user_agent() == dummy_data.user_agent


def test_verify_jwt_signature(voice: Voice):
    with patch('vonage.Voice.verify_signature') as mocked_verify_signature:
        mocked_verify_signature.return_value = True
        assert voice.verify_signature('valid_token', 'valid_signature')


def test_verify_jwt_invalid_signature(voice: Voice):
    with patch('vonage.Voice.verify_signature') as mocked_verify_signature:
        mocked_verify_signature.return_value = False
        assert voice.verify_signature('token', 'invalid_signature') is False

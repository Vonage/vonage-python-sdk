from os.path import abspath

import responses
from pytest import raises

from vonage_http_client.http_client import HttpClient
from vonage_voice.errors import VoiceError
from vonage_voice.models.ncco import Talk
from vonage_voice.voice import Voice
from vonage_voice.models.requests import CreateCallRequest
from vonage_voice.models.responses import CreateCallResponse

from testutils import build_response, get_mock_jwt_auth

path = abspath(__file__)


voice = Voice(HttpClient(get_mock_jwt_auth()))


@responses.activate
def test_create_call_basic_ncco():
    build_response(
        path, 'POST', 'https://api.nexmo.com/v1/calls', 'create_call.json', 201
    )
    ncco = [Talk(text='Hello world')]
    call = CreateCallRequest(
        ncco=ncco,
        to=[{'type': 'sip', 'uri': 'sip:test@example.com'}],
        random_from_number=True,
    )
    response = voice.create_call(call)

    assert type(response) == CreateCallResponse
    assert response.uuid == '106a581a-34d0-432a-a625-220221fd434f'
    assert response.status == 'started'
    assert response.direction == 'outbound'
    assert response.conversation_uuid == 'CON-2be039b2-d0a4-4274-afc8-d7b241c7c044'


@responses.activate
def test_create_call_ncco_options():
    build_response(
        path, 'POST', 'https://api.nexmo.com/v1/calls', 'create_call.json', 201
    )
    ncco = [Talk(text='Hello world')]
    call = CreateCallRequest(
        ncco=ncco,
        to=[{'type': 'phone', 'number': '1234567890', 'dtmf_answer': '1234'}],
        from_={'number': '1234567890', 'type': 'phone'},
        event_url=['https://example.com/event'],
        event_method='POST',
        machine_detection='hangup',
        length_timer=60,
        ringing_timer=30,
    )
    response = voice.create_call(call)

    assert type(response) == CreateCallResponse
    assert response.uuid == '106a581a-34d0-432a-a625-220221fd434f'
    assert response.status == 'started'
    assert response.direction == 'outbound'
    assert response.conversation_uuid == 'CON-2be039b2-d0a4-4274-afc8-d7b241c7c044'


@responses.activate
def test_create_call_basic_answer_url():
    build_response(
        path, 'POST', 'https://api.nexmo.com/v1/calls', 'create_call.json', 201
    )
    call = CreateCallRequest(
        to=[
            {
                'type': 'websocket',
                'uri': 'wss://example.com/websocket',
                'content_type': 'audio/l16;rate=8000',
                'headers': {'key': 'value'},
            }
        ],
        answer_url=['https://example.com/answer'],
        random_from_number=True,
    )
    response = voice.create_call(call)

    assert type(response) == CreateCallResponse
    assert response.uuid == '106a581a-34d0-432a-a625-220221fd434f'
    assert response.status == 'started'
    assert response.direction == 'outbound'
    assert response.conversation_uuid == 'CON-2be039b2-d0a4-4274-afc8-d7b241c7c044'


@responses.activate
def test_create_call_answer_url_options():
    build_response(
        path, 'POST', 'https://api.nexmo.com/v1/calls', 'create_call.json', 201
    )
    call = CreateCallRequest(
        to=[{'type': 'vbc', 'extension': '1234'}],
        answer_url=['https://example.com/answer'],
        answer_method='GET',
        random_from_number=True,
        event_url=['https://example.com/event'],
        event_method='POST',
        advanced_machine_detection={
            'behavior': 'hangup',
            'mode': 'detect_beep',
            'beep_timeout': 50,
        },
        length_timer=60,
        ringing_timer=30,
    )
    response = voice.create_call(call)

    assert type(response) == CreateCallResponse
    assert response.uuid == '106a581a-34d0-432a-a625-220221fd434f'
    assert response.status == 'started'
    assert response.direction == 'outbound'
    assert response.conversation_uuid == 'CON-2be039b2-d0a4-4274-afc8-d7b241c7c044'


def test_create_call_ncco_and_answer_url_error():
    with raises(VoiceError) as e:
        CreateCallRequest(
            to=[{'type': 'phone', 'number': '1234567890'}],
            random_from_number=True,
        )
    assert e.match('Either `ncco` or `answer_url` must be set')

    with raises(VoiceError) as e:
        CreateCallRequest(
            ncco=[Talk(text='Hello world')],
            answer_url=['https://example.com/answer'],
            to=[{'type': 'phone', 'number': '1234567890'}],
            random_from_number=True,
        )
    assert e.match('`ncco` and `answer_url` cannot be used together')


def test_create_call_from_and_random_from_number_error():
    with raises(VoiceError) as e:
        CreateCallRequest(
            ncco=[Talk(text='Hello world')],
            to=[{'type': 'phone', 'number': '1234567890'}],
        )
    assert e.match('Either `from_` or `random_from_number` must be set')

    with raises(VoiceError) as e:
        CreateCallRequest(
            ncco=[Talk(text='Hello world')],
            to=[{'type': 'phone', 'number': '1234567890'}],
            from_={'number': '9876543210', 'type': 'phone'},
            random_from_number=True,
        )
    assert e.match('`from_` and `random_from_number` cannot be used together')
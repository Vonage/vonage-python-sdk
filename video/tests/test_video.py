from os.path import abspath

import responses
from pytest import raises
from responses.matchers import json_params_matcher
from vonage_http_client.http_client import HttpClient

from vonage_video.video import Video

from testutils import build_response, get_mock_jwt_auth

path = abspath(__file__)


video = Video(HttpClient(get_mock_jwt_auth()))


def test_http_client_property():
    assert type(video.http_client) == HttpClient


###


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


@responses.activate
def test_list_calls():
    build_response(path, 'GET', 'https://api.nexmo.com/v1/calls', 'list_calls.json', 200)
    calls, _ = voice.list_calls()
    assert len(calls) == 3
    assert calls[0].to.number == '1234567890'
    assert calls[0].from_.number == '9876543210'
    assert calls[0].uuid == 'e154eb57-2962-41e7-baf4-90f63e25e439'
    assert calls[1].direction == 'outbound'
    assert calls[1].status == 'completed'
    assert calls[2].conversation_uuid == 'CON-2be039b2-d0a4-4274-afc8-d7b241c7c044'


@responses.activate
def test_list_calls_filter():
    build_response(
        path, 'GET', 'https://api.nexmo.com/v1/calls', 'list_calls_filter.json', 200
    )
    filter = ListCallsFilter(
        status='completed',
        date_start='2024-03-14T07:45:14Z',
        date_end='2024-04-19T08:45:14Z',
        page_size=10,
        record_index=0,
        order='asc',
        conversation_uuid='CON-2be039b2-d0a4-4274-afc8-d7b241c7c044',
    )
    filter_dict = {
        'status': 'completed',
        'date_start': '2024-03-14T07:45:14Z',
        'date_end': '2024-04-19T08:45:14Z',
        'page_size': 10,
        'record_index': 0,
        'order': 'asc',
        'conversation_uuid': 'CON-2be039b2-d0a4-4274-afc8-d7b241c7c044',
    }
    assert filter.model_dump(by_alias=True, exclude_none=True) == filter_dict

    calls, next_record_index = voice.list_calls(filter)
    assert len(calls) == 1
    assert calls[0].to.number == '1234567890'
    assert next_record_index == 2


@responses.activate
def test_get_call():
    build_response(
        path,
        'GET',
        'https://api.nexmo.com/v1/calls/e154eb57-2962-41e7-baf4-90f63e25e439',
        'get_call.json',
        200,
    )
    call = voice.get_call('e154eb57-2962-41e7-baf4-90f63e25e439')
    assert call.to.number == '1234567890'
    assert call.from_.number == '9876543210'
    assert call.uuid == 'e154eb57-2962-41e7-baf4-90f63e25e439'
    assert call.link == '/v1/calls/e154eb57-2962-41e7-baf4-90f63e25e439'


@responses.activate
def test_transfer_call_ncco():
    build_response(
        path,
        'PUT',
        'https://api.nexmo.com/v1/calls/e154eb57-2962-41e7-baf4-90f63e25e439',
        status_code=204,
    )

    ncco = [Talk(text='Hello world')]
    voice.transfer_call_ncco('e154eb57-2962-41e7-baf4-90f63e25e439', ncco)
    assert voice._http_client.last_response.status_code == 204


@responses.activate
def test_transfer_call_answer_url():
    answer_url = 'https://example.com/answer'
    build_response(
        path,
        'PUT',
        'https://api.nexmo.com/v1/calls/e154eb57-2962-41e7-baf4-90f63e25e439',
        status_code=204,
        match=[
            json_params_matcher(
                {
                    'action': 'transfer',
                    'destination': {'type': 'ncco', 'url': [answer_url]},
                },
            ),
        ],
    )

    voice.transfer_call_answer_url('e154eb57-2962-41e7-baf4-90f63e25e439', answer_url)
    assert voice._http_client.last_response.status_code == 204


@responses.activate
def test_hangup():
    build_response(
        path,
        'PUT',
        'https://api.nexmo.com/v1/calls/e154eb57-2962-41e7-baf4-90f63e25e439',
        status_code=204,
        match=[json_params_matcher({'action': 'hangup'})],
    )

    voice.hangup('e154eb57-2962-41e7-baf4-90f63e25e439')
    assert voice._http_client.last_response.status_code == 204


@responses.activate
def test_mute():
    build_response(
        path,
        'PUT',
        'https://api.nexmo.com/v1/calls/e154eb57-2962-41e7-baf4-90f63e25e439',
        status_code=204,
        match=[json_params_matcher({'action': 'mute'})],
    )

    voice.mute('e154eb57-2962-41e7-baf4-90f63e25e439')
    assert voice._http_client.last_response.status_code == 204


@responses.activate
def test_unmute():
    build_response(
        path,
        'PUT',
        'https://api.nexmo.com/v1/calls/e154eb57-2962-41e7-baf4-90f63e25e439',
        status_code=204,
        match=[json_params_matcher({'action': 'unmute'})],
    )

    voice.unmute('e154eb57-2962-41e7-baf4-90f63e25e439')
    assert voice._http_client.last_response.status_code == 204


@responses.activate
def test_earmuff():
    build_response(
        path,
        'PUT',
        'https://api.nexmo.com/v1/calls/e154eb57-2962-41e7-baf4-90f63e25e439',
        status_code=204,
        match=[json_params_matcher({'action': 'earmuff'})],
    )

    voice.earmuff('e154eb57-2962-41e7-baf4-90f63e25e439')
    assert voice._http_client.last_response.status_code == 204


@responses.activate
def test_unearmuff():
    build_response(
        path,
        'PUT',
        'https://api.nexmo.com/v1/calls/e154eb57-2962-41e7-baf4-90f63e25e439',
        status_code=204,
        match=[json_params_matcher({'action': 'unearmuff'})],
    )

    voice.unearmuff('e154eb57-2962-41e7-baf4-90f63e25e439')
    assert voice._http_client.last_response.status_code == 204


@responses.activate
def test_play_audio_into_call():
    uuid = 'e154eb57-2962-41e7-baf4-90f63e25e439'
    build_response(
        path,
        'PUT',
        f'https://api.nexmo.com/v1/calls/{uuid}/stream',
        'play_audio_into_call.json',
    )

    options = AudioStreamOptions(
        stream_url=['https://example.com/audio'], loop=2, level=0.5
    )
    response = voice.play_audio_into_call(uuid, options)
    assert response.message == 'Stream started'
    assert response.uuid == uuid


@responses.activate
def test_stop_audio_stream():
    uuid = 'e154eb57-2962-41e7-baf4-90f63e25e439'
    build_response(
        path,
        'DELETE',
        f'https://api.nexmo.com/v1/calls/{uuid}/stream',
        'stop_audio_stream.json',
    )

    response = voice.stop_audio_stream(uuid)
    assert response.message == 'Stream stopped'
    assert response.uuid == uuid


@responses.activate
def test_play_tts_into_call():
    uuid = 'e154eb57-2962-41e7-baf4-90f63e25e439'
    build_response(
        path,
        'PUT',
        f'https://api.nexmo.com/v1/calls/{uuid}/talk',
        'play_tts_into_call.json',
    )

    options = TtsStreamOptions(
        text='Hello world', language='en-ZA', style=1, premium=False, loop=2, level=0.5
    )
    response = voice.play_tts_into_call(uuid, options)
    assert response.message == 'Talk started'
    assert response.uuid == uuid


@responses.activate
def test_stop_tts():
    uuid = 'e154eb57-2962-41e7-baf4-90f63e25e439'
    build_response(
        path,
        'DELETE',
        f'https://api.nexmo.com/v1/calls/{uuid}/talk',
        'stop_tts.json',
    )

    response = voice.stop_tts(uuid)
    assert response.message == 'Talk stopped'
    assert response.uuid == uuid


@responses.activate
def test_play_dtmf_into_call():
    uuid = 'e154eb57-2962-41e7-baf4-90f63e25e439'
    build_response(
        path,
        'PUT',
        f'https://api.nexmo.com/v1/calls/{uuid}/dtmf',
        'play_dtmf_into_call.json',
    )

    response = voice.play_dtmf_into_call(uuid, dtmf='1234*#')
    assert response.message == 'DTMF sent'
    assert response.uuid == uuid

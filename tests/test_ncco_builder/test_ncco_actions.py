from vonage import Ncco, ConnectEndpoints
import ncco_samples.ncco_action_samples as nas

import json
import pytest
from pydantic import ValidationError


def _action_as_dict(action: Ncco.Action):
    return action.dict(exclude_none=True)


def test_record_full():
    record = Ncco.Record(
        format='wav',
        split='conversation',
        channels=4,
        endOnSilence=5,
        endOnKey='*',
        timeOut=100,
        beepStart=True,
        eventUrl=['http://example.com'],
        eventMethod='PUT',
    )
    assert type(record) == Ncco.Record
    assert json.dumps(_action_as_dict(record)) == nas.record_full


def test_record_url_passed_as_str():
    record = Ncco.Record(eventUrl='http://example.com/events')
    assert json.dumps(_action_as_dict(record)) == nas.record_url_as_str


def test_record_channels_adds_split_parameter():
    record = Ncco.Record(channels=4)
    assert json.dumps(_action_as_dict(record)) == nas.record_add_split


def test_record_model_errors():
    with pytest.raises(ValidationError):
        Ncco.Record(format='mp4')
    with pytest.raises(ValidationError):
        Ncco.Record(endOnKey='asdf')


def test_conversation_basic():
    conversation = Ncco.Conversation(name='my_conversation')
    assert type(conversation) == Ncco.Conversation
    assert json.dumps(_action_as_dict(conversation)) == nas.conversation_basic


def test_conversation_full():
    conversation = Ncco.Conversation(
        name='my_conversation',
        musicOnHoldUrl='http://example.com/music.mp3',
        startOnEnter=True,
        endOnExit=True,
        record=True,
        canSpeak=['asdf', 'qwer'],
        canHear=['asdf'],
    )
    assert json.dumps(_action_as_dict(conversation)) == nas.conversation_full


def test_conversation_field_type_error():
    with pytest.raises(ValidationError):
        Ncco.Conversation(name='my_conversation', startOnEnter='asdf')


def test_conversation_mute():
    conversation = Ncco.Conversation(name='my_conversation', mute=True)
    assert json.dumps(_action_as_dict(conversation)) == nas.conversation_mute_option


def test_conversation_incompatible_options_error():
    with pytest.raises(ValidationError) as err:
        Ncco.Conversation(name='my_conversation', canSpeak=['asdf', 'qwer'], mute=True)
    str(err.value) == 'Cannot use mute option if canSpeak option is specified.+'


def test_connect_phone_endpoint_from_dict():
    connect = Ncco.Connect(
        endpoint={
            "type": "phone",
            "number": "447000000000",
            "dtmfAnswer": "1p2p3p#**903#",
            "onAnswer": {"url": "https://example.com/answer", "ringbackTone": "http://example.com/ringbackTone.wav"},
        }
    )
    assert type(connect) is Ncco.Connect
    assert json.dumps(_action_as_dict(connect)) == nas.connect_phone


def test_connect_phone_endpoint_from_list():
    connect = Ncco.Connect(
        endpoint=[
            {
                "type": "phone",
                "number": "447000000000",
                "dtmfAnswer": "1p2p3p#**903#",
                "onAnswer": {
                    "url": "https://example.com/answer",
                    "ringbackTone": "http://example.com/ringbackTone.wav",
                },
            }
        ]
    )
    assert json.dumps(_action_as_dict(connect)) == nas.connect_phone


def test_connect_options():
    endpoint = ConnectEndpoints.PhoneEndpoint(number='447000000000')
    connect = Ncco.Connect(
        endpoint=endpoint,
        from_='447400000000',
        randomFromNumber=False,
        eventType='synchronous',
        timeout=15,
        limit=1000,
        machineDetection='hangup',
        eventUrl='http://example.com',
        eventMethod='PUT',
        ringbackTone='http://example.com',
    )
    assert json.dumps(_action_as_dict(connect)) == nas.connect_full


def test_connect_all_endpoints_from_model():
    phone = ConnectEndpoints.PhoneEndpoint(
        number='447000000000',
        dtmfAnswer='1p2p3p#**903#',
        onAnswer={"url": "https://example.com/answer", "ringbackTone": "http://example.com/ringbackTone.wav"},
    )
    connect_phone = Ncco.Connect(endpoint=phone)
    assert json.dumps(_action_as_dict(connect_phone)) == nas.connect_phone

    app = ConnectEndpoints.AppEndpoint(user='test_user')
    connect_app = Ncco.Connect(endpoint=app)
    assert json.dumps(_action_as_dict(connect_app)) == nas.connect_app

    websocket = ConnectEndpoints.WebsocketEndpoint(
        uri='ws://example.com/socket', contentType='audio/l16;rate=8000', headers={"language": "en-GB"}
    )
    connect_websocket = Ncco.Connect(endpoint=websocket)
    assert json.dumps(_action_as_dict(connect_websocket)) == nas.connect_websocket

    sip = ConnectEndpoints.SipEndpoint(
        uri='sip:rebekka@sip.mcrussell.com', headers={"location": "New York City", "occupation": "developer"}
    )
    connect_sip = Ncco.Connect(endpoint=sip)
    assert json.dumps(_action_as_dict(connect_sip)) == nas.connect_sip

    vbc = ConnectEndpoints.VbcEndpoint(extension='111')
    connect_vbc = Ncco.Connect(endpoint=vbc)
    assert json.dumps(_action_as_dict(connect_vbc)) == nas.connect_vbc


def test_connect_endpoints_errors():
    with pytest.raises(ValidationError) as err:
        ConnectEndpoints.PhoneEndpoint(number='447000000000', onAnswer={'url': 'not-a-valid-url'})

    with pytest.raises(ValidationError) as err:
        ConnectEndpoints.PhoneEndpoint(
            number='447000000000',
            onAnswer={'url': 'http://example.com/answer', 'ringbackTone': 'not-a-valid-url'},
        )

    with pytest.raises(ValueError) as err:
        ConnectEndpoints.create_endpoint_model_from_dict({'type': 'carrier_pigeon'})
    assert (
        str(err.value)
        == 'Invalid "type" specified for endpoint object. Cannot create a ConnectEndpoints.Endpoint model.'
    )


def test_connect_random_from_number_error():
    endpoint = ConnectEndpoints.PhoneEndpoint(number='447000000000')
    with pytest.raises(ValueError) as err:
        Ncco.Connect(endpoint=endpoint, from_='447400000000', randomFromNumber=True)

    assert 'Cannot set a "from" ("from_") field and also the "randomFromNumber" = True option' in str(err.value)


def test_connect_validation_errors():
    endpoint = ConnectEndpoints.PhoneEndpoint(number='447000000000')
    with pytest.raises(ValidationError):
        Ncco.Connect(endpoint=endpoint, from_=1234)
    with pytest.raises(ValidationError):
        Ncco.Connect(endpoint=endpoint, eventType='asynchronous')
    with pytest.raises(ValidationError):
        Ncco.Connect(endpoint=endpoint, limit=7201)
    with pytest.raises(ValidationError):
        Ncco.Connect(endpoint=endpoint, machineDetection='do_nothing')


def test_talk_basic():
    talk = Ncco.Talk(text='hello')
    assert type(talk) == Ncco.Talk
    assert json.dumps(_action_as_dict(talk)) == nas.talk_basic


def test_talk_optional_params():
    talk = Ncco.Talk(text='hello', bargeIn=True, loop=3, level=0.5, language='en-GB', style=1, premium=True)
    assert json.dumps(_action_as_dict(talk)) == nas.talk_full


def test_talk_validation_error():
    with pytest.raises(ValidationError):
        Ncco.Talk(text='hello', bargeIn='go ahead')


def test_stream_basic():
    stream = Ncco.Stream(streamUrl='https://example.com/stream/music.mp3')
    assert type(stream) == Ncco.Stream
    assert json.dumps(_action_as_dict(stream)) == nas.stream_basic


def test_stream_full():
    stream = Ncco.Stream(streamUrl='https://example.com/stream/music.mp3', level=0.1, bargeIn=True, loop=10)
    assert json.dumps(_action_as_dict(stream)) == nas.stream_full


def test_stream_error():
    with pytest.raises(ValidationError):
        Ncco.Stream(streamUrl='not_a_url')


def test_input_basic():
    input = Ncco.Input(type='dtmf')
    assert type(input) == Ncco.Input
    assert json.dumps(_action_as_dict(input)) == nas.input_basic_dtmf


def test_input_basic_list():
    input = Ncco.Input(type=['dtmf', 'speech'])
    assert json.dumps(_action_as_dict(input)) == nas.input_basic_dtmf_speech


def test_input_dtmf_options():
    ...


def test_notify_basic():
    notify = Ncco.Notify(payload={"message": "hello"}, eventUrl=["http://example.com"])
    assert type(notify) == Ncco.Notify
    assert json.dumps(_action_as_dict(notify)) == nas.notify_basic


def test_notify_basic_str_in_event_url():
    notify = Ncco.Notify(payload={"message": "hello"}, eventUrl="http://example.com")
    assert type(notify) == Ncco.Notify
    assert json.dumps(_action_as_dict(notify)) == nas.notify_basic


def test_notify_full():
    notify = Ncco.Notify(payload={"message": "hello"}, eventUrl=["http://example.com"], eventMethod='POST')
    assert type(notify) == Ncco.Notify
    assert json.dumps(_action_as_dict(notify)) == nas.notify_full


def test_notify_validation_error():
    with pytest.raises(ValidationError):
        Ncco.Notify(payload={"message": "hello"}, eventUrl=["not-a-valid-url"])


def test_build_ncco_from_notify_actions():
    notify1 = Ncco.Notify(payload={"message": "hello"}, eventUrl=["http://example.com"])
    notify2 = Ncco.Notify(payload={"message": "world"}, eventUrl=["http://example.com"], eventMethod='PUT')
    ncco = Ncco.build_ncco(notify1, notify2)
    assert ncco == nas.two_notify_ncco

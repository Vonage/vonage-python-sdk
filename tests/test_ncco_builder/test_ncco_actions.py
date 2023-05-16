from vonage import Ncco, ConnectEndpoints, InputTypes, PayPrompts
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


def test_connect_advanced_machine_detection():
    advancedMachineDetectionParams = {'behavior': 'continue', 'mode': 'detect'}
    endpoint = ConnectEndpoints.PhoneEndpoint(number='447000000000')
    connect = Ncco.Connect(
        endpoint=endpoint,
        from_='447400000000',
        advancedMachineDetection=advancedMachineDetectionParams,
        eventUrl='http://example.com',
    )
    assert json.dumps(_action_as_dict(connect)) == nas.connect_advancedMachineDetection


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
    with pytest.raises(ValidationError):
        Ncco.Connect(endpoint=endpoint, advancedMachineDetection={'behavior': 'do_nothing'})
    with pytest.raises(ValidationError):
        Ncco.Connect(endpoint=endpoint, advancedMachineDetection={'mode': 'detect_nothing'})


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


def test_input_basic():
    input = Ncco.Input(type='dtmf')
    assert type(input) == Ncco.Input
    assert json.dumps(_action_as_dict(input)) == nas.input_basic_dtmf


def test_input_basic_list():
    input = Ncco.Input(type=['dtmf', 'speech'])
    assert json.dumps(_action_as_dict(input)) == nas.input_basic_dtmf_speech


def test_input_dtmf_and_speech_options():
    dtmf = InputTypes.Dtmf(timeOut=5, maxDigits=12, submitOnHash=True)
    speech = InputTypes.Speech(
        uuid='my-uuid',
        endOnSilence=2.5,
        language='en-GB',
        context=['sales', 'billing'],
        startTimeout=20,
        maxDuration=30,
        saveAudio=True,
    )
    input = Ncco.Input(
        type=['dtmf', 'speech'], dtmf=dtmf, speech=speech, eventUrl='http://example.com/speech', eventMethod='put'
    )
    assert json.dumps(_action_as_dict(input)) == nas.input_dtmf_and_speech_full


def test_input_validation_error():
    with pytest.raises(ValidationError):
        Ncco.Input(type='invalid_type')


def test_notify_basic():
    notify = Ncco.Notify(payload={'message': 'hello'}, eventUrl=['http://example.com'])
    assert type(notify) == Ncco.Notify
    assert json.dumps(_action_as_dict(notify)) == nas.notify_basic


def test_notify_basic_str_in_event_url():
    notify = Ncco.Notify(payload={'message': 'hello'}, eventUrl='http://example.com')
    assert type(notify) == Ncco.Notify
    assert json.dumps(_action_as_dict(notify)) == nas.notify_basic


def test_notify_full():
    notify = Ncco.Notify(payload={'message': 'hello'}, eventUrl=['http://example.com'], eventMethod='POST')
    assert type(notify) == Ncco.Notify
    assert json.dumps(_action_as_dict(notify)) == nas.notify_full


def test_notify_validation_error():
    with pytest.raises(ValidationError):
        Ncco.Notify(payload={'message', 'hello'}, eventUrl=['http://example.com'])


def test_pay_voice_basic():
    pay = Ncco.Pay(amount='10.00')
    assert type(pay) == Ncco.Pay
    assert json.dumps(_action_as_dict(pay)) == nas.pay_basic


def test_pay_voice_full():
    voice_settings = PayPrompts.VoicePrompt(language='en-GB', style=1)
    pay = Ncco.Pay(amount=99.99, currency='gbp', eventUrl='https://example.com/payment', voice=voice_settings)
    assert json.dumps(_action_as_dict(pay)) == nas.pay_voice_full


def test_pay_text():
    text_prompts = PayPrompts.TextPrompt(
        type='CardNumber',
        text='Enter your card number.',
        errors={'InvalidCardType': {'text': 'The card you are trying to use is not valid for this purchase.'}},
    )
    pay = Ncco.Pay(amount=12.345, currency='gbp', eventUrl='https://example.com/payment', prompts=text_prompts)
    assert json.dumps(_action_as_dict(pay)) == nas.pay_text


def test_pay_text_multiple_prompts():
    card_prompt = PayPrompts.TextPrompt(
        type='CardNumber',
        text='Enter your card number.',
        errors={'InvalidCardType': {'text': 'The card you are trying to use is not valid for this purchase.'}},
    )
    expiration_date_prompt = PayPrompts.TextPrompt(
        type='ExpirationDate',
        text='Enter your card expiration date.',
        errors={
            'InvalidExpirationDate': {'text': 'You have entered an invalid expiration date.'},
            'Timeout': {'text': 'Please enter your card\'s expiration date.'},
        },
    )
    security_code_prompt = PayPrompts.TextPrompt(
        type='SecurityCode',
        text='Enter your 3-digit security code.',
        errors={
            'InvalidSecurityCode': {'text': 'You have entered an invalid security code.'},
            'Timeout': {'text': 'Please enter your card\'s security code.'},
        },
    )

    text_prompts = [card_prompt, expiration_date_prompt, security_code_prompt]
    pay = Ncco.Pay(amount=12, prompts=text_prompts)
    assert json.dumps(_action_as_dict(pay)) == nas.pay_text_multiple_prompts


def test_pay_validation_error():
    with pytest.raises(ValidationError):
        Ncco.Pay(amount='not-valid')

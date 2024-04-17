from pytest import raises
from vonage_voice.errors import NccoActionError
from vonage_voice.models import connect_endpoints, ncco
from vonage_voice.models.common import AdvancedMachineDetection


def test_record_basic():
    record = ncco.Record()
    assert record.model_dump(by_alias=True, exclude_none=True) == {'action': 'record'}


def test_record_full():
    record = ncco.Record(
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
    record_dict = {
        'format': 'wav',
        'split': 'conversation',
        'channels': 4,
        'endOnSilence': 5,
        'endOnKey': '*',
        'timeOut': 100,
        'beepStart': True,
        'eventUrl': ['http://example.com'],
        'eventMethod': 'PUT',
        'action': 'record',
    }
    assert record.model_dump(by_alias=True, exclude_none=True) == record_dict


def test_record_channels_adds_split_parameter():
    record = ncco.Record(channels=4)
    assert record.model_dump(by_alias=True, exclude_none=True) == {
        'channels': 4,
        'split': 'conversation',
        'action': 'record',
    }


def test_conversation_basic():
    conversation = ncco.Conversation(name='my_conversation')
    assert conversation.model_dump(by_alias=True, exclude_none=True) == {
        'name': 'my_conversation',
        'action': 'conversation',
    }


def test_conversation_full():
    conversation = ncco.Conversation(
        name='my_conversation',
        musicOnHoldUrl=['http://example.com/music.mp3'],
        startOnEnter=True,
        endOnExit=True,
        record=True,
        canSpeak=['asdf', 'qwer'],
        canHear=['asdf'],
        mute=False,
    )
    conversation_dict = {
        'name': 'my_conversation',
        'musicOnHoldUrl': ['http://example.com/music.mp3'],
        'startOnEnter': True,
        'endOnExit': True,
        'record': True,
        'canSpeak': ['asdf', 'qwer'],
        'canHear': ['asdf'],
        'mute': False,
        'action': 'conversation',
    }
    assert conversation.model_dump(by_alias=True, exclude_none=True) == conversation_dict


def test_conversation_mute():
    with raises(NccoActionError) as e:
        ncco.Conversation(name='my_conversation', canSpeak=['asdf'], mute=True)
    assert e.match('Cannot use mute option if canSpeak option is specified.')


def test_create_connect_endpoints():
    assert connect_endpoints.PhoneEndpoint(
        number='447000000000',
        dtmfAnswer='1234',
        onAnswer={'url': 'https://example.com', 'ringbackTone': 'http://example.com'},
    ).model_dump() == {
        'number': '447000000000',
        'dtmfAnswer': '1234',
        'onAnswer': {'url': 'https://example.com', 'ringbackTone': 'http://example.com'},
        'type': 'phone',
    }

    assert connect_endpoints.AppEndpoint(user='my_user').model_dump() == {
        'user': 'my_user',
        'type': 'app',
    }

    assert connect_endpoints.WebsocketEndpoint(
        uri='wss://example.com',
        contentType='audio/l16;rate=8000',
        headers={'asdf': 'qwer'},
    ).model_dump(by_alias=True) == {
        'uri': 'wss://example.com',
        'content-type': 'audio/l16;rate=8000',
        'headers': {'asdf': 'qwer'},
        'type': 'websocket',
    }

    assert connect_endpoints.SipEndpoint(
        uri='sip:example@sip.example.com', headers={'qwer': 'asdf'}
    ).model_dump() == {
        'uri': 'sip:example@sip.example.com',
        'headers': {'qwer': 'asdf'},
        'type': 'sip',
    }

    assert connect_endpoints.VbcEndpoint(extension='1234').model_dump() == {
        'extension': '1234',
        'type': 'vbc',
    }


def test_connect_basic():
    endpoint = connect_endpoints.PhoneEndpoint(number='447000000000')
    connect = ncco.Connect(endpoint=[endpoint], from_='1234567890')
    assert connect.model_dump(by_alias=True, exclude_none=True) == {
        'endpoint': [{'type': 'phone', 'number': '447000000000'}],
        'from': '1234567890',
        'action': 'connect',
    }


def test_connect_advanced_machine_detection():
    amd = AdvancedMachineDetection(behavior='continue', mode='detect', beep_timeout=60)

    assert amd.model_dump() == {
        'behavior': 'continue',
        'mode': 'detect',
        'beep_timeout': 60,
    }

    endpoint = connect_endpoints.PhoneEndpoint(number='447000000000')
    assert ncco.Connect(
        endpoint=[endpoint],
        from_='1234567890',
        advancedMachineDetection=amd,
    ).model_dump(by_alias=True, exclude_none=True) == {
        'endpoint': [{'type': 'phone', 'number': '447000000000'}],
        'from': '1234567890',
        'advancedMachineDetection': {
            'behavior': 'continue',
            'mode': 'detect',
            'beep_timeout': 60,
        },
        'action': 'connect',
    }


def test_connect_options():
    endpoint = connect_endpoints.PhoneEndpoint(number='447000000000')
    connect = ncco.Connect(
        endpoint=[endpoint],
        randomFromNumber=True,
        eventType='synchronous',
        timeout=15,
        limit=1000,
        machineDetection='hangup',
        eventUrl=['http://example.com'],
        eventMethod='PUT',
        ringbackTone=['http://example.com'],
    )
    assert connect.model_dump(by_alias=True, exclude_none=True) == {
        'endpoint': [{'type': 'phone', 'number': '447000000000'}],
        'randomFromNumber': True,
        'eventType': 'synchronous',
        'timeout': 15,
        'limit': 1000,
        'machineDetection': 'hangup',
        'eventUrl': ['http://example.com'],
        'eventMethod': 'PUT',
        'ringbackTone': ['http://example.com'],
        'action': 'connect',
    }


def test_connect_random_from_number_error():
    endpoint = connect_endpoints.PhoneEndpoint(number='447000000000')
    with raises(NccoActionError) as e:
        ncco.Connect(endpoint=[endpoint])

    assert e.match('Either `from_` or `random_from_number` must be set.')

    with raises(NccoActionError) as e:
        ncco.Connect(endpoint=[endpoint], from_='1234567890', randomFromNumber=True)
    assert e.match('`from_` and `random_from_number` cannot be used together.')


def test_talk_basic():
    talk = ncco.Talk(text='hello')
    assert talk.model_dump(by_alias=True, exclude_none=True) == {
        'text': 'hello',
        'action': 'talk',
    }


def test_talk_optional_params():
    talk = ncco.Talk(
        text='hello',
        bargeIn=True,
        loop=3,
        level=0.5,
        language='en-GB',
        style=1,
        premium=True,
    )
    assert talk.model_dump(by_alias=True, exclude_none=True) == {
        'text': 'hello',
        'bargeIn': True,
        'loop': 3,
        'level': 0.5,
        'language': 'en-GB',
        'style': 1,
        'premium': True,
        'action': 'talk',
    }


# def test_stream_basic():
#     stream = Ncco.Stream(streamUrl='https://example.com/stream/music.mp3')
#     assert type(stream) == Ncco.Stream
#     assert json.dumps(_action_as_dict(stream)) == nas.stream_basic


# def test_stream_full():
#     stream = Ncco.Stream(
#         streamUrl='https://example.com/stream/music.mp3', level=0.1, bargeIn=True, loop=10
#     )
#     assert json.dumps(_action_as_dict(stream)) == nas.stream_full


# def test_input_basic():
#     input = Ncco.Input(type='dtmf')
#     assert type(input) == Ncco.Input
#     assert json.dumps(_action_as_dict(input)) == nas.input_basic_dtmf


# def test_input_basic_list():
#     input = Ncco.Input(type=['dtmf', 'speech'])
#     assert json.dumps(_action_as_dict(input)) == nas.input_basic_dtmf_speech


# def test_input_dtmf_and_speech_options():
#     dtmf = InputTypes.Dtmf(timeOut=5, maxDigits=12, submitOnHash=True)
#     speech = InputTypes.Speech(
#         uuid='my-uuid',
#         endOnSilence=2.5,
#         language='en-GB',
#         context=['sales', 'billing'],
#         startTimeout=20,
#         maxDuration=30,
#         saveAudio=True,
#     )
#     input = Ncco.Input(
#         type=['dtmf', 'speech'],
#         dtmf=dtmf,
#         speech=speech,
#         eventUrl='http://example.com/speech',
#         eventMethod='put',
#     )
#     assert json.dumps(_action_as_dict(input)) == nas.input_dtmf_and_speech_full


# def test_input_validation_error():
#     with pytest.raises(ValidationError):
#         Ncco.Input(type='invalid_type')


# def test_notify_basic():
#     notify = Ncco.Notify(payload={'message': 'hello'}, eventUrl=['http://example.com'])
#     assert type(notify) == Ncco.Notify
#     assert json.dumps(_action_as_dict(notify)) == nas.notify_basic


# def test_notify_basic_str_in_event_url():
#     notify = Ncco.Notify(payload={'message': 'hello'}, eventUrl='http://example.com')
#     assert type(notify) == Ncco.Notify
#     assert json.dumps(_action_as_dict(notify)) == nas.notify_basic


# def test_notify_full():
#     notify = Ncco.Notify(
#         payload={'message': 'hello'}, eventUrl=['http://example.com'], eventMethod='POST'
#     )
#     assert type(notify) == Ncco.Notify
#     assert json.dumps(_action_as_dict(notify)) == nas.notify_full


# def test_notify_validation_error():
#     with pytest.raises(ValidationError):
#         Ncco.Notify(payload={'message', 'hello'}, eventUrl=['http://example.com'])


# def test_pay_voice_basic():
#     pay = Ncco.Pay(amount='10.00')
#     assert type(pay) == Ncco.Pay
#     assert json.dumps(_action_as_dict(pay)) == nas.pay_basic


# def test_pay_voice_full():
#     voice_settings = PayPrompts.VoicePrompt(language='en-GB', style=1)
#     pay = Ncco.Pay(
#         amount=99.99,
#         currency='gbp',
#         eventUrl='https://example.com/payment',
#         voice=voice_settings,
#     )
#     assert json.dumps(_action_as_dict(pay)) == nas.pay_voice_full


# def test_pay_text():
#     text_prompts = PayPrompts.TextPrompt(
#         type='CardNumber',
#         text='Enter your card number.',
#         errors={
#             'InvalidCardType': {
#                 'text': 'The card you are trying to use is not valid for this purchase.'
#             }
#         },
#     )
#     pay = Ncco.Pay(
#         amount=12.345,
#         currency='gbp',
#         eventUrl='https://example.com/payment',
#         prompts=text_prompts,
#     )
#     assert json.dumps(_action_as_dict(pay)) == nas.pay_text


# def test_pay_text_multiple_prompts():
#     card_prompt = PayPrompts.TextPrompt(
#         type='CardNumber',
#         text='Enter your card number.',
#         errors={
#             'InvalidCardType': {
#                 'text': 'The card you are trying to use is not valid for this purchase.'
#             }
#         },
#     )
#     expiration_date_prompt = PayPrompts.TextPrompt(
#         type='ExpirationDate',
#         text='Enter your card expiration date.',
#         errors={
#             'InvalidExpirationDate': {
#                 'text': 'You have entered an invalid expiration date.'
#             },
#             'Timeout': {'text': 'Please enter your card\'s expiration date.'},
#         },
#     )
#     security_code_prompt = PayPrompts.TextPrompt(
#         type='SecurityCode',
#         text='Enter your 3-digit security code.',
#         errors={
#             'InvalidSecurityCode': {'text': 'You have entered an invalid security code.'},
#             'Timeout': {'text': 'Please enter your card\'s security code.'},
#         },
#     )

#     text_prompts = [card_prompt, expiration_date_prompt, security_code_prompt]
#     pay = Ncco.Pay(amount=12, prompts=text_prompts)
#     assert json.dumps(_action_as_dict(pay)) == nas.pay_text_multiple_prompts


# def test_pay_validation_error():
#     with pytest.raises(ValidationError):
#         Ncco.Pay(amount='not-valid')

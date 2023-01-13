from vonage import Ncco, ConnectEndpoints, InputTypes, PayPrompts

record = Ncco.Record(eventUrl='http://example.com/events')

conversation = Ncco.Conversation(name='my_conversation')

connect = Ncco.Connect(
    endpoint=ConnectEndpoints.PhoneEndpoint(number='447000000000'),
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

talk_minimal = Ncco.Talk(text='hello')

talk = Ncco.Talk(text='hello', bargeIn=True, loop=3, level=0.5, language='en-GB', style=1, premium=True)

stream = Ncco.Stream(streamUrl='https://example.com/stream/music.mp3', level=0.1, bargeIn=True, loop=10)

input = Ncco.Input(
    type=['dtmf', 'speech'],
    dtmf=InputTypes.Dtmf(timeOut=5, maxDigits=12, submitOnHash=True),
    speech=InputTypes.Speech(
        uuid='my-uuid',
        endOnSilence=2.5,
        language='en-GB',
        context=['sales', 'billing'],
        startTimeout=20,
        maxDuration=30,
        saveAudio=True,
    ),
    eventUrl='http://example.com/speech',
    eventMethod='put',
)

notify = Ncco.Notify(payload={"message": "world"}, eventUrl=["http://example.com"], eventMethod='PUT')

pay_voice_prompt = Ncco.Pay(
    amount=99.99,
    currency='gbp',
    eventUrl='https://example.com/payment',
    voice=PayPrompts.VoicePrompt(language='en-GB', style=1),
)

pay_text_prompt = Ncco.Pay(
    amount=12.345,
    currency='gbp',
    eventUrl='https://example.com/payment',
    prompts=PayPrompts.TextPrompt(
        type='CardNumber',
        text='Enter your card number.',
        errors={'InvalidCardType': {'text': 'The card you are trying to use is not valid for this purchase.'}},
    ),
)

basic_ncco = [{"action": "talk", "text": "hello"}]

two_part_ncco = [
    {
        'action': 'record',
        'eventUrl': ['http://example.com/events'],
    },
    {'action': 'talk', 'text': 'hello'},
]

insane_ncco = ''

from pydantic import BaseModel, ValidationError, HttpUrl, AnyUrl, Field, validator, constr, confloat, conint
from typing import Optional, Union, List
from typing_extensions import Literal
import json


class ConnectEndpoints:
    class Endpoint(BaseModel):
        type: Field('endpoint', const=True)

    class PhoneEndpoint(Endpoint):
        type: Field('phone', const=True)
        number: constr(regex=r'^[1-9]\d{6,14}$')
        dtmfAnswer: Optional[constr(regex=asdf '^[0-9*#]$')]

    class AppEndpoint(Endpoint):
        ...

    class WebsocketEndpoint(Endpoint):
        ...

    class SipEndpoint(Endpoint):
        ...

    class VbcEndpoint(Endpoint):
        ...


class Ncco:
    class Action(BaseModel):
        action: str = None

    class Record(Action):
        """Use the record action to record a call or part of a call."""

        action = Field('record', const=True)
        format: Optional[Literal['mp3', 'wav', 'ogg']]
        split: Optional[Literal['conversation']]
        channels: Optional[conint(ge=1, le=32)]
        endOnSilence: Optional[conint(ge=3, le=10)]
        endOnKey: Optional[constr(regex='^[0-9*#]$')]
        timeOut: Optional[conint(ge=3, le=7200)]
        beepStart: Optional[bool]
        eventUrl: Optional[Union[List[HttpUrl], HttpUrl]]
        eventMethod: Optional[constr(to_upper=True)]

        @validator('channels')
        def enable_split(cls, v, values):
            if values['split'] is None:
                values['split'] = 'conversation'
            return v

        @validator('eventUrl')
        def validate_url(cls, v):
            return Ncco._ensure_object_in_list(v)

    class Conversation(Action):
        """You can use the conversation action to create standard or moderated conferences,
        while preserving the communication context.
        Using conversation with the same name reuses the same persisted conversation."""

        action = Field('notify', const=True)
        name: str
        musicOnHoldUrl: Optional[Union[List[AnyUrl], AnyUrl]]
        startOnEnter: Optional[bool]
        endOnExit: Optional[bool]
        record: Optional[bool]
        canSpeak: Optional[List[str]]
        canHear: Optional[List[str]]
        mute: Optional[bool]

        @validator('musicOnHoldUrl')
        def validate_url(cls, v):
            return Ncco._ensure_object_in_list(v)

        @validator('mute')
        def can_mute(cls, v, values):
            if 'canSpeak' in values and values['canSpeak'] is not None:
                raise ValidationError('Cannot use mute option if canSpeak option is specified.')
            return v

    class Connect(Action):
        """You can use the connect action to connect a call to endpoints such as phone numbers or a VBC extension."""
        
        action = Field('connect', const=True)
        endpoint: ConnectEndpoints.Endpoint
        from_: Optional[constr(regex=r'^[1-9]\d{6,14}$')]
        randomFromNumber: Optional[bool]
        eventType: Optional[Literal['synchronous']]
        timeout: Optional[int]
        limit: Optional[conint(le=7200)]
        machineDetection: Optional[Literal['continue', 'hangup']]
        eventUrl: Optional[Union[List[HttpUrl], HttpUrl]]
        eventMethod: Optional[constr(to_upper=True)]
        ringbackTone: Optional[HttpUrl]

        # @validator('endpoint')
        # def validate_endpoint(cls, v):
        #     if v['type'] == 'phone':
        #         Ncco.validate_phone()
        #     elif v['type'] == 'app':
        #         Ncco.validate_app()
        #     elif v['type'] == 'websocket':
        #         Ncco.validate_websocket()
        #     elif v['type'] == 'sip':
        #         Ncco.validate_sip()
        #     elif v['type'] == 'vbc':
        #         Ncco.validate_vbc()
        #     else:
        #         raise ValidationError('')
        #     return v

        @validator('from_')
        def set_from_field(cls, v, values):
            values['from'] = v

        @validator('randomFromNumber')
        def check_from_not_set(cls, v, values):
            if v == True and values['from'] is not None:
                raise ValidationError('Cannot set a "from" field and also the "randomFromNumber" = True option')
            return v

        @validator('eventUrl')
        def validate_url(cls, v):
            return Ncco._ensure_object_in_list(v)

    class Talk(Action):
        """The talk action sends synthesized speech to a Conversation."""

        action = Field('talk', const=True)
        text: constr(max_length=1500)
        bargeIn: Optional[bool]
        loop: Optional[int]
        level: Optional[confloat(ge=-1, le=1)]
        language: Optional[str]
        style: Optional[int]
        premium: Optional[bool]

    class Stream(Action):
        ...

    class Input(Action):
        ...

    class Notify(Action):
        """Use the notify action to send a custom payload to your event URL."""

        action = Field('notify', const=True)
        payload: dict
        eventUrl: Union[List[HttpUrl], HttpUrl]
        eventMethod: Optional[constr(to_upper=True)]

        @validator('eventUrl')
        def check_url_in_list(cls, v):
            return Ncco._ensure_object_in_list(v)

    class Pay(Action):
        ...

    @staticmethod
    def build_ncco(*args: Action):
        ncco = []
        for action in args:
            ncco.append(action.dict(exclude_none=True))
        print(f'ncco is this: {ncco}')
        print(f'json representation is this: {json.dumps(ncco)}')
        return json.dumps(ncco)

    @staticmethod
    def _ensure_object_in_list(obj):
        if type(obj) != list:
            return [obj]
        else:
            return obj


class Message(BaseModel):
    to: constr(min_length=7, max_length=15)
    sender: constr(min_length=1)
    client_ref: Optional[str]


class SmsMessage(Message):
    channel = Field(default='sms', const=True)
    message_type = Field(default='text', const=True)
    text: constr(max_length=1000)


def send_message_from_model(self, message: Message):
    params = message.dict()
    params['from'] = params.pop('sender')

    print('params = ', params)

    if self._client.jwt is None:
        self._auth_type = 'header'
    return self._client.post(
        self._client.api_host(),
        "/v1/messages",
        params,
        auth_type=self._auth_type,
    )

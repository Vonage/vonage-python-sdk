from pydantic import BaseModel, HttpUrl, AnyUrl, Field, validator, constr, confloat, conint
from typing import Optional, Union, List
from typing_extensions import Literal
import json

from .connect_endpoints import ConnectEndpoints
from .input_types import InputTypes


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
        def ensure_url_in_list(cls, v):
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
        def ensure_url_in_list(cls, v):
            return Ncco._ensure_object_in_list(v)

        @validator('mute')
        def can_mute(cls, v, values):
            if 'canSpeak' in values and values['canSpeak'] is not None:
                raise ValueError('Cannot use mute option if canSpeak option is specified.')
            return v

    class Connect(Action):
        """You can use the connect action to connect a call to endpoints such as phone numbers or a VBC extension."""

        action = Field('connect', const=True)
        endpoint: Union[dict, ConnectEndpoints.Endpoint, List[dict]]
        from_: Optional[constr(regex=r'^[1-9]\d{6,14}$')]
        randomFromNumber: Optional[bool]
        eventType: Optional[Literal['synchronous']]
        timeout: Optional[int]
        limit: Optional[conint(le=7200)]
        machineDetection: Optional[Literal['continue', 'hangup']]
        eventUrl: Optional[Union[List[HttpUrl], HttpUrl]]
        eventMethod: Optional[constr(to_upper=True)]
        ringbackTone: Optional[HttpUrl]

        @validator('endpoint')
        def validate_endpoint(cls, v):
            if type(v) is dict:
                return [ConnectEndpoints.create_endpoint_model_from_dict(v)]
            elif type(v) is list:
                return [ConnectEndpoints.create_endpoint_model_from_dict(v[0])]
            else:
                return [v]

        @validator('from_')
        def set_from_field(cls, v, values):
            values['from'] = v

        @validator('randomFromNumber')
        def check_from_not_set(cls, v, values):
            if v is True and 'from' in values:
                if values['from'] is not None:
                    raise ValueError(
                        'Cannot set a "from" ("from_") field and also the "randomFromNumber" = True option'
                    )
            return v

        @validator('eventUrl')
        def ensure_url_in_list(cls, v):
            return Ncco._ensure_object_in_list(v)

        class Config:
            smart_union = True

    class Talk(Action):
        """The talk action sends synthesized speech to a Conversation."""

        action = Field('talk', const=True)
        text: constr(max_length=1500)
        bargeIn: Optional[bool]
        loop: Optional[conint(ge=0)]
        level: Optional[confloat(ge=-1, le=1)]
        language: Optional[str]
        style: Optional[int]
        premium: Optional[bool]

    class Stream(Action):
        """The stream action allows you to send an audio stream to a Conversation."""

        action = Field('stream', const=True)
        streamUrl: Union[List[AnyUrl], AnyUrl]
        level: Optional[confloat(ge=-1, le=1)]
        bargeIn: Optional[bool]
        loop: Optional[conint(ge=0)]

        @validator('streamUrl')
        def ensure_url_in_list(cls, v):
            return Ncco._ensure_object_in_list(v)

    class Input(Action):
        """Collect digits or speech input by the person you are are calling."""

        action = Field('input', const=True)
        type: Union[
            Literal['dtmf', 'speech'], List[Literal['dtmf']], List[Literal['speech']], List[Literal['dtmf', 'speech']]
        ]
        dtmf: Optional[Union[InputTypes.Dtmf, dict]]
        speech: Optional[Union[InputTypes.Speech, dict]]
        eventUrl: Optional[Union[List[HttpUrl], HttpUrl]]
        eventMethod: Optional[constr(to_upper=True)]

        @validator('type')
        def ensure_type_in_list(cls, v):
            return Ncco._ensure_object_in_list(v)

        @validator('dtmf')
        def ensure_input_object_is_dtmf_model(cls, v):
            if type(v) is dict:
                return InputTypes.create_dtmf_model(v)
            else:
                return v

        @validator('speech')
        def ensure_input_object_is_speech_model(cls, v):
            if type(v) is dict:
                return InputTypes.create_speech_model(v)
            else:
                return v

        @validator('eventUrl')
        def ensure_url_in_list(cls, v):
            return Ncco._ensure_object_in_list(v)

    class Notify(Action):
        """Use the notify action to send a custom payload to your event URL."""

        action = Field('notify', const=True)
        payload: dict
        eventUrl: Union[List[HttpUrl], HttpUrl]
        eventMethod: Optional[constr(to_upper=True)]

        @validator('eventUrl')
        def ensure_url_in_list(cls, v):
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

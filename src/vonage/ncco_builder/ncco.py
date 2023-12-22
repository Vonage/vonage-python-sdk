from pydantic import BaseModel, Field, ValidationInfo, field_validator, constr, confloat, conint
from typing import Any, Dict,  Union, List
from typing_extensions import Annotated, Literal

from .connect_endpoints import ConnectEndpoints
from .input_types import InputTypes
from .pay_prompts import PayPrompts

from deprecated import deprecated


class Ncco:
    class Action(BaseModel):
        action: Literal['record', 'conversation', 'connect',
                        'talk', 'stream', 'input', 'notify', 'pay'] = None

    class Record(Action):
        """Use the record action to record a call or part of a call."""

        action: Literal['record'] = 'record'
        format: Literal['mp3', 'wav', 'ogg'] = None
        split: Literal['conversation'] = None
        channels: conint(ge=1, le=32) = None
        endOnSilence: conint(ge=3, le=10) = None
        endOnKey: constr(pattern='^[0-9*#]$') = None
        timeOut: conint(ge=3, le=7200) = None
        beepStart: bool = None
        eventUrl: Union[List[str], str] = None
        eventMethod: constr(to_upper=True) = None

        @field_validator('channels')
        @classmethod
        def enable_split(cls, v, info: ValidationInfo):
            values = info.data
            if values['split'] is None:
                values['split'] = 'conversation'
            return v

        @field_validator('eventUrl')
        @classmethod
        def ensure_url_in_list(cls, v):
            return Ncco._ensure_object_in_list(v)

    class Conversation(Action):
        """You can use the conversation action to create standard or moderated conferences,
        while preserving the communication context.
        Using conversation with the same name reuses the same persisted conversation."""

        action: Literal['conversation'] = 'conversation'
        name: str
        musicOnHoldUrl: Union[List[str], str] = None
        startOnEnter: bool = None
        endOnExit: bool = None
        record: bool = None
        canSpeak: List[str] = None
        canHear: List[str] = None
        mute: bool = None

        @field_validator('musicOnHoldUrl')
        @classmethod
        def ensure_url_in_list(cls, v: Any):
            return Ncco._ensure_object_in_list(v)

        @field_validator('mute')
        @classmethod
        def can_mute(cls, v, info: ValidationInfo):
            values = info.data
            if 'canSpeak' in values and values['canSpeak'] is not None:
                raise ValueError('Cannot use mute option if canSpeak option is specified.')
            return v

    class Connect(Action):
        """You can use the connect action to connect a call to endpoints such as phone numbers or a VBC extension."""

        action: Literal['connect'] = 'connect'
        endpoint: Union[dict, ConnectEndpoints.Endpoint, List]
        from_: Annotated[str, Field(alias='from_', serialization_alias='from',
                                    pattern=r'^[1-9]\d{6,14}$')] = None

        randomFromNumber: bool = None
        eventType: Literal['synchronous'] = None
        timeout: int = None
        limit: conint(le=7200) = None
        machineDetection: Literal['continue', 'hangup'] = None
        advancedMachineDetection: dict = None
        eventUrl: Union[List[str], str] = None
        eventMethod: constr(to_upper=True) = None
        ringbackTone: str = None

        @field_validator('endpoint')
        @classmethod
        def validate_endpoint(cls, v: Any):

            if type(v) is dict:
                return [ConnectEndpoints.create_endpoint_model_from_dict(v)]
            elif type(v) is list:
                return [ConnectEndpoints.create_endpoint_model_from_dict(v[0])]
            else:
                return [v]

        @field_validator('randomFromNumber')
        @classmethod
        def check_from_not_set(cls, v, info: ValidationInfo):
            values = info.data
            if v is True and 'from_' in values:
                if values['from_'] is not None:
                    raise ValueError(
                        'Cannot set a "from" ("from_") field and also the "randomFromNumber" = True option'
                    )
            return v

        @field_validator('eventUrl')
        @classmethod
        def ensure_url_in_list(cls, v):
            return Ncco._ensure_object_in_list(v)

        @field_validator('advancedMachineDetection')
        @classmethod
        def validate_advancedMachineDetection(cls, v):
            if 'behavior' in v and v['behavior'] not in ('continue', 'hangup'):
                raise ValueError(
                    'advancedMachineDetection["behavior"] must be one of: "continue", "hangup".'
                )
            if 'mode' in v and v['mode'] not in ('detect, detect_beep'):
                raise ValueError(
                    'advancedMachineDetection["mode"] must be one of: "detect", "detect_beep".'
                )
            return v

    class Talk(Action):
        """The talk action sends synthesized speech to a Conversation."""

        action: Literal['talk'] = 'talk'
        text: constr(max_length=1500)
        bargeIn: bool = None
        loop: conint(ge=0) = None
        level: confloat(ge=-1, le=1) = None
        language: str = None
        style: int = None
        premium: bool = None

    class Stream(Action):
        """The stream action allows you to send an audio stream to a Conversation."""

        action: Literal['stream'] = 'stream'
        streamUrl: Union[List[str], str]
        level: confloat(ge=-1, le=1) = None
        bargeIn: bool = None
        loop: conint(ge=0) = None

        @field_validator('streamUrl')
        @classmethod
        def ensure_url_in_list(cls, v):
            return Ncco._ensure_object_in_list(v)

    class Input(Action):
        """Collect digits or speech input by the person you are are calling."""

        action: Literal['input'] = 'input'

        type: Union[
            Literal['dtmf', 'speech'],
            List[Literal['dtmf']],
            List[Literal['speech']],
            List[Literal['dtmf', 'speech']],
        ]
        dtmf: Union[InputTypes.Dtmf, dict] = None
        speech: Union[InputTypes.Speech, dict] = None
        eventUrl: Union[List[str], str] = None
        eventMethod: constr(to_upper=True) = None

        @field_validator('type', 'eventUrl')
        @classmethod
        def ensure_value_in_list(cls, v):
            return Ncco._ensure_object_in_list(v)

        @field_validator('dtmf')
        @classmethod
        def ensure_input_object_is_dtmf_model(cls, v):
            if type(v) is dict:
                return InputTypes.create_dtmf_model(v)
            else:
                return v

        @field_validator('speech')
        @classmethod
        def ensure_input_object_is_speech_model(cls, v):
            if type(v) is dict:
                return InputTypes.create_speech_model(v)
            else:
                return v

    class Notify(Action):
        """Use the notify action to send a custom payload to your event URL."""

        action: Literal['notify'] = 'notify'

        payload: dict
        eventUrl: Union[List[str], str]
        eventMethod: constr(to_upper=True) = None

        @field_validator('eventUrl')
        @classmethod
        def ensure_url_in_list(cls, v):
            return Ncco._ensure_object_in_list(v)

    @deprecated(version='3.2.3', reason='The Pay NCCO action has been deprecated.')
    class Pay(Action):
        """The pay action collects credit card information with DTMF input in a secure (PCI-DSS compliant) way."""

        action: Literal['pay'] = 'pay'
        amount: confloat(ge=0)
        currency: constr(to_lower=True) = None
        eventUrl: Union[List[str], str] = None
        prompts: Union[List[PayPrompts.TextPrompt], PayPrompts.TextPrompt, dict] = None
        voice: Union[PayPrompts.VoicePrompt, dict] = None

        @field_validator('amount')
        @classmethod
        def round_amount(cls, v):
            return round(v, 2)

        @field_validator('eventUrl')
        @classmethod
        def ensure_url_in_list(cls, v):
            return Ncco._ensure_object_in_list(v)

        @field_validator('prompts')
        @classmethod
        def ensure_text_model(cls, v):
            if type(v) is dict:
                return PayPrompts.create_text_model(v)
            else:
                return v

        @field_validator('voice')
        @classmethod
        def ensure_voice_model(cls, v):
            if type(v) is dict:
                return PayPrompts.create_voice_model(v)
            else:
                return v

    @staticmethod
    def build_ncco(*args: Action, actions: List[Action] = None) -> str:
        ncco = []
        if actions is not None:
            for action in actions:
                ncco.append(action.model_dump(exclude_none=True, by_alias=True))
        for action in args:
            ncco.append(action.model_dump(exclude_none=True, by_alias=True))
        return ncco

    @staticmethod
    def _ensure_object_in_list(obj):
        if type(obj) != list:
            return [obj]
        else:
            return obj

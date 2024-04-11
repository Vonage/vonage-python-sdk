from pydantic import (
    AnyUrl,
    BaseModel,
    Field,
    model_validator,
    validator,
    constr,
    confloat,
    conint,
)
from typing import Optional, Union, List
from typing_extensions import Literal

from vonage_voice.errors import NccoActionError, VoiceError
from vonage_voice.models.common import AdvancedMachineDetection

from .connect_endpoints import BaseEndpoint
from .enums import NccoActionType
from .input_types import InputTypes
from vonage_utils.types import PhoneNumber


class NccoAction(BaseModel):
    """The base class for all NCCO actions.

    For more information on NCCO actions, see the Vonage API documentation."""


class Record(NccoAction):
    """Use the record action to record a call or part of a call."""

    format: Optional[Literal['mp3', 'wav', 'ogg']] = None
    split: Optional[Literal['conversation']] = None
    channels: Optional[int] = Field(None, ge=1, le=32)
    endOnSilence: Optional[int] = Field(None, ge=3, le=10)
    endOnKey: Optional[str] = Field(None, pattern=r'^[0-9#*]$')
    timeOut: Optional[int] = Field(None, ge=3, le=7200)
    beepStart: Optional[bool] = None
    eventUrl: Optional[List[AnyUrl]] = None
    eventMethod: Optional[str] = None
    action: NccoActionType = NccoActionType.RECORD

    @model_validator(mode='after')
    def enable_split(self):
        if self.channels and not self.split:
            self.split = 'conversation'
        return self


class Conversation(NccoAction):
    """You can use the conversation action to create standard or moderated conferences,
    while preserving the communication context.

    Using a conversation with the same name reuses the same persisted conversation."""

    name: str
    musicOnHoldUrl: Optional[List[AnyUrl]] = None
    startOnEnter: Optional[bool] = True
    endOnExit: Optional[bool] = False
    record: Optional[bool] = None
    canSpeak: Optional[List[str]] = None
    canHear: Optional[List[str]] = None
    mute: Optional[bool] = None
    action: NccoActionType = NccoActionType.CONVERSATION

    @model_validator(mode='after')
    def can_mute(self):
        if self.canSpeak and self.mute:
            raise NccoActionError(
                'Cannot use mute option if canSpeak option is specified.'
            )
        return self


class Connect(NccoAction):
    """You can use the connect action to connect a call to endpoints such as phone numbers or a VBC extension."""

    endpoint: List[BaseEndpoint]
    from_: Optional[PhoneNumber] = Field(None, serialization_alias='from')
    randomFromNumber: Optional[bool] = False
    eventType: Optional[Literal['synchronous']] = None
    timeout: Optional[int] = None
    limit: Optional[int] = Field(None, le=7200)
    machineDetection: Optional[Literal['continue', 'hangup']] = None
    advancedMachineDetection: Optional[AdvancedMachineDetection] = None
    eventUrl: Optional[List[AnyUrl]] = None
    eventMethod: Optional[str] = 'POST'
    ringbackTone: Optional[AnyUrl] = None
    action: NccoActionType = NccoActionType.CONNECT

    @model_validator(mode='after')
    def validate_from_and_random_from_number(self):
        if self.randomFromNumber is None and self.from_ is None:
            raise VoiceError('Either `from_` or `random_from_number` must be set')
        if self.randomFromNumber == True and self.from_ is not None:
            raise VoiceError('`from_` and `random_from_number` cannot be used together')
        return self


class Talk(NccoAction):
    """The talk action sends synthesized speech to a Conversation."""

    text: constr(max_length=1500)
    bargeIn: Optional[bool]
    loop: Optional[conint(ge=0)]
    level: Optional[confloat(ge=-1, le=1)]
    language: Optional[str]
    style: Optional[int]
    premium: Optional[bool]
    action: NccoActionType = NccoActionType.TALK


class Stream(NccoAction):
    """The stream action allows you to send an audio stream to a Conversation."""

    streamUrl: Union[List[str], str]
    level: Optional[confloat(ge=-1, le=1)]
    bargeIn: Optional[bool]
    loop: Optional[conint(ge=0)]
    action: NccoActionType = NccoActionType.STREAM

    @validator('streamUrl')
    def ensure_url_in_list(cls, v):
        return Ncco._ensure_object_in_list(v)


class Input(NccoAction):
    """Collect digits or speech input by the person you are are calling."""

    type: Union[
        Literal['dtmf', 'speech'],
        List[Literal['dtmf']],
        List[Literal['speech']],
        List[Literal['dtmf', 'speech']],
    ]
    dtmf: Optional[Union[InputTypes.Dtmf, dict]]
    speech: Optional[Union[InputTypes.Speech, dict]]
    eventUrl: Optional[Union[List[str], str]]
    eventMethod: Optional[constr(to_upper=True)]
    action: NccoActionType = NccoActionType.INPUT

    @validator('type', 'eventUrl')
    def ensure_value_in_list(cls, v):
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


class Notify(NccoAction):
    """Use the notify action to send a custom payload to your event URL."""

    payload: dict
    eventUrl: Union[List[str], str]
    eventMethod: Optional[constr(to_upper=True)]
    action: NccoActionType = NccoActionType.NOTIFY

    @validator('eventUrl')
    def ensure_url_in_list(cls, v):
        return Ncco._ensure_object_in_list(v)


@deprecated(version='3.2.3', reason='The Pay NCCO action has been deprecated.')
class Pay(NccoAction):
    """The pay action collects credit card information with DTMF input in a secure (PCI-DSS compliant) way."""

    action = Field('pay', const=True)
    amount: confloat(ge=0)
    currency: Optional[constr(to_lower=True)]
    eventUrl: Optional[Union[List[str], str]]
    prompts: Optional[Union[List[PayPrompts.TextPrompt], PayPrompts.TextPrompt, dict]]
    voice: Optional[Union[PayPrompts.VoicePrompt, dict]]

    @validator('amount')
    def round_amount(cls, v):
        return round(v, 2)

    @validator('eventUrl')
    def ensure_url_in_list(cls, v):
        return Ncco._ensure_object_in_list(v)

    @validator('prompts')
    def ensure_text_model(cls, v):
        if type(v) is dict:
            return PayPrompts.create_text_model(v)
        else:
            return v

    @validator('voice')
    def ensure_voice_model(cls, v):
        if type(v) is dict:
            return PayPrompts.create_voice_model(v)
        else:
            return v


@staticmethod
def build_ncco(*args: NccoAction, actions: List[NccoAction] = None) -> str:
    ncco = []
    if actions is not None:
        for action in actions:
            ncco.append(action.dict(exclude_none=True))
    for action in args:
        ncco.append(action.dict(exclude_none=True))
    return ncco


@staticmethod
def _ensure_object_in_list(obj):
    if type(obj) != list:
        return [obj]
    else:
        return obj

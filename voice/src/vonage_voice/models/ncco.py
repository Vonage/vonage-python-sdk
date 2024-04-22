from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field, model_validator
from vonage_utils.types import PhoneNumber
from vonage_voice.errors import NccoActionError
from vonage_voice.models.common import AdvancedMachineDetection

from .connect_endpoints import (
    AppEndpoint,
    PhoneEndpoint,
    SipEndpoint,
    VbcEndpoint,
    WebsocketEndpoint,
)
from .enums import NccoActionType
from .input_types import Dtmf, Speech


class NccoAction(BaseModel):
    """The base class for all NCCO actions.

    For more information on NCCO actions, see the Vonage API documentation.
    """


class Record(NccoAction):
    """Use the Record action to record a call or part of a call."""

    format: Optional[Literal['mp3', 'wav', 'ogg']] = None
    split: Optional[Literal['conversation']] = None
    channels: Optional[int] = Field(None, ge=1, le=32)
    endOnSilence: Optional[int] = Field(None, ge=3, le=10)
    endOnKey: Optional[str] = Field(None, pattern=r'^[0-9#*]$')
    timeOut: Optional[int] = Field(None, ge=3, le=7200)
    beepStart: Optional[bool] = None
    eventUrl: Optional[List[str]] = None
    eventMethod: Optional[str] = None
    action: NccoActionType = NccoActionType.RECORD

    @model_validator(mode='after')
    def enable_split(self):
        if self.channels and not self.split:
            self.split = 'conversation'
        return self


class Conversation(NccoAction):
    """You can use the Conversation action to create standard or moderated conferences, while
    preserving the communication context.

    Using a conversation with the same name reuses the same persisted conversation.
    """

    name: str
    musicOnHoldUrl: Optional[List[str]] = None
    startOnEnter: Optional[bool] = None
    endOnExit: Optional[bool] = None
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
    """You can use the Connect action to connect a call to endpoints such as phone numbers or a VBC
    extension."""

    endpoint: List[
        Union[PhoneEndpoint, AppEndpoint, WebsocketEndpoint, SipEndpoint, VbcEndpoint]
    ]
    from_: Optional[PhoneNumber] = Field(None, serialization_alias='from')
    randomFromNumber: Optional[bool] = None
    eventType: Optional[Literal['synchronous']] = None
    timeout: Optional[int] = None
    limit: Optional[int] = Field(None, le=7200)
    machineDetection: Optional[Literal['continue', 'hangup']] = None
    advancedMachineDetection: Optional[AdvancedMachineDetection] = None
    eventUrl: Optional[List[str]] = None
    eventMethod: Optional[str] = None
    ringbackTone: Optional[List[str]] = None
    action: NccoActionType = NccoActionType.CONNECT

    @model_validator(mode='after')
    def validate_from_and_random_from_number(self):
        if self.randomFromNumber is None and self.from_ is None:
            raise NccoActionError('Either `from_` or `random_from_number` must be set.')
        if self.randomFromNumber == True and self.from_ is not None:
            raise NccoActionError(
                '`from_` and `random_from_number` cannot be used together.'
            )
        return self


class Talk(NccoAction):
    """The Talk action sends synthesized speech to a Conversation.

    For valid languages, see the Vonage API documentation.
    https://developer.vonage.com/en/voice/voice-api/concepts/text-to-speech#supported-languages
    """

    text: str = Field(..., max_length=1500)
    bargeIn: Optional[bool] = None
    loop: Optional[int] = Field(None, ge=0)
    level: Optional[float] = Field(None, ge=-1, le=1)
    language: Optional[str] = None
    style: Optional[int] = None
    premium: Optional[bool] = None
    action: NccoActionType = NccoActionType.TALK


class Stream(NccoAction):
    """The stream action allows you to send an audio stream to a Conversation."""

    streamUrl: List[str]
    level: Optional[float] = Field(None, ge=-1, le=1)
    bargeIn: Optional[bool] = None
    loop: Optional[int] = Field(None, ge=0)
    action: NccoActionType = NccoActionType.STREAM


class Input(NccoAction):
    """Collect digits or speech input by the person you are are calling."""

    type: List[Union[Literal['dtmf'], Literal['speech']]]
    dtmf: Optional[Dtmf] = None
    speech: Optional[Speech] = None
    eventUrl: Optional[List[str]] = None
    eventMethod: Optional[str] = None
    action: NccoActionType = NccoActionType.INPUT


class Notify(NccoAction):
    """Use the notify action to send a custom payload to your event URL."""

    payload: dict
    eventUrl: List[str]
    eventMethod: Optional[str] = None
    action: NccoActionType = NccoActionType.NOTIFY

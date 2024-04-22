from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field, model_validator
from vonage_utils.types import Dtmf

from ..errors import VoiceError
from .common import AdvancedMachineDetection, Phone, Sip, Vbc, Websocket
from .enums import CallState, TtsLanguageCode
from .ncco import Connect, Conversation, Input, Notify, Record, Stream, Talk


class ToPhone(Phone):
    dtmf_answer: Optional[Dtmf] = Field(None, serialization_alias='dtmfAnswer')


class CreateCallRequest(BaseModel):
    ncco: List[Union[Record, Conversation, Connect, Input, Talk, Stream, Notify]] = None
    answer_url: List[str] = None
    answer_method: Optional[Literal['POST', 'GET']] = None
    to: List[Union[ToPhone, Sip, Websocket, Vbc]]

    from_: Optional[Phone] = Field(None, serialization_alias='from')
    random_from_number: Optional[bool] = None
    event_url: Optional[List[str]] = None
    event_method: Optional[Literal['POST', 'GET']] = None
    machine_detection: Optional[Literal['continue', 'hangup']] = None
    advanced_machine_detection: Optional[AdvancedMachineDetection] = None
    length_timer: Optional[int] = Field(None, ge=1, le=7200)
    ringing_timer: Optional[int] = Field(None, ge=1, le=120)

    @model_validator(mode='after')
    def validate_ncco_and_answer_url(self):
        if self.ncco is None and self.answer_url is None:
            raise VoiceError('Either `ncco` or `answer_url` must be set')
        if self.ncco is not None and self.answer_url is not None:
            raise VoiceError('`ncco` and `answer_url` cannot be used together')
        return self

    @model_validator(mode='after')
    def validate_from_and_random_from_number(self):
        if self.random_from_number is None and self.from_ is None:
            raise VoiceError('Either `from_` or `random_from_number` must be set')
        if self.random_from_number == True and self.from_ is not None:
            raise VoiceError('`from_` and `random_from_number` cannot be used together')
        return self


class ListCallsFilter(BaseModel):
    status: Optional[CallState] = None
    date_start: Optional[str] = None
    date_end: Optional[str] = None
    page_size: Optional[int] = Field(100, ge=1, le=100)
    record_index: Optional[int] = None
    order: Optional[Literal['asc', 'desc']] = None
    conversation_uuid: Optional[str] = None


class AudioStreamOptions(BaseModel):
    stream_url: List[str]
    loop: Optional[int] = Field(None, ge=0)
    level: Optional[float] = Field(None, ge=-1, le=1)


class TtsStreamOptions(BaseModel):
    text: str
    language: Optional[TtsLanguageCode] = None
    style: Optional[int] = None
    premium: Optional[bool] = None
    loop: Optional[int] = Field(None, ge=0)
    level: Optional[float] = Field(None, ge=-1, le=1)

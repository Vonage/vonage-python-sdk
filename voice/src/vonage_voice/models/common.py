from typing import Literal, Optional

from pydantic import BaseModel, Field
from vonage_utils.types import PhoneNumber, SipUri
from vonage_voice.models.enums import Channel


class Phone(BaseModel):
    number: PhoneNumber
    type: Channel = Channel.PHONE


class Sip(BaseModel):
    uri: SipUri
    type: Channel = Channel.SIP


class Websocket(BaseModel):
    uri: str = Field(..., min_length=1, max_length=50)
    content_type: Literal['audio/l16;rate=8000', 'audio/l16;rate=16000'] = Field(
        'audio/l16;rate=16000', serialization_alias='content-type'
    )
    type: Channel = Channel.WEBSOCKET
    headers: Optional[dict] = None


class Vbc(BaseModel):
    extension: str
    type: Channel = Channel.VBC


class AdvancedMachineDetection(BaseModel):
    behavior: Optional[Literal['continue', 'hangup']] = None
    mode: Optional[Literal['default', 'detect', 'detect_beep']] = None
    beep_timeout: Optional[int] = Field(None, ge=45, le=120)

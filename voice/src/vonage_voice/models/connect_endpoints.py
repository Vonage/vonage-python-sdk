from typing import Literal, Optional

from pydantic import BaseModel, Field
from vonage_utils.types import Dtmf, PhoneNumber, SipUri

from .enums import ConnectEndpointType


class OnAnswer(BaseModel):
    url: str
    ringbackTone: Optional[str] = None


class PhoneEndpoint(BaseModel):
    number: PhoneNumber
    dtmfAnswer: Optional[Dtmf] = None
    onAnswer: Optional[OnAnswer] = None
    type: ConnectEndpointType = ConnectEndpointType.PHONE


class AppEndpoint(BaseModel):
    user: str
    type: ConnectEndpointType = ConnectEndpointType.APP


class WebsocketEndpoint(BaseModel):
    uri: str
    contentType: Literal['audio/l16;rate=16000', 'audio/l16;rate=8000'] = Field(
        None, serialization_alias='content-type'
    )
    headers: Optional[dict] = None
    type: ConnectEndpointType = ConnectEndpointType.WEBSOCKET


class SipEndpoint(BaseModel):
    uri: SipUri
    headers: Optional[dict] = None
    type: ConnectEndpointType = ConnectEndpointType.SIP


class VbcEndpoint(BaseModel):
    extension: str
    type: ConnectEndpointType = ConnectEndpointType.VBC

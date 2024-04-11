from pydantic import BaseModel, AnyUrl, Field
from typing import Optional
from typing_extensions import Literal

from .enums import ConnectEndpointType

from vonage_utils.types import Dtmf, PhoneNumber, SipUri


class BaseEndpoint(BaseModel):
    """Base Endpoint model for use with the NCCO Connect action."""


class OnAnswer(BaseModel):
    url: AnyUrl
    ringbackTone: Optional[AnyUrl] = None


class PhoneEndpoint(BaseEndpoint):
    number: PhoneNumber
    dtmfAnswer: Optional[Dtmf] = None
    onAnswer: Optional[OnAnswer] = None
    type: ConnectEndpointType = ConnectEndpointType.PHONE


class AppEndpoint(BaseEndpoint):
    user: str
    type: ConnectEndpointType = ConnectEndpointType.APP


class WebsocketEndpoint(BaseEndpoint):
    uri: AnyUrl
    contentType: Literal['audio/l16;rate=16000', 'audio/l16;rate=8000'] = Field(
        'audio/l16;rate=16000', serialization_alias='content-type'
    )
    headers: Optional[dict] = {}
    type: ConnectEndpointType = ConnectEndpointType.WEBSOCKET


class SipEndpoint(BaseEndpoint):
    uri: SipUri
    headers: Optional[dict] = {}
    type: ConnectEndpointType = ConnectEndpointType.SIP


class VbcEndpoint(BaseEndpoint):
    extension: str
    type: ConnectEndpointType = ConnectEndpointType.VBC

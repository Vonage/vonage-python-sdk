from typing import Literal, Optional

from pydantic import BaseModel, Field
from vonage_utils.types import Dtmf, PhoneNumber, SipUri

from .enums import ConnectEndpointType


class OnAnswer(BaseModel):
    """Settings for what to do when the call is answered.

    Args:
        url (str): The URL to fetch the NCCO from. The URL serves an NCCO to execute in the
            number being connected to, before that call is joined to your existing conversation.
        ringbackTone (Optional[str]): A URL value that points to a `ringbackTone` to be played
            back on repeat to the caller, so they do not hear silence.
    """

    url: str
    ringbackTone: Optional[str] = None


class PhoneEndpoint(BaseModel):
    """Model for a phone endpoint.

    Args:
        number (PhoneNumber): The phone number to call.
        dtmfAnswer (Optional[Dtmf]): The DTMF tones to send when the call is answered.
        onAnswer (Optional[OnAnswer]): Settings for what to do when the call is answered.
    """

    number: PhoneNumber
    dtmfAnswer: Optional[Dtmf] = None
    onAnswer: Optional[OnAnswer] = None
    type: ConnectEndpointType = ConnectEndpointType.PHONE


class AppEndpoint(BaseModel):
    """Model for an RTC capable application endpoint.

    Args:
        user (str): The username of the user to connect to. This username must have been
            added as a user.
    """

    user: str
    type: ConnectEndpointType = ConnectEndpointType.APP


class WebsocketEndpoint(BaseModel):
    """Model for a WebSocket connection.

    Args:
        uri (str): The URI of the WebSocket connection.
        contentType (Literal['audio/l16;rate=8000', 'audio/l16;rate=16000']): The internet
            media type for the audio you are streaming.
        headers (Optional[dict]): The headers to include with the WebSocket connection.
    """

    uri: str
    contentType: Literal['audio/l16;rate=16000', 'audio/l16;rate=8000'] = Field(
        None, serialization_alias='content-type'
    )
    headers: Optional[dict] = None
    type: ConnectEndpointType = ConnectEndpointType.WEBSOCKET


class SipEndpoint(BaseModel):
    """Model for a SIP endpoint.

    Args:
        uri (SipUri): The SIP URI to connect to.
        headers (Optional[dict]): The headers to include with the SIP connection. To use
            TLS and/or SRTP, include respectively `transport=tls` or `media=srtp` to the URL with
            the semicolon `;` as a delimiter.
    """

    uri: SipUri
    headers: Optional[dict] = None
    type: ConnectEndpointType = ConnectEndpointType.SIP


class VbcEndpoint(BaseModel):
    """Model for a VBC endpoint.

    Args:
        extension (str): The VBC extension to connect the call to.
    """

    extension: str
    type: ConnectEndpointType = ConnectEndpointType.VBC

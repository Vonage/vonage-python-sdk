from typing import Literal, Optional

from pydantic import BaseModel, Field
from vonage_utils.types import PhoneNumber, SipUri
from vonage_voice.models.enums import Channel


class Phone(BaseModel):
    """Model for a phone number.

    Args:
        number (PhoneNumber): The phone number.
    """

    number: PhoneNumber
    type: Channel = Channel.PHONE


class Sip(BaseModel):
    """Model for a SIP URI.

    Args:
        uri (SipUri): The SIP URI.
    """

    uri: SipUri
    type: Channel = Channel.SIP


class Websocket(BaseModel):
    """Model for a WebSocket connection.

    Args:
        uri (str): The URI of the WebSocket connection.
        content_type (Literal['audio/l16;rate=8000', 'audio/l16;rate=16000']): The content
            type of the audio stream.
        headers (Optional[dict]): The headers to include with the WebSocket connection.
    """

    uri: str = Field(..., min_length=1)
    content_type: Literal['audio/l16;rate=8000', 'audio/l16;rate=16000'] = Field(
        'audio/l16;rate=16000', serialization_alias='content-type'
    )
    headers: Optional[dict] = None
    type: Channel = Channel.WEBSOCKET


class Vbc(BaseModel):
    """Model for a VBC connection.

    Args:
        extension (str): The extension to call.
    """

    extension: str
    type: Channel = Channel.VBC


class AdvancedMachineDetection(BaseModel):
    """Model for advanced machine detection settings. Configure the behavior of Vonage's
    advanced machine detection. Overrides `machine_detection` if both are set.

    Args:
        behavior (Optional[Literal['continue', 'hangup']]): The behavior when a machine
            is detected.
        mode (Optional[Literal['default', 'detect', 'detect_beep']]): Detect if machine
            answered and sends a human or machine status in the webhook payload.
        beep_timeout (Optional[int]): Maximum time in seconds Vonage should wait for a
            machine beep to be detected.
    """

    behavior: Optional[Literal['continue', 'hangup']] = None
    mode: Optional[Literal['default', 'detect', 'detect_beep']] = None
    beep_timeout: Optional[int] = Field(None, ge=45, le=120)

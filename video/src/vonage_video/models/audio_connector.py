from typing import Optional

from pydantic import BaseModel, Field
from vonage_video.models.enums import AudioSampleRate


class AudioConnectorWebsocket(BaseModel):
    """The audio connector websocket options.

    Args:
        uri (str): The URI.
        streams (list): The streams.
        headers (dict): The headers.
        audio_rate (AudioSampleRate): The audio sample rate.
    """

    uri: str
    streams: Optional[list] = None
    headers: Optional[dict] = None
    audio_rate: Optional[AudioSampleRate] = Field(None, serialization_alias='audioRate')


class AudioConnectorOptions(BaseModel):
    """Options for the audio connector.

    Args:
        session_id (str): The session ID.
        token (str): The token.
        websocket (AudioConnectorWebsocket): The audio connector websocket.
    """

    session_id: str = Field(..., serialization_alias='sessionId')
    token: str
    websocket: AudioConnectorWebsocket


class AudioConnectorData(BaseModel):
    """Class containing audio connector ID and audio captioning session ID."""

    id: Optional[str] = None
    captions_id: Optional[str] = Field(None, serialization_alias='captionsId')

from typing import Optional

from pydantic import BaseModel, Field
from vonage_video.models.enums import AudioSampleRate


class AudioConnectorWebSocket(BaseModel):
    """The audio connector websocket options.

    Args:
        uri (str): The URI.
        streams (list[str]): Stream IDs to include. If not provided, all streams are included.
        headers (dict): The headers to send to your WebSocket server.
        audio_rate (AudioSampleRate): The audio sample rate in Hertz.
    """

    uri: str
    streams: Optional[list[str]] = None
    headers: Optional[dict] = None
    audio_rate: Optional[AudioSampleRate] = Field(None, serialization_alias='audioRate')


class AudioConnectorOptions(BaseModel):
    """Options for the audio connector.

    Args:
        session_id (str): The session ID.
        token (str): The token.
        websocket (AudioConnectorWebSocket): The audio connector websocket.
    """

    session_id: str = Field(..., serialization_alias='sessionId')
    token: str
    websocket: AudioConnectorWebSocket


class AudioConnectorData(BaseModel):
    """Class containing Audio Connector WebSocket ID and connection ID.

    Args:
        id (str, Optional): The WebSocket ID.
        connection_id (str, Optional): The connection ID.
    """

    id: Optional[str] = None
    connection_id: Optional[str] = Field(None, validation_alias='connectionId')

from typing import Optional

from pydantic import BaseModel, Field
from vonage_video.models.enums import AudioSampleRate
from vonage_video.models.enums import AudioTransportEncoding, AudioTransportTransport

class AudioTransportConfiguration(BaseModel):
    """The audio transport configuration.

    Args:
        transport (AudioTransportTransport): 'binary' (raw PCM16, the default) or 'json'.
        encoding (AudioTransportEncoding): Required when transport is 'json'. Set to 'base64'.
        audio_field (str): The JSON key for the outbound audio data. Defaults to 'audio'.
        receive_audio_field (str): The JSON key for inbound audio data (when bidirectional is enabled). Defaults to the same value as audio_field.
        static_fields (dict): A dictionary of extra key-value pairs included in every outbound JSON audio message.
    """

    transport: Optional[AudioTransportTransport] = None
    encoding: Optional[AudioTransportEncoding] = None
    audio_field: Optional[str] = None
    receive_audio_field: Optional[str] = None
    static_fields: Optional[dict] = None


class AudioConnectorWebSocket(BaseModel):
    """The audio connector websocket options.

    Args:
        uri (str): The URI.
        streams (list[str]): Stream IDs to include. If not provided, all streams are included.
        headers (dict): The headers to send to your WebSocket server.
        audio_rate (AudioSampleRate): The audio sample rate in Hertz.
        bidirectional (bool): Whether the websocket is bidirectional.
        audio_transport (AudioTransportConfiguration): The audio transport configuration. Configures how audio is serialized on the WebSocket wire. By default, audio is sent as raw binary PCM 16-bit frames.
    """

    uri: str
    streams: Optional[list[str]] = None
    headers: Optional[dict] = None
    audio_rate: Optional[AudioSampleRate] = Field(None, serialization_alias='audioRate')
    bidirectional: Optional[bool] = Field(
        None, description="Whether the websocket is bidirectional."
    )
    audio_transport: Optional[AudioTransportConfiguration] = Field(
        None, serialization_alias='audioTransport'
    )

    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        if self.bidirectional is not True and 'bidirectional' in data:
            del data['bidirectional']

        if 'audioRate' in data and isinstance(data['audioRate'], AudioSampleRate):
            data['audioRate'] = data['audioRate'].value
        return data


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

    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        if isinstance(self.websocket, AudioConnectorWebSocket):
            data['websocket'] = self.websocket.model_dump(*args, **kwargs)
        return data


class AudioConnectorData(BaseModel):
    """Class containing Audio Connector WebSocket ID and connection ID.

    Args:
        id (str, Optional): The WebSocket ID.
        connection_id (str, Optional): The connection ID.
    """

    id: Optional[str] = None
    connection_id: Optional[str] = Field(None, validation_alias='connectionId')

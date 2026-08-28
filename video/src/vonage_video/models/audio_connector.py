import json
from typing import Optional

from pydantic import BaseModel, Field
from vonage_video.models.enums import AudioEncoding, AudioSampleRate, AudioTransport


class AudioTransportConfig(BaseModel):
    """Configuration for audio transport over the WebSocket connection.

    Args:
        transport (AudioTransport): The transport type ('binary' or 'json').
        encoding (AudioEncoding, Optional): The encoding type (required for 'json'
            transport, e.g. 'base64').
        audio_field (str, Optional): The JSON field name for outbound audio data.
            Defaults to 'audio' on the server side.
        receive_audio_field (str, Optional): The JSON field name for inbound audio
            data. Defaults to the value of audio_field.
        static_fields (dict, Optional): Optional static fields included in every
            outbound JSON message.
    """

    transport: AudioTransport
    encoding: Optional[AudioEncoding] = None
    audio_field: Optional[str] = Field(None, serialization_alias='audio_field')
    receive_audio_field: Optional[str] = Field(
        None, serialization_alias='receive_audio_field'
    )
    static_fields: Optional[dict] = Field(None, serialization_alias='static_fields')


class AudioConnectorWebSocket(BaseModel):
    """The audio connector websocket options.

    Args:
        uri (str): The URI.
        streams (list[str]): Stream IDs to include. If not provided, all streams are included.
        headers (dict): The headers to send to your WebSocket server.
        audio_rate (AudioSampleRate): The audio sample rate in Hertz.
        bidirectional (bool): Whether the websocket is bidirectional.
        audio_transport (AudioTransportConfig, Optional): Configuration for audio
            transport format. When set, audio is sent using the specified transport
            type and encoding.
    """

    uri: str
    streams: Optional[list[str]] = None
    headers: Optional[dict] = None
    audio_rate: Optional[AudioSampleRate] = Field(None, serialization_alias='audioRate')
    bidirectional: Optional[bool] = Field(
        None, description="Whether the websocket is bidirectional."
    )
    audio_transport: Optional[AudioTransportConfig] = None

    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        if self.bidirectional is not True and 'bidirectional' in data:
            del data['bidirectional']

        if 'audioRate' in data and isinstance(data['audioRate'], AudioSampleRate):
            data['audioRate'] = data['audioRate'].value

        if self.audio_transport is not None:
            data['audioTransport'] = json.dumps(
                self.audio_transport.model_dump(exclude_none=True, by_alias=True),
                separators=(',', ':'),
            )
            data.pop('audio_transport', None)
        else:
            data.pop('audio_transport', None)
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

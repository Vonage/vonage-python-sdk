from typing import Optional

from pydantic import BaseModel, Field, model_validator
from vonage_video.errors import InvalidHlsOptionsError, InvalidOutputOptionsError
from vonage_video.models.common import ComposedLayout, ListVideoFilter, VideoStream
from vonage_video.models.enums import StreamMode, VideoResolution


class ListBroadcastsFilter(ListVideoFilter):
    """Model with filters for listing broadcasts.

    Args:
        offset (int, Optional): The offset.
        page_size (int, Optional): The number of broadcast objects to return per page.
        session_id (str, Optional): The session ID of a Vonage Video session.
    """

    session_id: Optional[str] = None


class BroadcastHls(BaseModel):
    """Model for HLS output settings for a broadcast.

    Args:
        dvr (bool, Optional): Whether the broadcast supports DVR.
        low_latency (bool, Optional): Whether the broadcast is low latency.
            Note: Cannot be True when `dvr=True`.

    Raises:
        InvalidHlsOptionsError: If `low_latency=True` and `dvr=True`.
    """

    dvr: Optional[bool] = None
    low_latency: Optional[bool] = Field(None, serialization_alias='lowLatency')

    @model_validator(mode='after')
    def validate_low_latency(self):
        if self.dvr and self.low_latency:
            raise InvalidHlsOptionsError('Cannot set `low_latency=True` when `dvr=True`.')
        return self


class BroadcastRtmp(BaseModel):
    """Model for RTMP output settings for a broadcast.

    Args:
        id (str, Optional): A unique ID for the stream.
        server_url (str): The RTMP server URL.
        stream_name (str): The stream name, such as the YouTube Live stream name or the
            Facebook stream key.
    """

    id: Optional[str] = None
    server_url: str = Field(..., serialization_alias='serverUrl')
    stream_name: str = Field(..., serialization_alias='streamName')


class RtmpStream(BroadcastRtmp):
    """Model for RTMP output settings for a broadcast.

    Args:
        id (str, Optional): A unique ID for the stream.
        server_url (str): The RTMP server URL.
        stream_name (str): The stream name, such as the YouTube Live stream name or the
            Facebook stream key.
        status (str, Optional): The status of the RTMP stream.
    """

    server_url: Optional[str] = Field(None, validation_alias='serverUrl')
    stream_name: Optional[str] = Field(None, validation_alias='streamName')
    status: Optional[str] = None


class BroadcastUrls(BaseModel):
    """Model for URLs for a broadcast.

    Args:
        hls (str, Optional): URL for the HLS broadcast.
        hls_status (str, Optional): The status of the HLS broadcast.
        rtmp (list[str], Optional): An array of objects that include information on each of the RTMP streams.
    """

    hls: Optional[str] = None
    hls_status: Optional[str] = Field(None, validation_alias='hlsStatus')
    rtmp: Optional[list[RtmpStream]] = None


class HlsSettings(BaseModel):
    """Model for HLS settings for a broadcast.

    Args:
        dvr (bool, Optional): Whether the broadcast supports DVR.
        low_latency (bool, Optional): Whether the broadcast is low latency.
    """

    dvr: Optional[bool] = None
    low_latency: Optional[bool] = Field(None, validation_alias='lowLatency')


class BroadcastSettings(BaseModel):
    """Model for settings for a broadcast.

    Args:
        hls (HlsSettings, Optional): HLS settings for the broadcast.
    """

    hls: Optional[HlsSettings] = None


class Broadcast(BaseModel):
    """Model for a broadcast.

    Args:
        id (str, Optional): The broadcast ID.
        session_id (str, Optional): The video session ID.
        multi_broadcast_tag (str, Optional): The unique tag for simultaneous broadcasts
            (if one was set).
        application_id (str, Optional): The Vonage application ID.
        created_at (int, Optional): The timestamp when the broadcast started, expressed
            in milliseconds since the Unix epoch.
        updated_at (int, Optional): The timestamp when the broadcast was last updated,
            expressed in milliseconds since the Unix epoch.
        max_duration (int, Optional): The maximum duration of the broadcast in seconds.
        max_bitrate (int, Optional): The maximum bitrate of the broadcast.
        broadcast_urls (BroadcastUrls, Optional): An object containing details about the
            HLS and RTMP broadcasts.
        settings (BroadcastHls, Optional): The HLS output settings.
        resolution (VideoResolution, Optional): The resolution of the broadcast.
        has_audio (bool, Optional): Whether the broadcast includes audio.
        has_video (bool, Optional): Whether the broadcast includes video.
        stream_mode (StreamMode, Optional): Whether streams included in the broadcast are
            selected automatically (`auto`, the default) or manually (`manual`).
        status (str, Optional): The status of the broadcast.
        streams (list[VideoStream], Optional): An array of objects corresponding to
            streams currently being broadcast. This is only set for a broadcast with
            the status set to "started" and the `stream_mode` set to "manual".
    """

    id: Optional[str] = None
    session_id: Optional[str] = Field(None, validation_alias='sessionId')
    multi_broadcast_tag: Optional[str] = Field(None, validation_alias='multiBroadcastTag')
    application_id: Optional[str] = Field(None, validation_alias='applicationId')
    created_at: Optional[int] = Field(None, validation_alias='createdAt')
    updated_at: Optional[int] = Field(None, validation_alias='updatedAt')
    max_duration: Optional[int] = Field(None, validation_alias='maxDuration')
    max_bitrate: Optional[int] = Field(None, validation_alias='maxBitrate')
    broadcast_urls: Optional[BroadcastUrls] = Field(
        None, validation_alias='broadcastUrls'
    )
    settings: Optional[BroadcastSettings] = None
    resolution: Optional[VideoResolution] = None
    has_audio: Optional[bool] = Field(None, validation_alias='hasAudio')
    has_video: Optional[bool] = Field(None, validation_alias='hasVideo')
    stream_mode: Optional[StreamMode] = Field(None, validation_alias='streamMode')
    status: Optional[str] = None
    streams: Optional[list[VideoStream]] = None


class BroadcastOutputSettings(BaseModel):
    """Model for output options for a broadcast. You must specify at least one output
    option.

    Args:
        hls (BroadcastHls, Optional): HLS output settings.
        rtmp (list[BroadcastRtmp], Optional): RTMP output settings.

    Raises:
        InvalidOutputOptionsError: If neither HLS nor RTMP output options are set.
    """

    hls: Optional[BroadcastHls] = None
    rtmp: Optional[list[BroadcastRtmp]] = None

    @model_validator(mode='after')
    def validate_outputs(self):
        if self.hls is None and self.rtmp is None:
            raise InvalidOutputOptionsError(
                'You must specify at least one output option.'
            )
        return self


class CreateBroadcastRequest(BaseModel):
    """Model for creating a broadcast.

    Args:
        session_id (str): The session ID of a Vonage Video session.
        layout (Layout, Optional): Layout options for the broadcast.
        max_duration (int, Optional): The maximum duration of the broadcast in seconds.
        outputs (Outputs): Output options for the broadcast. This object defines the types of
            broadcast streams you want to start (both HLS and RTMP). You can include HLS, RTMP,
            or both as broadcast streams. If you include RTMP streaming, you can specify up
            to five target RTMP streams (or just one). Vonage streams the session to each RTMP
            URL you specify. Note that Vonage Video live streaming supports RTMP and RTMPS.
        resolution (VideoResolution, Optional): The resolution of the broadcast.
        stream_mode (StreamMode, Optional): Whether streams included in the broadcast are selected
            automatically ("auto", the default) or manually ("manual").
        multi_broadcast_tag (str, Optional): Set this to support recording multiple broadcasts
            for the same session simultaneously. Set this to a unique string for each simultaneous
            broadcast of an ongoing session. If you do not specify a unique multiBroadcastTag,
            you can only record one broadcast at a time for a given session.
        max_bitrate (int, Optional): The maximum bitrate of the broadcast, in bits per second.
    """

    session_id: str = Field(..., serialization_alias='sessionId')
    layout: Optional[ComposedLayout] = None
    max_duration: Optional[int] = Field(
        None, ge=60, le=36000, serialization_alias='maxDuration'
    )
    outputs: BroadcastOutputSettings
    resolution: Optional[VideoResolution] = None
    stream_mode: Optional[StreamMode] = Field(None, serialization_alias='streamMode')
    multi_broadcast_tag: Optional[str] = Field(
        None, serialization_alias='multiBroadcastTag'
    )
    max_bitrate: Optional[int] = Field(
        None, ge=100_000, le=6_000_000, serialization_alias='maxBitrate'
    )

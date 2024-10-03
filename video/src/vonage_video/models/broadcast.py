from typing import List, Optional

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
        stream_name (str): The such as the YouTube Live stream name or the Facebook stream key.
    """

    id: Optional[str] = None
    server_url: str = Field(..., serialization_alias='serverUrl')
    stream_name: str = Field(..., serialization_alias='streamName')


class RtmpStream(BroadcastRtmp):
    """Model for RTMP output settings for a broadcast.

    Args:
        id (str, Optional): A unique ID for the stream.
        server_url (str): The RTMP server URL.
        stream_name (str): The such as the YouTube Live stream name or the Facebook stream key.
        status (str, Optional): The status of the RTMP stream.
    """

    status: Optional[str] = None


class BroadcastUrls(BaseModel):
    """Model for URLs for a broadcast.

    Args:
        hls (str, Optional): URL for the HLS broadcast.
        rtmp (List[str], Optional): An array of objects that include information on each of the RTMP streams.
    """

    hls: Optional[str] = None
    rtmp: Optional[List[RtmpStream]] = None


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
        streams (List[VideoStream], Optional): An array of objects corresponding to
            streams currently being broadcast. This is only set for a broadcast with
            the status set to "started" and the `stream_mode` set to "manual".
    """

    id: Optional[str] = None
    session_id: Optional[str] = Field(None, alias='sessionId')
    multi_broadcast_tag: Optional[str] = Field(None, alias='multiBroadcastTag')
    application_id: Optional[str] = Field(None, alias='applicationId')
    created_at: Optional[int] = Field(None, alias='createdAt')
    updated_at: Optional[int] = Field(None, alias='updatedAt')
    max_duration: Optional[int] = Field(None, alias='maxDuration')
    max_bitrate: Optional[int] = Field(None, alias='maxBitrate')
    broadcast_urls: Optional[BroadcastUrls] = Field(None, alias='broadcastUrls')
    settings: Optional[BroadcastHls] = None
    resolution: Optional[VideoResolution] = None
    has_audio: Optional[bool] = Field(None, alias='hasAudio')
    has_video: Optional[bool] = Field(None, alias='hasVideo')
    stream_mode: Optional[StreamMode] = Field(None, alias='streamMode')
    status: Optional[str] = None
    streams: Optional[List[VideoStream]] = None


class Outputs(BaseModel):
    """Model for output options for a broadcast. You must specify at least one output option.

    Args:
        hls (BroadcastHls, Optional): HLS output settings.
        rtmp (List[BroadcastRtmp], Optional): RTMP output settings.
    """

    hls: Optional[BroadcastHls] = None
    rtmp: Optional[List[BroadcastRtmp]] = None

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
        has_audio (bool, Optional): Whether the archive or broadcast should include audio.
        has_video (bool, Optional): Whether the archive or broadcast should include video.
        layout (Layout, Optional): Layout options for the archive or broadcast.
        name (str, Optional): The name of the archive or broadcast.
        output_mode (OutputMode, Optional): Whether all streams in the archive or broadcast are recorded to a
            single file ("composed", the default) or to individual files ("individual").
        resolution (VideoResolution, Optional): The resolution of the archive or broadcast.
        stream_mode (StreamMode, Optional): Whether streams included in the archive or broadcast are selected
            automatically ("auto", the default) or manually ("manual").
        multi_broadcast_tag (str, Optional): Set this to support recording multiple broadcasts for the same session simultaneously.
            Set this to a unique string for each simultaneous broadcast of an ongoing session.
            You must also set this option when manually starting a broadcast in a session that is automatically broadcasted.
            If you do not specify a unique multiBroadcastTag, you can only record one broadcast at a time for a given session.
    """

    session_id: str = Field(..., serialization_alias='sessionId')
    layout: Optional[ComposedLayout] = None
    max_duration: Optional[int] = Field(None, serialization_alias='maxDuration')
    outputs: Outputs
    resolution: Optional[VideoResolution] = None
    stream_mode: Optional[StreamMode] = Field(None, serialization_alias='streamMode')
    multi_broadcast_tag: Optional[str] = Field(
        None, serialization_alias='multiBroadcastTag'
    )
    max_bitrate: Optional[int] = Field(None, serialization_alias='maxBitrate')

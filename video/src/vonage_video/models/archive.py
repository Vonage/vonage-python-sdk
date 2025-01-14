from typing import Optional

from pydantic import BaseModel, Field, model_validator
from vonage_video.errors import IndividualArchivePropertyError, NoAudioOrVideoError
from vonage_video.models.common import ComposedLayout, ListVideoFilter, VideoStream
from vonage_video.models.enums import (
    ArchiveStatus,
    OutputMode,
    StreamMode,
    VideoResolution,
)


class ListArchivesFilter(ListVideoFilter):
    """Model with filters for listing archives.

    Args:
        offset (int, Optional): The offset.
        page_size (int, Optional): The number of archives to return per page.
        session_id (str, Optional): The session ID of a Vonage Video session.
    """

    session_id: Optional[str] = None


class Transcription(BaseModel):
    """Model for transcription options for an archive.

    Args:
        status (str, Optional): The status of the transcription.
        reason (str, Optional): May give a brief reason for the transcription status.
    """

    status: Optional[str] = None
    reason: Optional[str] = None


class Archive(BaseModel):
    """Model for an archive.

    Args:
        id (str, Optional): The unique archive ID.
        status (ArchiveStatus, Optional): The status of the archive.
        name (str, Optional): The name of the archive.
        reason (str, Optional): May give a brief reason for the archive status.
        session_id (str, Optional): The session ID of the Vonage Video session.
        application_id (str, Optional): The Vonage application ID.
        created_at (int, Optional): The timestamp when the archive when the archive
            started recording, expressed in milliseconds since the Unix epoch.
        size (int, Optional): The size of the archive.
        duration (int, Optional): The duration of the archive in seconds.
            For archives that have are being recorded, this value is set to 0.
        output_mode (OutputMode, Optional): The output mode of the archive.
        stream_mode (StreamMode, Optional): Whether streams included in the archive
            are selected automatically (`auto`, the default) or manually (`manual`).
        has_audio (bool, Optional): Whether the archive will record audio.
        has_video (bool, Optional): Whether the archive will record video.
        has_transcription (bool, Optional): Whether audio will be transcribed.
        sha256_sum (str, Optional): The SHA-256 hash of the archive.
        password (str, Optional): The password for the archive.
        updated_at (int, Optional): The timestamp when the archive was last updated,
            expressed in milliseconds since the Unix epoch.
        multi_archive_tag (str, Optional): Set this to support recording multiple
            archives for the same session simultaneously. Set this to a unique string
            for each simultaneous archive of an ongoing session.
        event (str, Optional): The event that triggered the response.
        resolution (VideoResolution, Optional): The resolution of the archive.
        streams (list[VideoStream], Optional): The streams in the archive.
        url (str, Optional): The download URL of the available archive file.
            This is only set for an archive with the status set to `available`.
        transcription (Transcription, Optional): Transcription options for the archive.
        max_bitrate (int, Optional): The maximum video bitrate of the archive, in bits per
            second. This is only valid for composed archives.
    """

    id: Optional[str] = None
    status: Optional[ArchiveStatus] = None
    name: Optional[str] = None
    reason: Optional[str] = None
    session_id: Optional[str] = Field(None, validation_alias='sessionId')
    application_id: Optional[str] = Field(None, validation_alias='applicationId')
    created_at: Optional[int] = Field(None, validation_alias='createdAt')
    size: Optional[int] = None
    duration: Optional[int] = None
    output_mode: Optional[OutputMode] = Field(None, validation_alias='outputMode')
    stream_mode: Optional[StreamMode] = Field(None, validation_alias='streamMode')
    has_audio: Optional[bool] = Field(None, validation_alias='hasAudio')
    has_video: Optional[bool] = Field(None, validation_alias='hasVideo')
    has_transcription: Optional[bool] = Field(None, validation_alias='hasTranscription')
    sha256_sum: Optional[str] = Field(None, validation_alias='sha256sum')
    password: Optional[str] = None
    updated_at: Optional[int] = Field(None, validation_alias='updatedAt')
    multi_archive_tag: Optional[str] = Field(None, validation_alias='multiArchiveTag')
    event: Optional[str] = None
    resolution: Optional[VideoResolution] = None
    streams: Optional[list[VideoStream]] = None
    url: Optional[str] = None
    transcription: Optional[Transcription] = None
    max_bitrate: Optional[int] = Field(None, validation_alias='maxBitrate')


class CreateArchiveRequest(BaseModel):
    """Model for creating an archive.

    Args:
        session_id (str): The session ID of a Vonage Video session.
        has_audio (bool, Optional): Whether the archive should include audio.
        has_video (bool, Optional): Whether the archive should include video.
        layout (Layout, Optional): Layout options for the archive.
        multi_archive_tag (str, Optional): Set this to support recording multiple archives for the same session simultaneously.
            Set this to a unique string for each simultaneous archive of an ongoing session.
            You must also set this option when manually starting an archive in a session that is automatically archived.
            If you do not specify a unique multiArchiveTag, you can only record one archive at a time for a given session.
        name (str, Optional): The name of the archive.
        output_mode (OutputMode, Optional): Whether all streams in the archive are recorded to a
        single file ("composed", the default) or to individual files ("individual").
        resolution (VideoResolution, Optional): The resolution of the archive.
        stream_mode (StreamMode, Optional): Whether streams included in the archive are selected
            automatically ("auto", the default) or manually ("manual").
        max_bitrate (int, Optional): The maximum video bitrate of the archive, in bits per
            second. This is only valid for composed archives.
    Raises:
        NoAudioOrVideoError: If neither `has_audio` nor `has_video` is set.
        IndividualArchivePropertyError: If `resolution` or `layout` is set for individual archives
            or if `has_transcription` is set for composed archives.
    """

    session_id: str = Field(..., serialization_alias='sessionId')
    has_audio: Optional[bool] = Field(None, serialization_alias='hasAudio')
    has_video: Optional[bool] = Field(None, serialization_alias='hasVideo')
    has_transcription: Optional[bool] = Field(
        None, serialization_alias='hasTranscription'
    )
    layout: Optional[ComposedLayout] = None
    multi_archive_tag: Optional[str] = Field(None, serialization_alias='multiArchiveTag')
    name: Optional[str] = None
    output_mode: Optional[OutputMode] = Field(None, serialization_alias='outputMode')
    resolution: Optional[VideoResolution] = None
    stream_mode: Optional[StreamMode] = Field(None, serialization_alias='streamMode')
    max_bitrate: Optional[int] = Field(
        None, ge=100_000, le=6_000_000, serialization_alias='maxBitrate'
    )

    @model_validator(mode='after')
    def validate_audio_or_video(self):
        if self.has_audio is False and self.has_video is False:
            raise NoAudioOrVideoError(
                'One of `has_audio` or `has_video` must be included.'
            )
        return self

    @model_validator(mode='after')
    def no_layout_or_resolution_for_individual_archives(self):
        if self.output_mode == OutputMode.INDIVIDUAL and self.resolution is not None:
            raise IndividualArchivePropertyError(
                'The `resolution` property cannot be set for `archive_mode: \'individual\'`.'
            )
        if self.output_mode == OutputMode.INDIVIDUAL and self.layout is not None:
            raise IndividualArchivePropertyError(
                'The `layout` property cannot be set for `archive_mode: \'individual\'`.'
            )
        return self

    @model_validator(mode='after')
    def transcription_only_for_individual_archives(self):
        if self.output_mode == OutputMode.COMPOSED and self.has_transcription is True:
            raise IndividualArchivePropertyError(
                'The `has_transcription` property can only be set for `archive_mode: \'individual\'`.'
            )
        return self

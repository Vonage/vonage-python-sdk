from typing import List, Optional

from pydantic import BaseModel, Field, model_validator
from vonage_video.errors import (
    IndividualArchivePropertyError,
    LayoutScreenshareTypeError,
    LayoutStylesheetError,
    NoAudioOrVideoError,
)
from vonage_video.models.enums import (
    ArchiveStatus,
    LayoutType,
    OutputMode,
    StreamMode,
    VideoResolution,
)


class ListArchivesFilter(BaseModel):
    """Model with filters for listing archives.

    Args:
        offset (int, Optional): The offset.
        page_size (int, Optional): The number of archives to return per page.
        session_id (str, Optional): The session ID of a Vonage Video session.
    """

    offset: Optional[int] = None
    page_size: Optional[int] = Field(1000, serialization_alias='count')
    session_id: Optional[str] = None


class ArchiveStream(BaseModel):
    """Model for a stream in an archive.

    Args:
        stream_id (str, Optional): The stream ID.
        has_audio (bool, Optional): Whether the stream has audio.
        has_video (bool, Optional): Whether the stream has video.
    """

    stream_id: Optional[str] = Field(None, validation_alias='streamId')
    has_audio: Optional[bool] = Field(None, validation_alias='hasAudio')
    has_video: Optional[bool] = Field(None, validation_alias='hasVideo')


class Archive(BaseModel):
    """Model for an archive.

    Args:
        created_at (int, Optional): The timestamp when the archive when the archive
            started recording, expressed in milliseconds since the Unix epoch.
        duration (int, Optional): The duration of the archive in seconds.
            For archives that have are being recorded, this value is set to 0.
        has_audio (bool, Optional): Whether the archive will record audio.
        has_video (bool, Optional): Whether the archive will record video.
        id (str, Optional): The unique archive ID.
        multi_archive_tag (str, Optional): Set this to support recording multiple
            archives for the same session simultaneously. Set this to a unique string
            for each simultaneous archive of an ongoing session.
        name (str, Optional): The name of the archive.
        application_id (str, Optional): The Vonage application ID.
        reason (str, Optional): This is set when the `status` is `stopped` or `failed`.
        resolution (VideoResolution, Optional): The resolution of the archive.
        session_id (str, Optional): The session ID of the Vonage Video session.
        size (int, Optional): The size of the archive.
        status (ArchiveStatus, Optional): The status of the archive.
        stream_mode (StreamMode, Optional): Whether streams included in the archive
            are selected automatically (`auto`, the default) or manually (`manual`).
        streams (List[ArchiveStream], Optional): The streams in the archive.
        url (str, Optional): The download URL of the available archive file.
            This is only set for an archive with the status set to `available`.
    """

    created_at: Optional[int] = Field(None, validation_alias='createdAt')
    duration: Optional[int] = None
    has_audio: Optional[bool] = Field(None, validation_alias='hasAudio')
    has_video: Optional[bool] = Field(None, validation_alias='hasVideo')
    id: Optional[str] = None
    multi_archive_tag: Optional[str] = Field(None, validation_alias='multiArchiveTag')
    name: Optional[str] = None
    application_id: Optional[str] = Field(None, validation_alias='applicationId')
    reason: Optional[str] = None
    resolution: Optional[VideoResolution] = None
    session_id: Optional[str] = Field(None, validation_alias='sessionId')
    size: Optional[int] = None
    status: Optional[ArchiveStatus] = None
    stream_mode: Optional[StreamMode] = Field(None, validation_alias='streamMode')
    streams: Optional[List[ArchiveStream]] = None
    url: Optional[str] = None


class Layout(BaseModel):
    """Model for layout options for an archive.

    Args:
        type (str): Specify this to assign the initial layout type for the archive.
            This applies only to composed archives.
        stylesheet (str, Optional): The stylesheet URL. Used for the custom layout to
            define the visual layout.
        screenshare_type (str, Optional): The screenshare type. Set the screenshareType
            property to the layout type to use when there is a screen-sharing stream in
            the session. If you set the screenshareType property, you must set the type
            property to "bestFit" and leave the stylesheet property unset.
    """

    type: LayoutType
    stylesheet: Optional[str] = None
    screenshare_type: Optional[LayoutType] = Field(
        None, serialization_alias='screenshareType'
    )

    @model_validator(mode='after')
    def validate_stylesheet(self):
        if self.type == LayoutType.CUSTOM and self.stylesheet is None:
            raise LayoutStylesheetError(
                'The `stylesheet` property must be set for `layout_type: \'custom\'`.'
            )
        if self.type != LayoutType.CUSTOM and self.stylesheet is not None:
            raise LayoutStylesheetError(
                'The `stylesheet` property cannot be set for `layout_type: \'bestFit\'`.'
            )
        return self

    @model_validator(mode='after')
    def type_and_screenshare_type(self):
        if self.screenshare_type is not None and self.type != LayoutType.BEST_FIT:
            raise LayoutScreenshareTypeError(
                'If `screenshare_type` is set, `type` must have the value `bestFit`.'
            )
        return self


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
    """

    session_id: str = Field(..., serialization_alias='sessionId')
    has_audio: Optional[bool] = Field(None, serialization_alias='hasAudio')
    has_video: Optional[bool] = Field(None, serialization_alias='hasVideo')
    layout: Optional[Layout] = None
    multi_archive_tag: Optional[str] = Field(None, serialization_alias='multiArchiveTag')
    name: Optional[str] = None
    output_mode: Optional[OutputMode] = Field(None, serialization_alias='outputMode')
    resolution: Optional[VideoResolution] = None
    stream_mode: Optional[StreamMode] = Field(None, serialization_alias='streamMode')

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

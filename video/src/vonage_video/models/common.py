from typing import Optional

from pydantic import BaseModel, Field, model_validator
from vonage_video.errors import LayoutScreenshareTypeError, LayoutStylesheetError
from vonage_video.models.enums import LayoutType


class VideoStream(BaseModel):
    """Model for a video stream used for archive and broadcast operations.

    Args:
        stream_id (str, Optional): The stream ID.
        has_audio (bool, Optional): Whether the stream has audio.
        has_video (bool, Optional): Whether the stream has video.
    """

    stream_id: Optional[str] = Field(None, validation_alias='streamId')
    has_audio: Optional[bool] = Field(None, validation_alias='hasAudio')
    has_video: Optional[bool] = Field(None, validation_alias='hasVideo')


class AddStreamRequest(BaseModel):
    """Model for adding a stream to an archive or broadcast.

    Args:
        stream_id (VideoStream): The stream ID to add to the archive/broadcast.
        has_audio (bool, Optional): Whether the stream has audio.
        has_video (bool, Optional): Whether the stream has video.
    """

    stream_id: str = Field(..., serialization_alias='addStream')
    has_audio: Optional[bool] = Field(None, serialization_alias='hasAudio')
    has_video: Optional[bool] = Field(None, serialization_alias='hasVideo')


class ComposedLayout(BaseModel):
    """Model for layout options for a composed archive/broadcast.

    Args:
        type (str): Specify this to assign the initial layout type for the archive/broadcast.
            This applies only to composed archives.
        stylesheet (str, Optional): The stylesheet URL. Used for the custom layout to
            define the visual layout.
        screenshare_type (str, Optional): The screenshare type. Set the screenshareType
            property to the layout type to use when there is a screen-sharing stream in
            the session. If you set the screenshareType property, you must set the type
            property to "bestFit" and leave the stylesheet property unset.

    Raises:
        LayoutStylesheetError: If `stylesheet` is not set for `layout_type: 'custom'` or
            if `stylesheet` is set for `layout_type: 'bestFit'`.
        LayoutScreenshareTypeError: If `screenshare_type` is set and `type` is not 'bestFit'.
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


class ListVideoFilter(BaseModel):
    """Base model to filter when listing archives/broadcasts/Experience Composers.

    Args:
        offset (int, Optional): The offset.
        page_size (int, Optional): The number of archives to return per page.
    """

    offset: Optional[int] = None
    page_size: Optional[int] = Field(100, serialization_alias='count')

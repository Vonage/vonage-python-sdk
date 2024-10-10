from typing import List, Optional

from pydantic import BaseModel, Field


class StreamInfo(BaseModel):
    """The stream information.

    Args:
        id (str): The stream ID.
        video_type (str): Set to "camera", "screen", or "custom". A "screen" video uses
            screen sharing on the publisher as the video source; a "custom" video is
            published by a web client using an HTML VideoTrack element as the video
            source.
        name (str): An array of the layout classes for the stream.
    """

    id: Optional[str] = Field(None, validation_alias='id')
    video_type: Optional[str] = Field(None, validation_alias='videoType')
    name: Optional[str] = Field(None, validation_alias='name')
    layout_class_list: Optional[List[str]] = Field(
        None, validation_alias='layoutClassList'
    )


class StreamLayout(BaseModel):
    """The stream layout.

    Args:
        id (str): The stream ID.
        layout_class_list (list): An array of the layout classes for the stream.
    """

    id: str
    layout_class_list: List[str] = Field(..., serialization_alias='layoutClassList')


class StreamLayoutOptions(BaseModel):
    """The options for the stream layout.

    Args:
        items (list): An array of the stream layout items. Each item is a StreamLayout
            object. See StreamLayout.
    """

    items: List[StreamLayout]

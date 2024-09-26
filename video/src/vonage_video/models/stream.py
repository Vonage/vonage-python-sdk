from typing import List, Optional

from pydantic import BaseModel, Field


class StreamInfo(BaseModel):
    """The stream information.

    Args:
        id (str): The stream ID.
        video_type (str): The video type.
        name (str): The name.
        layout_class_list (list(str)): The layout class list.
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
        layout_class_list (list): The layout class list.
    """

    id: str
    layout_class_list: List[str] = Field(..., serialization_alias='layoutClassList')


class StreamLayoutOptions(BaseModel):
    """The options for the stream layout."""

    items: List[StreamLayout]

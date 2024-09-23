from typing import List, Optional

from pydantic import BaseModel, Field


class StreamInfo(BaseModel):
    id: Optional[str] = Field(None, validation_alias='id')
    video_type: Optional[str] = Field(None, validation_alias='videoType')
    name: Optional[str] = Field(None, validation_alias='name')
    layout_class_list: Optional[List[str]] = Field(
        None, validation_alias='layoutClassList'
    )


class StreamLayout(BaseModel):
    id: str
    layout_class_list: List[str] = Field(..., validation_alias='layoutClassList')


class StreamLayoutOptions(BaseModel):
    items: List[StreamLayout]

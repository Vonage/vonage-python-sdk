from typing import Optional

from pydantic import BaseModel, Field, field_validator

from .enums import ArchiveMode, MediaMode


class SessionOptions(BaseModel):
    archive_mode: Optional[ArchiveMode] = Field(None, serialization_alias='archiveMode')
    location: Optional[str] = None
    media_mode: Optional[MediaMode] = Field(None, serialization_alias='p2p.preference')

    @field_validator('media_mode')
    @classmethod
    def change_to_p2p_preference(cls, v: MediaMode):
        if v == MediaMode.ROUTED:
            return 'disabled'
        if v == MediaMode.RELAYED:
            return 'always'

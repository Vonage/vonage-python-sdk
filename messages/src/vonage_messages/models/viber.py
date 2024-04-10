from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator

from .base_message import BaseMessage
from .enums import ChannelType, MessageType


class ViberAction(BaseModel):
    url: str
    text: str = Field(..., max_length=30)


class ViberOptions(BaseModel):
    category: Literal['transaction', 'promotion'] = None
    ttl: Optional[int] = Field(None, ge=30, le=259200)
    type: Optional[Literal['string', 'template']] = None


class BaseViber(BaseMessage):
    from_: str = Field(..., min_length=1, max_length=50, serialization_alias='from')
    viber_service: Optional[ViberOptions] = None
    channel: ChannelType = ChannelType.VIBER


class ViberTextOptions(ViberOptions):
    action: Optional[ViberAction] = None


class ViberText(BaseViber):
    text: str = Field(..., max_length=1000)
    viber_service: Optional[ViberTextOptions] = None
    message_type: MessageType = MessageType.TEXT


class ViberImageResource(BaseModel):
    url: str
    caption: Optional[str] = None


class ViberImageOptions(ViberOptions):
    action: Optional[ViberAction] = None


class ViberImage(BaseViber):
    image: ViberImageResource
    viber_service: Optional[ViberImageOptions] = None
    message_type: MessageType = MessageType.IMAGE


class ViberVideoResource(BaseModel):
    url: str
    thumb_url: str = Field(..., max_length=1000)
    caption: Optional[str] = Field(None, max_length=1000)


class ViberVideoOptions(ViberOptions):
    duration: str
    file_size: str

    @field_validator('duration')
    @classmethod
    def validate_duration(cls, value):
        value_int = int(value)
        if not 1 <= value_int <= 600:
            raise ValueError('"Duration" must be a number between 1 and 600.')
        return value

    @field_validator('file_size')
    @classmethod
    def validate_file_size(cls, value):
        value_int = int(value)
        if not 1 <= value_int <= 200:
            raise ValueError('"File size" must be a number between 1 and 200.')
        return value


class ViberVideo(BaseViber):
    video: ViberVideoResource
    viber_service: ViberVideoOptions
    message_type: MessageType = MessageType.VIDEO


class ViberFileResource(BaseModel):
    url: str
    name: Optional[str] = Field(None, max_length=25)


class ViberFileOptions(ViberOptions):
    pass


class ViberFile(BaseViber):
    file: ViberFileResource
    viber_service: Optional[ViberFileOptions] = None
    message_type: MessageType = MessageType.FILE

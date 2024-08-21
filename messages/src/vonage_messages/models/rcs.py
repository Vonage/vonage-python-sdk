from typing import Optional

from pydantic import BaseModel, Field
from vonage_utils.types import PhoneNumber

from .base_message import BaseMessage
from .enums import ChannelType, MessageType


class RcsResource(BaseModel):
    url: str


class BaseRcs(BaseMessage):
    to: PhoneNumber
    from_: str = Field(..., serialization_alias='from', pattern='^[a-zA-Z0-9]+$')
    ttl: Optional[int] = Field(None, ge=300, le=259200)
    channel: ChannelType = ChannelType.RCS


class RcsText(BaseRcs):
    text: str = Field(..., min_length=1, max_length=3072)
    message_type: MessageType = MessageType.TEXT


class RcsImage(BaseRcs):
    image: RcsResource
    message_type: MessageType = MessageType.IMAGE


class RcsVideo(BaseRcs):
    video: RcsResource
    message_type: MessageType = MessageType.VIDEO


class RcsFile(BaseRcs):
    file: RcsResource
    message_type: MessageType = MessageType.FILE


class RcsCustom(BaseRcs):
    custom: dict
    message_type: MessageType = MessageType.CUSTOM

from typing import Optional, Union

from pydantic import BaseModel, Field
from vonage_utils.types import PhoneNumber

from .base_message import BaseMessage
from .enums import ChannelType, MessageType


class MmsResource(BaseModel):
    url: str
    caption: Optional[str] = Field(None, min_length=1, max_length=2000)


class BaseMms(BaseMessage):
    to: PhoneNumber
    from_: Union[PhoneNumber, str] = Field(..., serialization_alias='from')
    ttl: Optional[int] = Field(None, ge=300, le=259200)
    channel: ChannelType = ChannelType.MMS


class MmsImage(BaseMms):
    image: MmsResource
    message_type: MessageType = MessageType.IMAGE


class MmsVcard(BaseMms):
    vcard: MmsResource
    message_type: MessageType = MessageType.VCARD


class MmsAudio(BaseMms):
    audio: MmsResource
    message_type: MessageType = MessageType.AUDIO


class MmsVideo(BaseMms):
    video: MmsResource
    message_type: MessageType = MessageType.VIDEO

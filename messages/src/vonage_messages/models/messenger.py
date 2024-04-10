from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator

from .base_message import BaseMessage
from .enums import ChannelType, MessageType


class MessengerResource(BaseModel):
    url: str


class MessengerOptions(BaseModel):
    category: Optional[Literal['response', 'update', 'message_tag']] = None
    tag: Optional[str] = None

    @model_validator(mode='after')
    def check_tag_if_category_message_tag(self):
        if self.category == 'message_tag' and not self.tag:
            raise ValueError('"tag" is required when "category" == "message_tag"')
        return self


class BaseMessenger(BaseMessage):
    to: str = Field(..., min_length=1, max_length=50)
    from_: str = Field(..., min_length=1, max_length=50, serialization_alias='from')
    messenger: Optional[MessengerOptions] = None
    channel: ChannelType = ChannelType.MESSENGER


class MessengerText(BaseMessenger):
    text: str = Field(..., max_length=640)
    message_type: MessageType = MessageType.TEXT


class MessengerImage(BaseMessenger):
    image: MessengerResource
    message_type: MessageType = MessageType.IMAGE


class MessengerAudio(BaseMessenger):
    audio: MessengerResource
    message_type: MessageType = MessageType.AUDIO


class MessengerVideo(BaseMessenger):
    video: MessengerResource
    message_type: MessageType = MessageType.VIDEO


class MessengerFile(BaseMessenger):
    file: MessengerResource
    message_type: MessageType = MessageType.FILE

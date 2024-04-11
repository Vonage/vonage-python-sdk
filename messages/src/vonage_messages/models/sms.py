from typing import Optional, Union

from pydantic import BaseModel, Field
from vonage_utils.types import PhoneNumber

from .base_message import BaseMessage
from .enums import ChannelType, EncodingType, MessageType


class SmsOptions(BaseModel):
    encoding_type: Optional[EncodingType] = None
    content_id: Optional[str] = None
    entity_id: Optional[str] = None


class Sms(BaseMessage):
    from_: Union[PhoneNumber, str] = Field(..., serialization_alias='from')
    text: str = Field(..., max_length=1000)
    ttl: Optional[int] = None
    sms: Optional[SmsOptions] = None
    channel: ChannelType = ChannelType.SMS
    message_type: MessageType = MessageType.TEXT

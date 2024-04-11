from typing import List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field
from vonage_utils.types import PhoneNumber

from .base_message import BaseMessage
from .enums import ChannelType, MessageType


class WhatsappContext(BaseModel):
    message_uuid: str


class BaseWhatsapp(BaseMessage):
    from_: Union[PhoneNumber, str] = Field(..., serialization_alias='from')
    context: Optional[WhatsappContext] = None
    channel: ChannelType = ChannelType.WHATSAPP


class WhatsappText(BaseWhatsapp):
    text: str = Field(..., max_length=4096)
    message_type: MessageType = MessageType.TEXT


class WhatsappImageResource(BaseModel):
    url: str
    caption: Optional[str] = Field(None, min_length=1, max_length=3000)


class WhatsappImage(BaseWhatsapp):
    image: WhatsappImageResource
    message_type: MessageType = MessageType.IMAGE


class WhatsappAudioResource(BaseModel):
    url: str = Field(..., min_length=10, max_length=2000)


class WhatsappAudio(BaseWhatsapp):
    audio: WhatsappAudioResource
    message_type: MessageType = MessageType.AUDIO


class WhatsappVideoResource(BaseModel):
    url: str
    caption: Optional[str] = None


class WhatsappVideo(BaseWhatsapp):
    video: WhatsappVideoResource
    message_type: MessageType = MessageType.VIDEO


class WhatsappFileResource(BaseModel):
    url: str
    caption: Optional[str] = None
    name: Optional[str] = None


class WhatsappFile(BaseWhatsapp):
    file: WhatsappFileResource
    message_type: MessageType = MessageType.FILE


class WhatsappTemplateResource(BaseModel):
    name: str
    parameters: Optional[List[str]] = None

    model_config = ConfigDict(extra='allow')


class WhatsappTemplateSettings(BaseModel):
    locale: Optional[str] = 'en_US'
    policy: Optional[Literal['deterministic']] = None


class WhatsappTemplate(BaseWhatsapp):
    template: WhatsappTemplateResource
    whatsapp: WhatsappTemplateSettings = WhatsappTemplateSettings()
    message_type: MessageType = MessageType.TEMPLATE


class WhatsappStickerUrl(BaseModel):
    url: str


class WhatsappStickerId(BaseModel):
    id: str


class WhatsappSticker(BaseWhatsapp):
    sticker: Union[WhatsappStickerUrl, WhatsappStickerId]
    message_type: MessageType = MessageType.STICKER


class WhatsappCustom(BaseWhatsapp):
    custom: Optional[dict] = None
    message_type: MessageType = MessageType.CUSTOM

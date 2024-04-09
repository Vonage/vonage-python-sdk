from typing import Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field
from vonage_utils.types.phone_number import PhoneNumber

from ..enums import ChannelType, MessageType
from .message import BaseMessage


class WhatsappContext(BaseModel):
    message_uuid: str


class BaseWhatsapp(BaseMessage):
    from_: Union[PhoneNumber, str] = Field(..., serialization_alias='from')
    context: WhatsappContext
    channel: ChannelType = ChannelType.WHATSAPP


class WhatsappText(BaseWhatsapp):
    text: str = Field(..., max_length=4096)
    type: MessageType = MessageType.TEXT


class WhatsappImageResource(BaseModel):
    url: str
    caption: Optional[str] = Field(None, min_length=1, max_length=3000)


class WhatsappImage(BaseWhatsapp):
    image: WhatsappImageResource
    type: MessageType = MessageType.IMAGE


class WhatsappAudioResource(BaseModel):
    url: str = Field(..., min_length=10, max_length=2000)


class WhatsappAudio(BaseWhatsapp):
    audio: WhatsappAudioResource
    type: MessageType = MessageType.AUDIO


class WhatsappVideoResource(BaseModel):
    url: str
    caption: Optional[str] = None


class WhatsappVideo(BaseWhatsapp):
    video: WhatsappVideoResource
    type: MessageType = MessageType.VIDEO


class WhatsappFileResource(BaseModel):
    url: str
    caption: Optional[str] = None
    name: Optional[str] = None


class WhatsappFile(BaseWhatsapp):
    file: WhatsappFileResource
    type: MessageType = MessageType.FILE


class WhatsappTemplateResource(BaseModel):
    name: str
    parameters: Optional[list] = None

    model_config = ConfigDict(extra='allow')


class WhatsappTemplateSettings(BaseModel):
    locale: str = 'en_US'
    policy: Optional[Literal['deterministic']] = None


class WhatsappTemplate(BaseWhatsapp):
    template: WhatsappTemplateResource
    whatsapp: WhatsappTemplateSettings
    type: MessageType = MessageType.TEMPLATE


class WhatsappStickerUrl(BaseModel):
    url: str


class WhatsappStickerId(BaseModel):
    id: str


class WhatsappSticker(BaseWhatsapp):
    sticker: Union[WhatsappStickerUrl, WhatsappStickerId]
    type: MessageType = MessageType.STICKER


class WhatsappCustom(BaseWhatsapp):
    custom: Optional[dict] = None
    type: MessageType = MessageType.CUSTOM

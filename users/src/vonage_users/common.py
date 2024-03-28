from typing import List, Optional

from pydantic import BaseModel, Field, model_validator
from typing_extensions import Annotated

PhoneNumber = Annotated[str, Field(pattern=r'^[1-9]\d{6,14}$')]


class Link(BaseModel):
    href: str


class ResourceLink(BaseModel):
    self: Link


class PstnChannel(BaseModel):
    number: int


class SipChannel(BaseModel):
    uri: str = Field(..., pattern=r'^(sip|sips):\+?([\w|:.\-@;,=%&]+)')
    username: str = None
    password: str = None


class VbcChannel(BaseModel):
    extension: str


class WebsocketChannel(BaseModel):
    uri: str = Field(pattern=r'^(ws|wss):\/\/[a-zA-Z0-9~#%@&-_?\/.,:;)(\]\[]*$')
    content_type: Optional[str] = Field(
        None, alias='content-type', pattern='^audio/l16;rate=(8000|16000)$'
    )
    headers: Optional[dict] = None


class SmsChannel(BaseModel):
    number: PhoneNumber


class MmsChannel(BaseModel):
    number: PhoneNumber


class WhatsappChannel(BaseModel):
    number: PhoneNumber


class ViberChannel(BaseModel):
    number: PhoneNumber


class MessengerChannel(BaseModel):
    id: str


class Channels(BaseModel):
    sms: Optional[List[SmsChannel]] = None
    mms: Optional[List[MmsChannel]] = None
    whatsapp: Optional[List[WhatsappChannel]] = None
    viber: Optional[List[ViberChannel]] = None
    messenger: Optional[List[MessengerChannel]] = None
    pstn: Optional[List[PstnChannel]] = None
    sip: Optional[List[SipChannel]] = None
    websocket: Optional[List[WebsocketChannel]] = None
    vbc: Optional[List[VbcChannel]] = None


class Properties(BaseModel):
    custom_data: Optional[dict] = None


class User(BaseModel):
    name: Optional[str] = None
    display_name: Optional[str] = None
    image_url: Optional[str] = None
    channels: Optional[Channels] = None
    properties: Optional[Properties] = None
    links: Optional[ResourceLink] = Field(None, validation_alias='_links', exclude=True)
    link: Optional[str] = None
    id: Optional[str] = None

    @model_validator(mode='after')
    @classmethod
    def get_link(cls, data):
        if data.links is not None:
            data.link = data.links.self.href
        return data

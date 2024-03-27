from typing import Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl
from typing_extensions import Annotated

PhoneNumber = Annotated[str, Field(pattern='^[1-9]\d{6,14}$')]


class PstnChannel(BaseModel):
    number: int


class SipChannel(BaseModel):
    uri: str = Field(..., pattern='^(sip|sips):\+?([\w|:.\-@;,=%&]+)')
    username: str = None
    password: str = None


class VbcChannel(BaseModel):
    extension: str


class WebsocketChannel(BaseModel):
    uri: str = Field(pattern='^(ws|wss)://[a-zA-Z0-9~#%@&-_?\/.,:;)(][]*$')
    content_type: str = Field(pattern="^audio/l16;rate=(8000|16000)$")
    headers: Optional[Dict[str, str]] = None


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
    pstn: Optional[List[PstnChannel]] = None
    sip: Optional[List[SipChannel]] = None
    vbc: Optional[List[VbcChannel]] = None
    websocket: Optional[List[WebsocketChannel]] = None
    sms: Optional[List[SmsChannel]] = None
    mms: Optional[List[MmsChannel]] = None
    whatsapp: Optional[List[WhatsappChannel]] = None
    viber: Optional[List[ViberChannel]] = None
    messenger: Optional[List[MessengerChannel]] = None


class Properties(BaseModel):
    custom_data: Optional[Dict[str, str]]


class User(BaseModel):
    name: Optional[str] = Field(None, example="my_user_name")
    display_name: Optional[str] = Field(None, example="My User Name")
    image_url: Optional[HttpUrl] = Field(None, example="https://example.com/image.png")
    properties: Optional[Properties]
    channels: Optional[Channels]

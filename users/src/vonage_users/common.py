from typing import Optional

from pydantic import BaseModel, Field, model_validator
from vonage_utils.models import ResourceLink
from vonage_utils.types import PhoneNumber


class PstnChannel(BaseModel):
    """Model for a PSTN channel.

    Args:
        number (int): The PSTN number.
    """

    number: int


class SipChannel(BaseModel):
    """Model for a SIP channel.

    Args:
        uri (str): The SIP URI.
        username (str, Optional): The username for the SIP channel.
        password (str, Optional): The password for the SIP channel.
    """

    uri: str = Field(..., pattern=r'^(sip|sips):\+?([\w|:.\-@;,=%&]+)')
    username: str = None
    password: str = None


class VbcChannel(BaseModel):
    """Model for a VBC channel.

    Args:
        extension (str): The VBC extension.
    """

    extension: str


class WebsocketChannel(BaseModel):
    """Model for a WebSocket channel.

    Args:
        uri (str): URI for the WebSocket.
        content_type (str, Optional): Content type for the WebSocket.
        headers (dict, Optional): Headers sent to the WebSocket.
    """

    uri: str = Field(pattern=r'^(ws|wss):\/\/[a-zA-Z0-9~#%@&-_?\/.,:;)(\]\[]*$')
    content_type: Optional[str] = Field(
        None, alias='content-type', pattern='^audio/l16;rate=(8000|16000)$'
    )
    headers: Optional[dict] = None


class SmsChannel(BaseModel):
    """Model for an SMS channel.

    Args:
        number (PhoneNumber): The phone number for the SMS channel.
    """

    number: PhoneNumber


class MmsChannel(BaseModel):
    """Model for an MMS channel.

    Args:
        number (PhoneNumber): The phone number for the MMS channel.
    """

    number: PhoneNumber


class WhatsappChannel(BaseModel):
    """Model for a WhatsApp channel.

    Args:
        number (PhoneNumber): The phone number for the WhatsApp channel.
    """

    number: PhoneNumber


class ViberChannel(BaseModel):
    """Model for a Viber channel.

    Args:
        number (PhoneNumber): The phone number for the Viber channel.
    """

    number: PhoneNumber


class MessengerChannel(BaseModel):
    """Model for a Messenger channel.

    Args:
        id (str): The ID for the Messenger channel.
    """

    id: str


class Channels(BaseModel):
    """Model for channels associated with a user account.

    Args:
        sms (list[SmsChannel], Optional): A list of SMS channels.
        mms (list[MmsChannel], Optional): A list of MMS channels.
        whatsapp (list[WhatsappChannel], Optional): A list of WhatsApp channels.
        viber (list[ViberChannel], Optional): A list of Viber channels.
        messenger (list[MessengerChannel], Optional): A list of Messenger channels.
        pstn (list[PstnChannel], Optional): A list of PSTN channels.
        sip (list[SipChannel], Optional): A list of SIP channels.
        websocket (list[WebsocketChannel], Optional): A list of WebSocket channels.
        vbc (list[VbcChannel], Optional): A list of VBC channels.
    """

    sms: Optional[list[SmsChannel]] = None
    mms: Optional[list[MmsChannel]] = None
    whatsapp: Optional[list[WhatsappChannel]] = None
    viber: Optional[list[ViberChannel]] = None
    messenger: Optional[list[MessengerChannel]] = None
    pstn: Optional[list[PstnChannel]] = None
    sip: Optional[list[SipChannel]] = None
    websocket: Optional[list[WebsocketChannel]] = None
    vbc: Optional[list[VbcChannel]] = None


class Properties(BaseModel):
    """Model for properties associated with a user account.

    Args:
        custom_data (dict, Optional): Custom data associated with the user.
    """

    custom_data: Optional[dict] = None


class User(BaseModel):
    """Model for a user.

    Args:
        name (str, Optional): The name of the user.
        display_name (str, Optional): A string to be displayed as user name. It does not
            need to be unique.
        image_url (str, Optional): An image URL that you associate with the user.
        channels (Channels, Optional): The channels associated with the user.
        properties (Properties, Optional): The properties associated with the user.
        links (ResourceLink, Optional): Links associated with the user.
        link (str, Optional): The `_self` link.
        id (str, Optional): The ID of the user.
    """

    name: Optional[str] = None
    display_name: Optional[str] = None
    image_url: Optional[str] = None
    channels: Optional[Channels] = None
    properties: Optional[Properties] = None
    links: Optional[ResourceLink] = Field(None, validation_alias='_links', exclude=True)
    link: Optional[str] = None
    id: Optional[str] = None

    @model_validator(mode='after')
    def get_link(self):
        if self.links is not None:
            self.link = self.links.self.href
        return self

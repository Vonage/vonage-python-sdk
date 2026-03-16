from typing import Optional, List, Union

from pydantic import BaseModel, Field
from vonage_utils.types import PhoneNumber

from .base_message import BaseMessage
from .enums import ChannelType, MessageType, SuggestionType, UrlWebviewViewMode, RcsCategory, RcsCardOrientation, RcsImageAlignment, RcsCardWidth, RcsMediaHeight


class RcsResource(BaseModel):
    """Model for a resource in an RCS message.

    Args:
        url (str): The URL of the resource.
    """

    url: str


class RcsSuggestionBase(BaseModel):
    """Model for a suggestion in an RCS message.

    Args:
        text (str): The text to display on the suggestion chip.
        postback_data (str): The data that will be sent via the Inbound Message webhook when the suggestion is selected.
    """

    text: str = Field(..., min_length=1, max_length=25)
    postback_data: str


class RcsSuggestionReply(RcsSuggestionBase):
    """Model for a reply suggestion in an RCS message.

    Args:
        text (str): The text to display on the suggestion chip.
        postback_data (str): The data that will be sent via the Inbound Message webhook when the suggestion is selected.
    """

    type_: SuggestionType = Field(SuggestionType.REPLY, serialization_alias='type')


class RcsSuggestionActionDial(RcsSuggestionBase):
    """Model for a dial action suggestion in an RCS message.

    Args:
        text (str): The text to display on the suggestion chip.
        postback_data (str): The data that will be sent via the Inbound Message webhook when the suggestion is selected.
        phone_number (str): The phone number to dial when the suggestion is selected. In E.164 format without the leading plus sign.
    """

    type_: SuggestionType = Field(SuggestionType.DIAL, serialization_alias='type')
    phone_number: PhoneNumber


class RcsSuggestionActionViewLocation(RcsSuggestionBase):
    """Model for a view location action suggestion in an RCS message.

    Args:
        text (str): The text to display on the suggestion chip.
        postback_data (str): The data that will be sent via the Inbound Message webhook when the suggestion is selected.
        latitude (float): The latitude of the location to view when the suggestion is selected.
        longitude (float): The longitude of the location to view when the suggestion is selected.
        pin_label (str): The label to display on the location pin.
        fallback_url (str, Optional): The URL to open if the device doesn't support the view location action.
    """

    type_: SuggestionType = Field(SuggestionType.VIEW_LOCATION, serialization_alias='type')
    latitude: str
    longitude: str
    pin_label: str
    fallback_url: Optional[str] = None


class RcsSuggestionActionShareLocation(RcsSuggestionBase):
    """Model for a share location action suggestion in an RCS message.

    Args:
        text (str): The text to display on the suggestion chip.
        postback_data (str): The data that will be sent via the Inbound Message webhook when the suggestion is selected.
    """

    type_: SuggestionType = Field(SuggestionType.SHARE_LOCATION, serialization_alias='type')


class RcsSuggestionActionOpenUrl(RcsSuggestionBase):
    """Model for an open URL action suggestion in an RCS message.

    Args:
        text (str): The text to display on the suggestion chip.
        postback_data (str): The data that will be sent via the Inbound Message webhook when the suggestion is selected.
        url (str): The URL to open when the suggestion is selected.
    """

    type_: SuggestionType = Field(SuggestionType.OPEN_URL, serialization_alias='type')
    url: str
    description: str = Field(..., min_length=1, max_length=500)


class RcsSuggestionActionOpenUrlWebview(RcsSuggestionActionOpenUrl):
    """Model for an open URL in webview action suggestion in an RCS message.

    Args:
        text (str): The text to display on the suggestion chip.
        postback_data (str): The data that will be sent via the Inbound Message webhook when the suggestion is selected.
        url (str): The URL to open in a webview when the suggestion is selected.
        view_mode (str, Optional): The view mode for the webview. If not specified, the default view mode will be used.
    """

    type_: SuggestionType = Field(SuggestionType.OPEN_URL_IN_WEBVIEW, serialization_alias='type')
    view_mode: Optional[UrlWebviewViewMode] = None

class RcsSuggestionActionCreateCalendarEvent(RcsSuggestionBase):
    """Model for a create calendar event action suggestion in an RCS message.

    Args:
        text (str): The text to display on the suggestion chip.
        postback_data (str): The data that will be sent via the Inbound Message webhook when the suggestion is selected.
        start_time (str): The start time of the calendar event in ISO 8601 format.
        end_time (str): The end time of the calendar event in ISO 8601 format
        title (str): The title of the calendar event.
        description (str): The description of the calendar event.
        fallback_url (str, Optional): The URL to open if the device doesn't support the create calendar event action.
    """

    type_: SuggestionType = Field(SuggestionType.CREATE_CALENDAR_EVENT, serialization_alias='type')
    start_time: str
    end_time: str
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    fallback_url: Optional[str] = None


class RcsOptions(BaseModel):
    """Model for RCS message options.

    Args:
        category (str, Optional): The category of the RCS message.
    """

    category: Optional[RcsCategory] = None


class RcsOptionsCard(RcsOptions):
    """Model for an RCS card message options.

    Args:
        category (str, Optional): The category of the RCS message.
        card_orientation (str): The orientation of the card (HORIZONTAL or VERTICAL).
        image_alignment (str): The alignment of the image on the card (LEFT or RIGHT).
    """

    card_orientation: Optional[RcsCardOrientation] = None
    image_alignment: Optional[RcsImageAlignment] = None


class RcsOptionsCarousel(RcsOptions):
    """Model for an RCS carousel message options.

    Args:
        card_width (str): The width of each card in the carousel (SMALL or MEDIUM).
    """

    card_width: RcsCardWidth


class BaseRcs(BaseMessage):
    """Model for a base RCS message.

    Args:
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (str): The sender's phone number in E.164 format. Don't use a leading plus sign.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    to: PhoneNumber
    from_: str = Field(..., serialization_alias='from', pattern='^[a-zA-Z0-9-_&]+$')
    ttl: Optional[int] = Field(None, ge=300, le=259200)
    channel: ChannelType = ChannelType.RCS


class RcsText(BaseRcs):
    """Model for an RCS text message.

    Args:
        text (str): The text of the message.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (str): The sender's phone number in E.164 format. Don't use a leading plus sign.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    text: str = Field(..., min_length=1, max_length=3072)
    message_type: MessageType = MessageType.TEXT
    suggestions: Optional[
        List[
            Union[
                RcsSuggestionReply,
                RcsSuggestionActionDial,
                RcsSuggestionActionViewLocation,
                RcsSuggestionActionShareLocation,
                RcsSuggestionActionOpenUrl,
                RcsSuggestionActionOpenUrlWebview,
                RcsSuggestionActionCreateCalendarEvent,
            ]
        ]
    ] = Field(None, min_length=1, max_length=11)
    rcs: Optional[RcsOptions] = None


class RcsImage(BaseRcs):
    """Model for an RCS image message.

    Args:
        image (RcsResource): The image resource.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (str): The sender's phone number in E.164 format. Don't use a leading plus sign.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    image: RcsResource
    message_type: MessageType = MessageType.IMAGE


class RcsVideo(BaseRcs):
    """Model for an RCS video message.

    Args:
        video (RcsResource): The video resource.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (str): The sender's phone number in E.164 format. Don't use a leading plus sign.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    video: RcsResource
    message_type: MessageType = MessageType.VIDEO


class RcsFile(BaseRcs):
    """Model for an RCS file message.

    Args:
        file (RcsResource): The file resource.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (str): The sender's phone number in E.164 format. Don't use a leading plus sign.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    file: RcsResource
    message_type: MessageType = MessageType.FILE

class RcsCardContent(BaseModel):
    """Model for the content of an RCS card.

    Args:
        title (str): The title of the card.
        text (str): The text of the card.
        media_url (str): The media URL for the card. Can be an image or a video.
        suggestions (List[Union[RcsSuggestionReply, RcsSuggestionActionDial, RcsSuggestionActionViewLocation, RcsSuggestionActionShareLocation, RcsSuggestionActionOpenUrl, RcsSuggestionActionOpenUrlWebview, RcsSuggestionActionCreateCalendarEvent], Optional): A list of suggestions to include on the card. Can include up to 4 suggestions.
    """

    title: str = Field(..., min_length=1, max_length=200)
    text: str = Field(..., min_length=1, max_length=2000)
    media_url: str
    media_description: Optional[str] = None
    media_height: Optional[RcsMediaHeight] = None
    thumbnail_url: Optional[str] = None
    media_force_refresh: Optional[bool] = None
    suggestions: Optional[
        List[
            Union[
                RcsSuggestionReply,
                RcsSuggestionActionDial,
                RcsSuggestionActionViewLocation,
                RcsSuggestionActionShareLocation,
                RcsSuggestionActionOpenUrl,
                RcsSuggestionActionOpenUrlWebview,
                RcsSuggestionActionCreateCalendarEvent,
            ]
        ]
    ] = Field(None, min_length=1, max_length=4)


class RcsCard(RcsCardContent, BaseRcs):
    """Model for an RCS card message.

    Args:
        title (str): The title of the card.
        description (str): The description of the card.
        media_url (str, Optional): The media URL for the card. Can be an image or a video.
        suggestions (List[Union[RcsSuggestionReply, RcsSuggestionActionDial, RcsSuggestionActionViewLocation, RcsSuggestionActionShareLocation, RcsSuggestionActionOpenUrl, RcsSuggestionActionOpenUrlWebview, RcsSuggestionActionCreateCalendarEvent], Optional): A list of suggestions to include on the card. Can include up to 4 suggestions.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (str): The sender's phone number in E.164 format. Don't use a leading plus sign.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    rcs: Optional[RcsOptionsCard] = None
    message_type: MessageType = MessageType.CARD


class RcsCarousel(BaseRcs):
    """Model for an RCS carousel message.

    Args:
        cards (List[RcsCard]): A list of cards to include in the carousel. Can include up to 10 cards.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (str): The sender's phone number in E.164 format. Don't use a leading plus sign.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    cards: List[RcsCardContent] = Field(..., min_length=1, max_length=10)
    rcs: Optional[RcsOptionsCarousel] = None
    message_type: MessageType = MessageType.CAROUSEL


class RcsCustom(BaseRcs):
    """Model for an RCS custom message.

    Args:
        custom (dict): The custom message data.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (str): The sender's phone number in E.164 format. Don't use a leading plus sign.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    custom: dict
    message_type: MessageType = MessageType.CUSTOM

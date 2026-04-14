from typing import List, Optional, Union

from pydantic import BaseModel, Field
from vonage_utils.types import PhoneNumber

from .base_message import BaseMessage
from .enums import (
    ChannelType,
    MessageType,
    RcsCardOrientation,
    RcsCardWidth,
    RcsCategory,
    RcsImageAlignment,
    RcsMediaHeight,
    SuggestionType,
    UrlWebviewViewMode,
)


class RcsResource(BaseModel):
    """Model for a resource in an RCS message.

    Args:
        url (str): The URL of the resource.
    """

    url: str


class RcsSuggestionBase(BaseModel):
    """Base model for a suggestion in an RCS message.

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
        fallback_url (str, Optional): The URL to open if the device doesn't support the dial action.
    """

    type_: SuggestionType = Field(SuggestionType.DIAL, serialization_alias='type')
    phone_number: PhoneNumber
    fallback_url: Optional[str] = None


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

    type_: SuggestionType = Field(
        SuggestionType.VIEW_LOCATION, serialization_alias='type'
    )
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

    type_: SuggestionType = Field(
        SuggestionType.SHARE_LOCATION, serialization_alias='type'
    )


class RcsSuggestionActionOpenUrl(RcsSuggestionBase):
    """Model for an open URL action suggestion in an RCS message.

    Args:
        text (str): The text to display on the suggestion chip.
        postback_data (str): The data that will be sent via the Inbound Message webhook when the suggestion is selected.
        url (str): The URL to open when the suggestion is selected.
        description (str): A short description of the URL for accessibility purposes.
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
        description (str): A short description of the URL for accessibility purposes.
        view_mode (str, Optional): The view mode for the webview (FULL, TALL, HALF). If not specified, the default view mode for the device will be used.
    """

    type_: SuggestionType = Field(
        SuggestionType.OPEN_URL_IN_WEBVIEW, serialization_alias='type'
    )
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

    type_: SuggestionType = Field(
        SuggestionType.CREATE_CALENDAR_EVENT, serialization_alias='type'
    )
    start_time: str
    end_time: str
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    fallback_url: Optional[str] = None


class RcsOptions(BaseModel):
    """Base model for RCS message options.

    Args:
        category (str, Optional): The category of the RCS message (authentication, transaction, promotion, service, request, acknowledgement).
    """

    category: Optional[RcsCategory] = None


class RcsOptionsCard(RcsOptions):
    """Model for an RCS card message options.

    Args:
        category (str, Optional): The category of the RCS message (authentication, transaction, promotion, service, request, acknowledgement).
        card_orientation (str): The orientation of the card (HORIZONTAL or VERTICAL).
        image_alignment (str): The alignment of the image on the card (LEFT or RIGHT).
    """

    card_orientation: Optional[RcsCardOrientation] = None
    image_alignment: Optional[RcsImageAlignment] = None


class RcsOptionsCarousel(RcsOptions):
    """Model for an RCS carousel message options.

    Args:
        category (str, Optional): The category of the RCS message (authentication, transaction, promotion, service, request, acknowledgement).
        card_width (str): The width of each card in the carousel (SMALL or MEDIUM).
    """

    card_width: RcsCardWidth


class BaseRcs(BaseMessage):
    """Base model for a base RCS message.

    Args:
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (str): The RCS Agent ID.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        trusted_recipient (bool, Optional): Whether the recipient is a trusted recipient. Setting this parameter to true overrides, on a per-message basis, any protections set up via Fraud Defender. Defaults to false.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
        rcs: RcsOptions, Optional: An optional RcsOptions object to include in the message.
    """

    to: PhoneNumber
    from_: str = Field(..., serialization_alias='from', pattern='^[a-zA-Z0-9-_&]+$')
    ttl: Optional[int] = Field(None, ge=20, le=259200)
    trusted_recipient: Optional[bool] = None
    rcs: Optional[RcsOptions] = None
    channel: ChannelType = ChannelType.RCS


class RcsText(BaseRcs):
    """Model for an RCS text message.

    Args:
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (str): The RCS Agent ID.
        text (str): The text of the message.
        suggestions (List, Optional): An optional list of suggestions to include in the message. Can include up to 11 suggestions.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        trusted_recipient (bool, Optional): Whether the recipient is a trusted recipient. Setting this parameter to true overrides, on a per-message basis, any protections set up via Fraud Defender. Defaults to false.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
        rcs: (RcsOptions, Optional): An optional RcsOptions object to include in the message.
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


class RcsImage(BaseRcs):
    """Model for an RCS image message.

    Args:
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (str): The RCS Agent ID.
        image (RcsResource): The image resource.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        trusted_recipient (bool, Optional): Whether the recipient is a trusted recipient. Setting this parameter to true overrides, on a per-message basis, any protections set up via Fraud Defender. Defaults to false.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
        rcs: (RcsOptions, Optional): An optional RcsOptions object to include in the message.
    """

    image: RcsResource
    message_type: MessageType = MessageType.IMAGE


class RcsVideo(BaseRcs):
    """Model for an RCS video message.

    Args:
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (str): The RCS Agent ID.
        video (RcsResource): The video resource.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        trusted_recipient (bool, Optional): Whether the recipient is a trusted recipient. Setting this parameter to true overrides, on a per-message basis, any protections set up via Fraud Defender. Defaults to false.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
        rcs: (RcsOptions, Optional): An optional RcsOptions object to include in the message.
    """

    video: RcsResource
    message_type: MessageType = MessageType.VIDEO


class RcsFile(BaseRcs):
    """Model for an RCS file message.

    Args:
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (str): The RCS Agent ID.
        file (RcsResource): The file resource.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        trusted_recipient (bool, Optional): Whether the recipient is a trusted recipient. Setting this parameter to true overrides, on a per-message basis, any protections set up via Fraud Defender. Defaults to false.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
        rcs: (RcsOptions, Optional): An optional RcsOptions object to include in the message.
    """

    file: RcsResource
    message_type: MessageType = MessageType.FILE


class RcsCard(BaseModel):
    """Base model for the content of an RCS card.

    Args:
        title (str): The title of the card.
        text (str): The text of the card.
        media_url (str): The media URL for the card. Can be an image or a video.
        media_height (str, Optional): The height of the media on the card (SHORT, MEDIUM, TALL).
        media_description (str, Optional): A description of the media for accessibility purposes.
        thumbnail_url (str, Optional): The URL of the thumbnail image for the media. If not specified, the media URL will be used as the thumbnail.
        media_force_refresh (bool, Optional): Whether to force refresh the media on the card. If true, the media will be refreshed on the device even if the media URL is the same as a previous message. Defaults to false.
        suggestions (List, Optional): An optional list of suggestions to include in the message. A card can include up to 4 suggestions.
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


class RcsCardMessage(BaseRcs):
    """Model for an RCS card message.

    Args:
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (str): The sender's phone number in E.164 format. Don't use a leading plus sign.
        card (RcsCard): The content of the card.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        trusted_recipient (bool, Optional): Whether the recipient is a trusted recipient. Setting this parameter to true overrides, on a per-message basis, any protections set up via Fraud Defender. Defaults to false.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
        rcs: (RcsOptionsCard, Optional): An optional RcsOptionsCard object to include in the message.
    """

    card: RcsCard
    rcs: Optional[RcsOptionsCard] = None
    message_type: MessageType = MessageType.CARD


class RcsCarousel(BaseModel):
    """Model for the content of an RCS carousel.

    Args:
        cards (List[RcsCard]): A list of card items to include in the carousel. Can include up to 10 cards.
    """

    cards: List[RcsCard] = Field(..., min_length=2, max_length=10)


class RcsCarouselMessage(BaseRcs):
    """Model for an RCS carousel message.

    Args:
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (str): The sender's phone number in E.164 format. Don't use a leading plus sign.
        carousel (RcsCarousel): The content of the carousel.
        suggestions (List, Optional): An optional list of suggestions to include in the message. Can include up to 11 suggestions.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        trusted_recipient (bool, Optional): Whether the recipient is a trusted recipient. Setting this parameter to true overrides, on a per-message basis, any protections set up via Fraud Defender. Defaults to false.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
        rcs: (RcsOptionsCarousel): An RcsOptionsCarousel object to include in the message.
    """

    carousel: RcsCarousel
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
    rcs: RcsOptionsCarousel
    message_type: MessageType = MessageType.CAROUSEL


class RcsCustom(BaseRcs):
    """Model for an RCS custom message.

    Args:
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (str): The sender's phone number in E.164 format. Don't use a leading plus sign.
        custom (dict): The custom message data.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        trusted_recipient (bool, Optional): Whether the recipient is a trusted recipient. Setting this parameter to true overrides, on a per-message basis, any protections set up via Fraud Defender. Defaults to false.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
        rcs: (RcsOptions, Optional): An optional RcsOptions object to include in the message.
    """

    custom: dict
    message_type: MessageType = MessageType.CUSTOM

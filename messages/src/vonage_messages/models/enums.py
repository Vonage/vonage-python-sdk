from enum import Enum


class MessageType(str, Enum):
    """The type of message."""

    TEXT = 'text'
    IMAGE = 'image'
    AUDIO = 'audio'
    VIDEO = 'video'
    FILE = 'file'
    TEMPLATE = 'template'
    STICKER = 'sticker'
    CUSTOM = 'custom'
    VCARD = 'vcard'
    CARD = 'card'
    CAROUSEL = 'carousel'
    CONTENT = 'content'


class ChannelType(str, Enum):
    """The channel used to send a message."""

    SMS = 'sms'
    MMS = 'mms'
    RCS = 'rcs'
    WHATSAPP = 'whatsapp'
    MESSENGER = 'messenger'
    VIBER = 'viber_service'


class WebhookVersion(str, Enum):
    """Which version of the Messages API will be used to send Status Webhook messages."""

    V0_1 = 'v0.1'
    V1 = 'v1'


class EncodingType(str, Enum):
    TEXT = 'text'
    UNICODE = 'unicode'
    AUTO = 'auto'


class SuggestionType(str, Enum):
    """The type of RCS suggestion."""

    REPLY = 'reply'
    DIAL = 'dial'
    VIEW_LOCATION = 'view_location'
    SHARE_LOCATION = 'share_location'
    OPEN_URL = 'open_url'
    OPEN_URL_IN_WEBVIEW = 'open_url_in_webview'
    CREATE_CALENDAR_EVENT = 'create_calendar_event'


class UrlWebviewViewMode(str, Enum):
    """The view mode for an RCS suggestion that opens a URL in a webview."""

    FULL = 'FULL'
    TALL = 'TALL'
    HALF = 'HALF'


class RcsCategory(str, Enum):
    """The category of an RCS message."""

    ACKNOWLEDGEMENT = 'acknowledgement'
    AUTHENTICATION = 'authentication'
    PROMOTION = 'promotion'
    SERVICE_REQUEST = 'service-request'
    TRANSACTION = 'transaction'


class RcsCardOrientation(str, Enum):
    """The orientation of an RCS card."""

    VERTICAL = 'VERTICAL'
    HORIZONTAL = 'HORIZONTAL'


class RcsImageAlignment(str, Enum):
    """The alignment of an image on an RCS card."""

    LEFT = 'LEFT'
    RIGHT = 'RIGHT'


class RcsCardWidth(str, Enum):
    """The width of a card in an RCS carousel."""

    SMALL = 'SMALL'
    MEDIUM = 'MEDIUM'


class RcsMediaHeight(str, Enum):
    """The height of media on an RCS card."""

    SHORT = 'SHORT'
    MEDIUM = 'MEDIUM'
    TALL = 'TALL'


class MmsContentItemType(str, Enum):
    """The type of a content item in an MMS Content message."""

    IMAGE = 'image'
    AUDIO = 'audio'
    VIDEO = 'video'
    FILE = 'file'
    VCARD = 'vcard'


class ReplyingIndicatorType(str, Enum):
    """The type of a WhatsApp replying indicator."""

    TEXT = 'text'

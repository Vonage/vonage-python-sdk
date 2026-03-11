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
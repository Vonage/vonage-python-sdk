from enum import Enum


class MessageType(str, Enum):
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
    SMS = 'sms'
    MMS = 'mms'
    WHATSAPP = 'whatsapp'
    MESSENGER = 'messenger'
    VIBER = 'viber_service'


class WebhookVersion(str, Enum):
    V0_1 = 'v0.1'
    V1 = 'v1'


class EncodingType(str, Enum):
    TEXT = 'text'
    UNICODE = 'unicode'
    AUTO = 'auto'

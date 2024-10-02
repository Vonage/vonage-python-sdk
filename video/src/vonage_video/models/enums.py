from enum import Enum


class TokenRole(str, Enum):
    SUBSCRIBER = 'subscriber'
    PUBLISHER = 'publisher'
    PUBLISHER_ONLY = 'publisheronly'
    MODERATOR = 'moderator'


class ArchiveMode(str, Enum):
    MANUAL = 'manual'
    ALWAYS = 'always'


class MediaMode(str, Enum):
    ROUTED = 'routed'
    RELAYED = 'relayed'


class P2pPreference(str, Enum):
    DISABLED = 'disabled'
    ALWAYS = 'always'


class LanguageCode(str, Enum):
    EN_US = 'en-US'
    EN_AU = 'en-AU'
    EN_GB = 'en-GB'
    ZH_CN = 'zh-CN'
    FR_FR = 'fr-FR'
    FR_CA = 'fr-CA'
    DE_DE = 'de-DE'
    HI_IN = 'hi-IN'
    IT_IT = 'it-IT'
    JA_JP = 'ja-JP'
    KO_KR = 'ko-KR'
    PT_BR = 'pt-BR'
    TH_TH = 'th-TH'


class AudioSampleRate(int, Enum):
    KHZ_8 = 8000
    KHZ_16 = 16000


class VideoResolution(str, Enum):
    RES_640x480 = '640x480'
    RES_480x640 = '480x640'
    RES_1280x720 = '1280x720'
    RES_720x1280 = '720x1280'
    RES_1920x1080 = '1920x1080'
    RES_1080x1920 = '1080x1920'


class ExperienceComposerStatus(str, Enum):
    STARTING = 'starting'
    STARTED = 'started'
    STOPPED = 'stopped'
    FAILED = 'failed'


class OutputMode(str, Enum):
    COMPOSED = 'composed'
    INDIVIDUAL = 'individual'


class StreamMode(str, Enum):
    AUTO = 'auto'
    MANUAL = 'manual'


class LayoutType(str, Enum):
    BEST_FIT = 'bestFit'
    CUSTOM = 'custom'
    PIP = 'pip'
    VERTICAL_PRESENTATION = 'verticalPresentation'
    HORIZONTAL_PRESENTATION = 'horizontalPresentation'


class ArchiveStatus(str, Enum):
    AVAILABLE = 'available'
    EXPIRED = 'expired'
    FAILED = 'failed'
    PAUSED = 'paused'
    STARTED = 'started'
    STOPPED = 'stopped'
    UPLOADED = 'uploaded'
    DELETED = 'deleted'

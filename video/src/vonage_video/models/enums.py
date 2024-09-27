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

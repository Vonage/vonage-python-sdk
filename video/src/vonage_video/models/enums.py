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

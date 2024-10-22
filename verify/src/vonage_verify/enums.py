from enum import Enum


class ChannelType(str, Enum):
    SILENT_AUTH = 'silent_auth'
    SMS = 'sms'
    WHATSAPP = 'whatsapp'
    VOICE = 'voice'
    EMAIL = 'email'


class Locale(str, Enum):
    EN_US = 'en-us'
    EN_GB = 'en-gb'
    ES_ES = 'es-es'
    ES_MX = 'es-mx'
    ES_US = 'es-us'
    IT_IT = 'it-it'
    FR_FR = 'fr-fr'
    DE_DE = 'de-de'
    RU_RU = 'ru-ru'
    HI_IN = 'hi-in'
    PT_BR = 'pt-br'
    PT_PT = 'pt-pt'
    ID_ID = 'id-id'

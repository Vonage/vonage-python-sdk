from enum import Enum


class NumberType(str, Enum):
    LANDLINE = 'landline'
    MOBILE_LVN = 'mobile-lvn'
    LANDLINE_TOLL_FREE = 'landline-toll-free'


class NumberFeatures(str, Enum):
    SMS = 'SMS'
    VOICE = 'VOICE'
    MMS = 'MMS'
    SMS_VOICE = 'SMS,VOICE'
    SMS_MMS = 'SMS,MMS'
    VOICE_MMS = 'VOICE,MMS'
    SMS_VOICE_MMS = 'SMS,VOICE,MMS'


class VoiceCallbackType(str, Enum):
    SIP = 'sip'
    TEL = 'tel'

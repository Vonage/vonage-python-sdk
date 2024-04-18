from enum import Enum


class Channel(str, Enum):
    PHONE = 'phone'
    SIP = 'sip'
    WEBSOCKET = 'websocket'
    VBC = 'vbc'


class NccoActionType(str, Enum):
    RECORD = 'record'
    CONVERSATION = 'conversation'
    CONNECT = 'connect'
    TALK = 'talk'
    STREAM = 'stream'
    INPUT = 'input'
    NOTIFY = 'notify'


class ConnectEndpointType(str, Enum):
    PHONE = 'phone'
    APP = 'app'
    WEBSOCKET = 'websocket'
    SIP = 'sip'
    VBC = 'vbc'


class CallStatus(str, Enum):
    STARTED = 'started'
    RINGING = 'ringing'
    ANSWERED = 'answered'
    MACHINE = 'machine'
    COMPLETED = 'completed'
    BUSY = 'busy'
    CANCELLED = 'cancelled'
    FAILED = 'failed'
    REJECTED = 'rejected'
    TIMEOUT = 'timeout'
    UNANSWERED = 'unanswered'

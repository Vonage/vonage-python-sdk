from enum import Enum


class Channel(Enum, str):
    PHONE = 'phone'
    SIP = 'sip'
    WEBSOCKET = 'websocket'
    VBC = 'vbc'


class NccoActionType(Enum, str):
    RECORD = 'record'
    CONVERSATION = 'conversation'
    CONNECT = 'connect'
    TALK = 'talk'
    STREAM = 'stream'
    INPUT = 'input'
    NOTIFY = 'notify'


class ConnectEndpointType(Enum, str):
    PHONE = 'phone'
    APP = 'app'
    WEBSOCKET = 'websocket'
    SIP = 'sip'
    VBC = 'vbc'

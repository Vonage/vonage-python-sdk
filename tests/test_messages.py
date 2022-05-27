from util import *
from vonage.errors import InvalidMessageTypeError
from vonage.message_classes import *

def test_invalid_sms_message_type():
    with pytest.raises(InvalidMessageTypeError):
        SmsMessage('image')

def test_invalid_mms_message_type():
    with pytest.raises(InvalidMessageTypeError):
        MmsMessage('text')

def test_invalid_whatsapp_message_type():
    with pytest.raises(InvalidMessageTypeError):
        WhatsAppMessage('vcard')

def test_invalid_messenger_message_type():
    with pytest.raises(InvalidMessageTypeError):
        MessengerMessage('template')

def test_invalid_viber_message_type():
    with pytest.raises(InvalidMessageTypeError):
        ViberMessage('audio')


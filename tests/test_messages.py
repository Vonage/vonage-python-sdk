from util import *
from vonage.errors import InvalidMessageTypeError, MessagesError
from vonage.message_classes import *
from vonage.messages import Messages

def test_invalid_message_channel(messages):
    with pytest.raises(MessagesError):
        messages.send_message(channel='carrier_pigeon')

def test_invalid_message_type(messages):
    with pytest.raises(InvalidMessageTypeError):
        messages.send_message(channel='sms', message_type='video')

def test_invalid_recipient(messages):
    with pytest.raises(MessagesError):
        messages.send_message(channel='sms', message_type='text', to='+441234567890')

def test_invalid_sender(messages):
    with pytest.raises(MessagesError):
        messages.send_message(channel='sms', message_type='text', to='441234567890', frm=1234)

# def test_invalid_sms_message_type():
#     with pytest.raises(InvalidMessageTypeError):
#         SmsMessage('image')

# def test_invalid_mms_message_type():
#     with pytest.raises(InvalidMessageTypeError):
#         MmsMessage('text')

# def test_invalid_whatsapp_message_type():
#     with pytest.raises(InvalidMessageTypeError):
#         WhatsAppMessage('vcard')

# def test_invalid_messenger_message_type():
#     with pytest.raises(InvalidMessageTypeError):
#         MessengerMessage('template')

# def test_invalid_viber_message_type():
#     with pytest.raises(InvalidMessageTypeError):
#         ViberMessage('audio')


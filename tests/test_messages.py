from util import *
from vonage.errors import InvalidMessageTypeError, MessagesError

def test_invalid_message_channel(messages):
    with pytest.raises(MessagesError):
        messages.send_message(channel='carrier_pigeon')

def test_invalid_message_type(messages):
    with pytest.raises(InvalidMessageTypeError):
        messages.send_message(channel='sms', message_type='video')

def test_invalid_recipient_not_string(messages):
    with pytest.raises(MessagesError):
        messages.send_message(channel='sms', message_type='text', to=441234567890)

def test_invalid_recipient_number(messages):
    with pytest.raises(MessagesError):
        messages.send_message(channel='sms', message_type='text', to='+441234567890')

def test_invalid_messenger_recipient(messages):
    with pytest.raises(MessagesError):
        messages.send_message(channel='messenger', message_type='text', to='441234567890')

def test_invalid_sender(messages):
    with pytest.raises(MessagesError):
        messages.send_message(channel='sms', message_type='text', to='441234567890', frm=1234)

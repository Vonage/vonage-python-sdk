from .errors import InvalidMessageTypeError

class BaseMessage(object):
    def __init__(self, to, sender, channel, message_type):
        self.to = to
        self.sender = sender
        self.channel = channel
        self.message_type = message_type

class SmsMessage(BaseMessage):
    valid_message_types = {'text'}
    def __init__(self, message_type='text'):
        if message_type not in self.valid_message_types:
            raise InvalidMessageTypeError

class MmsMessage(BaseMessage):
    valid_message_types = {'image', 'vcard', 'audio', 'video'}
    def __init__(self, message_type):
        if message_type not in self.valid_message_types:
            raise InvalidMessageTypeError
        self.message_type = message_type

class WhatsAppMessage(BaseMessage):
    def __init__(self, message_type):
        self.valid_message_types = {'text', 'image', 'audio', 'video', 'file', 'template', 'custom'}
        if message_type not in self.valid_message_types:
            raise InvalidMessageTypeError
        self.message_type = message_type

class MessengerMessage(BaseMessage):
     def __init__(self, message_type):
        self.valid_message_types = {'text', 'image', 'audio', 'video', 'file'}
        if message_type not in self.valid_message_types:
            raise InvalidMessageTypeError
        self.message_type = message_type

class ViberMessage(BaseMessage):
    def __init__(self, message_type):
        self.valid_message_types = {'text', 'image'}
        if message_type not in self.valid_message_types:
            raise InvalidMessageTypeError
        self.message_type = message_type

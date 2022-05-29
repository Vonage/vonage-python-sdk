import string
from .errors import MessagesError, InvalidMessageTypeError

import re

class Messages:
    valid_message_channels = {'sms', 'mms', 'whatsapp', 'messenger', 'viber'}
    valid_message_types = {
        'sms': {'text'},
        'mms': {'image', 'vcard', 'audio', 'video'},
        'whatsapp': {'text', 'image', 'audio', 'video', 'file', 'template', 'custom'},
        'messenger': {'text', 'image', 'audio', 'video', 'file'},
        'viber': {'text', 'image'}
    }
    
    def __init__(self, client):
        self._client = client

    def send_message(
        self, 
        channel=None, 
        message_type=None, 
        to=None, 
        frm=None,
        opts=None
    ):

        self._channel = channel
        self._message_type = message_type
        self._to = to
        self._frm = frm
        self._opts = opts

        self._validate_send_message_input()

        self._build_request_string()

        # return self._client.post(self._client.api_host(), "/v1/messages", header_auth=True)

    def _validate_send_message_input(self):
        self._check_valid_message_channel()
        self._check_valid_message_type()
        self._check_valid_recipient()
        self._check_sender_string()

    def _check_valid_message_channel(self):
        if self._channel not in Messages.valid_message_channels:
            raise MessagesError(f"""
            '{self._channel}' is an invalid message channel. 
            Must be one of the following types: {self.valid_message_channels}'
            """)

    def _check_valid_message_type(self):
        if self._message_type not in self.valid_message_types[self._channel]:
            raise InvalidMessageTypeError(f"""
                "{self._message_type}" is not a valid message type for channel "{self._channel}". 
                Must be one of the following types: {self.valid_message_types[self._channel]}
            """)

    def _check_valid_recipient(self):
        if not re.search(r'^[1-9]\d{6,14}$', self._to):
            raise MessagesError(f'Message recipient ("to={self._to}") details not in a valid format.')

    def _check_sender_string(self):
        if not isinstance(self._frm, str) or self._frm == "":
            raise MessagesError(f'Message sender ("frm={self._frm}") set incorrectly. Set a valid name for the sender.')

    def _build_request_string(self):
        pass
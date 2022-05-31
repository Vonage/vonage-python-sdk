from .errors import MessagesError

import re

class Messages:
    valid_message_channels = {'sms', 'mms', 'whatsapp', 'messenger', 'viber_service'}
    valid_message_types = {
        'sms': {'text'},
        'mms': {'image', 'vcard', 'audio', 'video'},
        'whatsapp': {'text', 'image', 'audio', 'video', 'file', 'template', 'custom'},
        'messenger': {'text', 'image', 'audio', 'video', 'file'},
        'viber_service': {'text', 'image'}
    }
    
    def __init__(self, client):
        self._client = client

    def send_message(self, params: dict):        
        self._set_instance_attributes(params)
        self._validate_send_message_input()

        self._build_request_string()

        # return self._client.post(self._client.api_host(), "/v1/messages", header_auth=True)

    def _set_instance_attributes(self, params):
        try:
            self._channel = params['channel']
            self._message_type = params['message_type']
            self._to = params['to'] 
            self._from = params['from']
            
            # Message specific checks
            # e.g. for sms this will be an object called 'text': 'hello'
            # and for mms will be something like 'image': {'url': 'myurl.com', 'caption' my photo'}
            self._message = params[self._message_type] 

            # Channel specific checks
            if self._channel == 'whatsapp' and self._message_type == 'template':
                self._whatsapp = params['whatsapp']
            if self._channel == 'messenger' and 'messenger' in params:
                self._messenger = params['messenger']
            if self._channel == 'viber_service':
                self._viber_service = params['viber_service']
        except (KeyError, TypeError):
            raise MessagesError('You must specify all required properties for this channel and message type.')

        if 'client_ref' in params:
            if len(params['client_ref']) <= 40:
                self._client_ref = params['client_ref']
            else:
                raise MessagesError('client_ref can be a maximum of 40 characters.')

    def _validate_send_message_input(self):
        self._check_valid_message_channel()
        self._check_valid_message_type()
        self._check_valid_recipient()
        self._check_valid_sender()
    
    def _check_valid_message_channel(self):
        if self._channel not in Messages.valid_message_channels:
            raise MessagesError(f"""
            '{self._channel}' is an invalid message channel. 
            Must be one of the following types: {self.valid_message_channels}'
            """)

    def _check_valid_message_type(self):
        if self._message_type not in self.valid_message_types[self._channel]:
            raise MessagesError(f"""
                "{self._message_type}" is not a valid message type for channel "{self._channel}". 
                Must be one of the following types: {self.valid_message_types[self._channel]}
            """)

    def _check_valid_recipient(self):
        if not isinstance(self._to, str):
            raise MessagesError(f'Message recipient ("to={self._to}") not in a valid format.')
        elif self._channel != 'messenger' and not re.search(r'^[1-9]\d{6,14}$', self._to):
            raise MessagesError(f'Message recipient number ("to={self._to}") not in a valid format.')
        elif self._channel == 'messenger' and not 0 < len(self._to) < 50:
            raise MessagesError(f'Message recipient ID ("to={self._to}") not in a valid format.')

    def _check_valid_sender(self):
        if not isinstance(self._from, str) or self._from == "":
            raise MessagesError(f'Message sender ("frm={self._from}") set incorrectly. Set a valid name or number for the sender.')


    def _build_request_string(self):
        pass

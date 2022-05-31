from util import *
from vonage.errors import MessagesError

def test_invalid_send_message_params_object(messages):
    with pytest.raises(MessagesError):
        messages.send_message('hi')

def test_invalid_message_channel(messages):
    with pytest.raises(MessagesError):
        messages.send_message({
            'channel': 'carrier_pigeon', 
            'message_type': 'text', 
            'to': '12345678', 
            'from': 'vonage',
            'text': 'my important message'
        })

def test_invalid_message_type(messages):
    with pytest.raises(MessagesError):
        messages.send_message({
            'channel': 'sms', 
            'message_type': 'video',
            'to': '12345678', 
            'from': 'vonage',
            'video': 'my_url.com'
        })

def test_invalid_recipient_not_string(messages):
    with pytest.raises(MessagesError):
        messages.send_message({
            'channel': 'sms', 
            'message_type': 'text',
            'to': 12345678, 
            'from': 'vonage',
            'text': 'my important message'
        })

def test_invalid_recipient_number(messages):
    with pytest.raises(MessagesError):
        messages.send_message({
            'channel': 'sms', 
            'message_type': 'text',
            'to': '+441234567890', 
            'from': 'vonage',
            'text': 'my important message'
        })

def test_invalid_messenger_recipient(messages):
    with pytest.raises(MessagesError):
        messages.send_message({
            'channel': 'messenger', 
            'message_type': 'text',
            'to': '', 
            'from': 'vonage',
            'text': 'my important message'
        })

def test_invalid_sender(messages):
    with pytest.raises(MessagesError):
        messages.send_message({
            'channel': 'sms', 
            'message_type': 'text',
            'to': '441234567890', 
            'from': 1234,
            'text': 'my important message'
        })

def test_set_client_ref(messages):
    messages._set_instance_attributes({
        'channel': 'sms', 
        'message_type': 'text',
        'to': '441234567890', 
        'from': 'vonage',
        'text': 'my important message',
        'client_ref': 'my client reference'
    })
    assert messages._client_ref == 'my client reference'

def test_invalid_client_ref(messages):
    with pytest.raises(MessagesError):
        messages._set_instance_attributes({
        'channel': 'sms', 
        'message_type': 'text',
        'to': '441234567890', 
        'from': 'vonage',
        'text': 'my important message',
        'client_ref': 'my client reference that is far longer than the 40 character limit'
        })

def test_set_whatsapp_template(messages):
    messages._set_instance_attributes({
            'channel': 'whatsapp', 
            'message_type': 'template',
            'to': '', 
            'from': 'vonage',
            'template': {'name': 'namespace:mytemplate'},
            'whatsapp': {'policy': 'deterministic', 'locale': 'en-GB'}
        })

    assert messages._channel == 'whatsapp'    
    assert messages._whatsapp == {'policy': 'deterministic', 'locale': 'en-GB'}

def test_set_messenger_optional_attribute(messages):
    messages._set_instance_attributes({
        'channel': 'messenger', 
        'message_type': 'text',
        'to': 'user_messenger_id', 
        'from': 'vonage',
        'text': 'my important message',
        'messenger': {'category': 'response', 'tag': 'ACCOUNT_UPDATE'}
    })
    assert messages._messenger == {'category': 'response', 'tag': 'ACCOUNT_UPDATE'}

def test_set_viber_service_optional_attribute(messages):
    messages._set_instance_attributes({
        'channel': 'viber_service', 
        'message_type': 'text',
        'to': '44123456789', 
        'from': 'vonage',
        'text': 'my important message',
        'viber_service': {'category': 'transaction', 'ttl': 30, 'type': 'text'}
    })
    assert messages._viber_service == {'category': 'transaction', 'ttl': 30, 'type': 'text'}

from util import *

@responses.activate
def test_send_sms_with_messages_api(messages, dummy_data):
    stub(responses.POST, 'https://api.nexmo.com/v1/messages')

    params = {
        'channel': 'sms', 
        'message_type': 'text', 
        'to': '447123456789', 
        'from': 'Vonage',
        'text': 'Hello from Vonage'
    }

    assert isinstance(messages.send_message(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert b'"from": "Vonage"' in request_body()
    assert b'"to": "447123456789"' in request_body()
    assert b'"text": "Hello from Vonage"' in request_body()

@responses.activate
def test_send_whatsapp_image_with_messages_api(messages, dummy_data):
    stub(responses.POST, 'https://api.nexmo.com/v1/messages')

    params = {
        'channel': 'whatsapp', 
        'message_type': 'image', 
        'to': '447123456789', 
        'from': '440123456789',
        'image': {'url': 'https://example.com/image.jpg', 'caption': 'fake test image'}
    }

    assert isinstance(messages.send_message(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert b'"from": "440123456789"' in request_body()
    assert b'"to": "447123456789"' in request_body()
    assert b'"image": {"url": "https://example.com/image.jpg", "caption": "fake test image"}' in request_body()


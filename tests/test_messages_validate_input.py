from util import *
from vonage.errors import MessagesError


def test_invalid_send_message_params_object(messages):
    with pytest.raises(MessagesError) as err:
        messages.send_message('hi')
    assert (
        str(err.value) == 'Parameters to the send_message method must be specified as a dictionary.'
    )


def test_invalid_message_channel(messages):
    with pytest.raises(MessagesError) as err:
        messages.send_message(
            {
                'channel': 'carrier_pigeon',
                'message_type': 'text',
                'to': '12345678',
                'from': 'vonage',
                'text': 'my important message',
            }
        )
    assert '"carrier_pigeon" is an invalid message channel.' in str(err.value)


def test_invalid_message_type(messages):
    with pytest.raises(MessagesError) as err:
        messages.send_message(
            {
                'channel': 'sms',
                'message_type': 'video',
                'to': '12345678',
                'from': 'vonage',
                'video': 'my_url.com',
            }
        )
    assert '"video" is not a valid message type for channel "sms".' in str(err.value)


def test_invalid_recipient_not_string(messages):
    with pytest.raises(MessagesError) as err:
        messages.send_message(
            {
                'channel': 'sms',
                'message_type': 'text',
                'to': 12345678,
                'from': 'vonage',
                'text': 'my important message',
            }
        )
    assert str(err.value) == 'Message recipient ("to=12345678") not in a valid format.'


def test_invalid_recipient_number(messages):
    with pytest.raises(MessagesError) as err:
        messages.send_message(
            {
                'channel': 'sms',
                'message_type': 'text',
                'to': '+441234567890',
                'from': 'vonage',
                'text': 'my important message',
            }
        )
    assert str(err.value) == 'Message recipient number ("to=+441234567890") not in a valid format.'


def test_invalid_messenger_recipient(messages):
    with pytest.raises(MessagesError) as err:
        messages.send_message(
            {
                'channel': 'messenger',
                'message_type': 'text',
                'to': '',
                'from': 'vonage',
                'text': 'my important message',
            }
        )
    assert str(err.value) == 'Message recipient ID ("to=") not in a valid format.'


def test_invalid_sender(messages):
    with pytest.raises(MessagesError) as err:
        messages.send_message(
            {
                'channel': 'sms',
                'message_type': 'text',
                'to': '441234567890',
                'from': 1234,
                'text': 'my important message',
            }
        )
    assert (
        str(err.value)
        == 'Message sender ("frm=1234") set incorrectly. Set a valid name or number for the sender.'
    )


def test_set_client_ref(messages):
    messages._check_valid_client_ref(
        {
            'channel': 'sms',
            'message_type': 'text',
            'to': '441234567890',
            'from': 'vonage',
            'text': 'my important message',
            'client_ref': 'my client reference',
        }
    )
    assert messages._client_ref == 'my client reference'


def test_invalid_client_ref(messages):
    with pytest.raises(MessagesError) as err:
        messages._check_valid_client_ref(
            {
                'channel': 'sms',
                'message_type': 'text',
                'to': '441234567890',
                'from': 'vonage',
                'text': 'my important message',
                'client_ref': 'my client reference that is, in fact, a small, but significant amount longer than the 100 character limit imposed at this present juncture.',
            }
        )
    assert str(err.value) == 'client_ref can be a maximum of 100 characters.'


def test_whatsapp_template(messages):
    messages.validate_send_message_input(
        {
            'channel': 'whatsapp',
            'message_type': 'template',
            'to': '4412345678912',
            'from': 'vonage',
            'template': {'name': 'namespace:mytemplate'},
            'whatsapp': {'policy': 'deterministic', 'locale': 'en-GB'},
        }
    )


def test_set_messenger_optional_attribute(messages):
    messages.validate_send_message_input(
        {
            'channel': 'messenger',
            'message_type': 'text',
            'to': 'user_messenger_id',
            'from': 'vonage',
            'text': 'my important message',
            'messenger': {'category': 'response', 'tag': 'ACCOUNT_UPDATE'},
        }
    )


def test_set_viber_service_optional_attribute(messages):
    messages.validate_send_message_input(
        {
            'channel': 'viber_service',
            'message_type': 'text',
            'to': '44123456789',
            'from': 'vonage',
            'text': 'my important message',
            'viber_service': {'category': 'transaction', 'ttl': 30, 'type': 'text'},
        }
    )


def test_viber_service_video(messages):
    messages.validate_send_message_input(
        {
            'channel': 'viber_service',
            'message_type': 'video',
            'to': '44123456789',
            'from': 'vonage',
            'video': {
                'url': 'https://example.com/video.mp4',
                'caption': 'Look at this video',
                'thumb_url': 'https://example.com/thumbnail.jpg',
            },
            'viber_service': {
                'category': 'transaction',
                'duration': '120',
                'ttl': 30,
                'type': 'string',
            },
        }
    )


def test_viber_service_file(messages):
    messages.validate_send_message_input(
        {
            'channel': 'viber_service',
            'message_type': 'file',
            'to': '44123456789',
            'from': 'vonage',
            'video': {'url': 'https://example.com/files', 'name': 'example.pdf'},
            'viber_service': {'category': 'transaction', 'ttl': 30, 'type': 'string'},
        }
    )


def test_viber_service_text_action_button(messages):
    messages.validate_send_message_input(
        {
            'channel': 'viber_service',
            'message_type': 'text',
            'to': '44123456789',
            'from': 'vonage',
            'text': 'my important message',
            'viber_service': {
                'category': 'transaction',
                'ttl': 30,
                'type': 'string',
                'action': {'url': 'https://example.com/page1.html', 'text': 'Find out more'},
            },
        }
    )


def test_viber_service_image_action_button(messages):
    messages.validate_send_message_input(
        {
            'channel': 'viber_service',
            'message_type': 'image',
            'to': '44123456789',
            'from': 'vonage',
            'image': {
                'url': 'https://example.com/image.jpg',
                'caption': 'Check out this new promotion',
            },
            'viber_service': {
                'category': 'transaction',
                'ttl': 30,
                'type': 'string',
                'action': {'url': 'https://example.com/page1.html', 'text': 'Find out more'},
            },
        }
    )


def test_incomplete_input(messages):
    with pytest.raises(MessagesError) as err:
        messages.validate_send_message_input(
            {
                'channel': 'viber_service',
                'message_type': 'text',
                'to': '44123456789',
                'from': 'vonage',
                'text': 'my important message',
            }
        )
    assert (
        str(err.value)
        == 'You must specify all required properties for message channel "viber_service".'
    )


def test_whatsapp_sticker_id(messages):
    messages.validate_send_message_input(
        {
            'channel': 'whatsapp',
            'message_type': 'sticker',
            'sticker': {'id': '13aaecab-2485-4255-a0a7-97a2be6906b9'},
            'to': '44123456789',
            'from': 'vonage',
        }
    )


def test_whatsapp_sticker_url(messages):
    messages.validate_send_message_input(
        {
            'channel': 'whatsapp',
            'message_type': 'sticker',
            'sticker': {'url': 'https://example.com/sticker1.webp'},
            'to': '44123456789',
            'from': 'vonage',
        }
    )


def test_whatsapp_sticker_invalid_input_error(messages):
    with pytest.raises(MessagesError) as err:
        messages.validate_send_message_input(
            {
                'channel': 'whatsapp',
                'message_type': 'sticker',
                'sticker': {'my_sticker'},
                'to': '44123456789',
                'from': 'vonage',
            }
        )
    assert (
        str(err.value) == 'Must specify one, and only one, of "id" or "url" in the "sticker" field.'
    )


def test_whatsapp_sticker_exclusive_keys_error(messages):
    with pytest.raises(MessagesError) as err:
        messages.validate_send_message_input(
            {
                'channel': 'whatsapp',
                'message_type': 'sticker',
                'sticker': {
                    'id': '13aaecab-2485-4255-a0a7-97a2be6906b9',
                    'url': 'https://example.com/sticker1.webp',
                },
                'to': '44123456789',
                'from': 'vonage',
            }
        )
    assert (
        str(err.value) == 'Must specify one, and only one, of "id" or "url" in the "sticker" field.'
    )

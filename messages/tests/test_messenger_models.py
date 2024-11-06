from pytest import raises
from vonage_messages.models import (
    MessengerAudio,
    MessengerFile,
    MessengerImage,
    MessengerOptions,
    MessengerResource,
    MessengerText,
    MessengerVideo,
)
from vonage_messages.models.enums import WebhookVersion


def test_messenger_options_validator():
    with raises(ValueError):
        MessengerOptions(category='message_tag')


def test_create_messenger_text():
    messenger_model = MessengerText(
        to='1234567890', from_='1234567890', text='Hello, World!'
    )
    messenger_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'text': 'Hello, World!',
        'channel': 'messenger',
        'message_type': 'text',
    }

    assert messenger_model.model_dump(by_alias=True, exclude_none=True) == messenger_dict


def test_create_messenger_text_all_fields():
    messenger_model = MessengerText(
        to='1234567890',
        from_='1234567890',
        text='Hello, World!',
        messenger=MessengerOptions(category='message_tag', tag='tag'),
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
    )
    messenger_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'text': 'Hello, World!',
        'messenger': {'category': 'message_tag', 'tag': 'tag'},
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1',
        'channel': 'messenger',
        'message_type': 'text',
    }

    assert messenger_model.model_dump(by_alias=True) == messenger_dict


def test_create_messenger_image():
    messenger_model = MessengerImage(
        to='1234567890',
        from_='1234567890',
        image=MessengerResource(url='https://example.com/image.jpg'),
    )
    messenger_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'image': {'url': 'https://example.com/image.jpg'},
        'channel': 'messenger',
        'message_type': 'image',
    }

    assert messenger_model.model_dump(by_alias=True, exclude_none=True) == messenger_dict


def test_create_messenger_image_all_fields():
    messenger_model = MessengerImage(
        to='1234567890',
        from_='1234567890',
        image=MessengerResource(url='https://example.com/image.jpg'),
        messenger=MessengerOptions(category='message_tag', tag='tag'),
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
    )
    messenger_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'image': {'url': 'https://example.com/image.jpg'},
        'messenger': {'category': 'message_tag', 'tag': 'tag'},
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1',
        'channel': 'messenger',
        'message_type': 'image',
    }

    assert messenger_model.model_dump(by_alias=True) == messenger_dict


def test_create_messenger_audio():
    messenger_model = MessengerAudio(
        to='1234567890',
        from_='1234567890',
        audio=MessengerResource(url='https://example.com/audio.mp3'),
    )
    messenger_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'audio': {'url': 'https://example.com/audio.mp3'},
        'channel': 'messenger',
        'message_type': 'audio',
    }

    assert messenger_model.model_dump(by_alias=True, exclude_none=True) == messenger_dict


def test_create_messenger_audio_all_fields():
    messenger_model = MessengerAudio(
        to='1234567890',
        from_='1234567890',
        audio=MessengerResource(url='https://example.com/audio.mp3'),
        messenger=MessengerOptions(category='message_tag', tag='tag'),
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
    )
    messenger_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'audio': {'url': 'https://example.com/audio.mp3'},
        'messenger': {'category': 'message_tag', 'tag': 'tag'},
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1',
        'channel': 'messenger',
        'message_type': 'audio',
    }

    assert messenger_model.model_dump(by_alias=True) == messenger_dict


def test_create_messenger_video():
    messenger_model = MessengerVideo(
        to='1234567890',
        from_='1234567890',
        video=MessengerResource(url='https://example.com/video.mp4'),
    )
    messenger_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'video': {'url': 'https://example.com/video.mp4'},
        'channel': 'messenger',
        'message_type': 'video',
    }

    assert messenger_model.model_dump(by_alias=True, exclude_none=True) == messenger_dict


def test_create_messenger_video_all_fields():
    messenger_model = MessengerVideo(
        to='1234567890',
        from_='1234567890',
        video=MessengerResource(url='https://example.com/video.mp4'),
        messenger=MessengerOptions(category='message_tag', tag='tag'),
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
    )
    messenger_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'video': {'url': 'https://example.com/video.mp4'},
        'messenger': {'category': 'message_tag', 'tag': 'tag'},
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1',
        'channel': 'messenger',
        'message_type': 'video',
    }

    assert messenger_model.model_dump(by_alias=True) == messenger_dict


def test_create_messenger_file():
    messenger_model = MessengerFile(
        to='1234567890',
        from_='1234567890',
        file=MessengerResource(url='https://example.com/file.pdf'),
    )
    messenger_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'file': {'url': 'https://example.com/file.pdf'},
        'channel': 'messenger',
        'message_type': 'file',
    }

    assert messenger_model.model_dump(by_alias=True, exclude_none=True) == messenger_dict


def test_create_messenger_file_all_fields():
    messenger_model = MessengerFile(
        to='1234567890',
        from_='1234567890',
        file=MessengerResource(url='https://example.com/file.pdf'),
        messenger=MessengerOptions(category='message_tag', tag='tag'),
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
    )
    messenger_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'file': {'url': 'https://example.com/file.pdf'},
        'messenger': {'category': 'message_tag', 'tag': 'tag'},
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1',
        'channel': 'messenger',
        'message_type': 'file',
    }

    assert messenger_model.model_dump(by_alias=True) == messenger_dict

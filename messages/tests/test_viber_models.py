from pytest import raises
from vonage_messages.models import (
    ViberAction,
    ViberFile,
    ViberFileOptions,
    ViberFileResource,
    ViberImage,
    ViberImageOptions,
    ViberImageResource,
    ViberText,
    ViberTextOptions,
    ViberVideo,
    ViberVideoOptions,
    ViberVideoResource,
)
from vonage_messages.models.enums import WebhookVersion


def test_viber_video_options_validator():
    with raises(ValueError):
        ViberVideoOptions(duration='601', file_size='10')

    with raises(ValueError):
        ViberVideoOptions(duration='100', file_size='201')


def test_create_viber_text():
    viber_model = ViberText(to='1234567890', from_='1234567890', text='Hello, World!')
    viber_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'text': 'Hello, World!',
        'channel': 'viber_service',
        'message_type': 'text',
    }

    assert viber_model.model_dump(by_alias=True, exclude_none=True) == viber_dict


def test_create_viber_text_all_fields():
    viber_model = ViberText(
        to='1234567890',
        from_='1234567890',
        text='Hello, World!',
        viber_service=ViberTextOptions(
            category='transaction',
            ttl=30,
            type='string',
            action=ViberAction(url='https://example.com', text='text'),
        ),
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
    )
    viber_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'text': 'Hello, World!',
        'viber_service': {
            'category': 'transaction',
            'ttl': 30,
            'type': 'string',
            'action': {'url': 'https://example.com', 'text': 'text'},
        },
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1',
        'channel': 'viber_service',
        'message_type': 'text',
    }

    assert viber_model.model_dump(by_alias=True) == viber_dict


def test_create_viber_image():
    viber_model = ViberImage(
        to='1234567890',
        from_='1234567890',
        image=ViberImageResource(url='https://example.com/image.jpg'),
    )
    viber_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'image': {'url': 'https://example.com/image.jpg'},
        'channel': 'viber_service',
        'message_type': 'image',
    }

    assert viber_model.model_dump(by_alias=True, exclude_none=True) == viber_dict


def test_create_viber_image_all_fields():
    viber_model = ViberImage(
        to='1234567890',
        from_='1234567890',
        image=ViberImageResource(url='https://example.com/image.jpg', caption='caption'),
        viber_service=ViberImageOptions(
            category='transaction',
            ttl=30,
            type='string',
            action=ViberAction(url='https://example.com', text='text'),
        ),
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
    )
    viber_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'image': {'url': 'https://example.com/image.jpg', 'caption': 'caption'},
        'viber_service': {
            'category': 'transaction',
            'ttl': 30,
            'type': 'string',
            'action': {'url': 'https://example.com', 'text': 'text'},
        },
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1',
        'channel': 'viber_service',
        'message_type': 'image',
    }

    assert viber_model.model_dump(by_alias=True) == viber_dict


def test_create_viber_video():
    viber_model = ViberVideo(
        to='1234567890',
        from_='1234567890',
        video=ViberVideoResource(
            url='https://example.com/video.mp4', thumb_url='https://example.com/thumb.jpg'
        ),
        viber_service=ViberVideoOptions(duration='100', file_size='10'),
    )
    viber_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'video': {
            'url': 'https://example.com/video.mp4',
            'thumb_url': 'https://example.com/thumb.jpg',
        },
        'viber_service': {'duration': '100', 'file_size': '10'},
        'channel': 'viber_service',
        'message_type': 'video',
    }

    assert viber_model.model_dump(by_alias=True, exclude_none=True) == viber_dict


def test_create_viber_video_all_fields():
    viber_model = ViberVideo(
        to='1234567890',
        from_='1234567890',
        video=ViberVideoResource(
            url='https://example.com/video.mp4',
            thumb_url='https://example.com/thumb.jpg',
            caption='caption',
        ),
        viber_service=ViberVideoOptions(
            duration='100',
            file_size='10',
            category='transaction',
            ttl=30,
            type='string',
        ),
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
    )
    viber_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'video': {
            'url': 'https://example.com/video.mp4',
            'thumb_url': 'https://example.com/thumb.jpg',
            'caption': 'caption',
        },
        'viber_service': {
            'duration': '100',
            'file_size': '10',
            'category': 'transaction',
            'ttl': 30,
            'type': 'string',
        },
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1',
        'channel': 'viber_service',
        'message_type': 'video',
    }

    assert viber_model.model_dump(by_alias=True) == viber_dict


def test_create_viber_file():
    viber_model = ViberFile(
        to='1234567890',
        from_='1234567890',
        file=ViberFileResource(url='https://example.com/file.pdf'),
    )
    viber_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'file': {'url': 'https://example.com/file.pdf'},
        'channel': 'viber_service',
        'message_type': 'file',
    }

    assert viber_model.model_dump(by_alias=True, exclude_none=True) == viber_dict


def test_create_viber_file_all_fields():
    viber_model = ViberFile(
        to='1234567890',
        from_='1234567890',
        file=ViberFileResource(url='https://example.com/file.pdf', name='file.pdf'),
        viber_service=ViberFileOptions(
            category='transaction',
            ttl=30,
            type='string',
        ),
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
    )
    viber_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'file': {'url': 'https://example.com/file.pdf', 'name': 'file.pdf'},
        'viber_service': {
            'category': 'transaction',
            'ttl': 30,
            'type': 'string',
        },
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1',
        'channel': 'viber_service',
        'message_type': 'file',
    }

    assert viber_model.model_dump(by_alias=True) == viber_dict

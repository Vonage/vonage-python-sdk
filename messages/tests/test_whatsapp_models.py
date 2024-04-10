from copy import deepcopy

from vonage_messages.enums import WebhookVersion
from vonage_messages.models import (
    WhatsappAudio,
    WhatsappAudioResource,
    WhatsappContext,
    WhatsappCustom,
    WhatsappFile,
    WhatsappFileResource,
    WhatsappImage,
    WhatsappImageResource,
    WhatsappSticker,
    WhatsappStickerId,
    WhatsappStickerUrl,
    WhatsappTemplate,
    WhatsappTemplateResource,
    WhatsappTemplateSettings,
    WhatsappText,
    WhatsappVideo,
    WhatsappVideoResource,
)


def test_whatsapp_text():
    whatsapp_model = WhatsappText(
        to='1234567890',
        from_='1234567890',
        text='Hello, World!',
    )
    whatsapp_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'text': 'Hello, World!',
        'channel': 'whatsapp',
        'message_type': 'text',
    }

    assert whatsapp_model.model_dump(by_alias=True, exclude_none=True) == whatsapp_dict


def test_whatsapp_text_all_fields():
    whatsapp_model = WhatsappText(
        to='1234567890',
        from_='1234567890',
        text='Hello, World!',
        context=WhatsappContext(
            message_uuid='uuid',
        ),
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
    )
    whatsapp_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'text': 'Hello, World!',
        'context': {'message_uuid': 'uuid'},
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1',
        'channel': 'whatsapp',
        'message_type': 'text',
    }

    assert whatsapp_model.model_dump(by_alias=True) == whatsapp_dict
    whatsapp_pre_dict = deepcopy(whatsapp_dict)
    whatsapp_pre_dict['from_'] = '1234567890'
    whatsapp_model_from_dict = WhatsappText(**whatsapp_pre_dict)
    assert whatsapp_model_from_dict.model_dump(by_alias=True) == whatsapp_dict


def test_whatsapp_image():
    whatsapp_model = WhatsappImage(
        to='1234567890',
        from_='1234567890',
        image=WhatsappImageResource(url='https://example.com/image.jpg'),
    )
    whatsapp_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'image': {'url': 'https://example.com/image.jpg'},
        'channel': 'whatsapp',
        'message_type': 'image',
    }

    assert whatsapp_model.model_dump(by_alias=True, exclude_none=True) == whatsapp_dict


def test_whatsapp_image_all_fields():
    whatsapp_model = WhatsappImage(
        to='1234567890',
        from_='1234567890',
        image=WhatsappImageResource(
            url='https://example.com/image.jpg',
            caption='Image caption',
        ),
        context=WhatsappContext(
            message_uuid='uuid',
        ),
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
    )
    whatsapp_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'image': {
            'url': 'https://example.com/image.jpg',
            'caption': 'Image caption',
        },
        'context': {'message_uuid': 'uuid'},
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1',
        'channel': 'whatsapp',
        'message_type': 'image',
    }

    assert whatsapp_model.model_dump(by_alias=True) == whatsapp_dict


def test_whatsapp_audio():
    whatsapp_model = WhatsappAudio(
        to='1234567890',
        from_='1234567890',
        audio=WhatsappAudioResource(url='https://example.com/audio.mp3'),
    )
    whatsapp_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'audio': {'url': 'https://example.com/audio.mp3'},
        'channel': 'whatsapp',
        'message_type': 'audio',
    }

    assert whatsapp_model.model_dump(by_alias=True, exclude_none=True) == whatsapp_dict


def test_whatsapp_audio_all_fields():
    whatsapp_model = WhatsappAudio(
        to='1234567890',
        from_='1234567890',
        audio=WhatsappAudioResource(
            url='https://example.com/audio.mp3',
        ),
        context=WhatsappContext(
            message_uuid='uuid',
        ),
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
    )
    whatsapp_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'audio': {'url': 'https://example.com/audio.mp3'},
        'context': {'message_uuid': 'uuid'},
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1',
        'channel': 'whatsapp',
        'message_type': 'audio',
    }

    assert whatsapp_model.model_dump(by_alias=True) == whatsapp_dict


def test_whatsapp_video():
    whatsapp_model = WhatsappVideo(
        to='1234567890',
        from_='1234567890',
        video=WhatsappVideoResource(url='https://example.com/video.mp4'),
    )
    whatsapp_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'video': {'url': 'https://example.com/video.mp4'},
        'channel': 'whatsapp',
        'message_type': 'video',
    }

    assert whatsapp_model.model_dump(by_alias=True, exclude_none=True) == whatsapp_dict


def test_whatsapp_video_all_fields():
    whatsapp_model = WhatsappVideo(
        to='1234567890',
        from_='1234567890',
        video=WhatsappVideoResource(
            url='https://example.com/video.mp4',
            caption='Video caption',
        ),
        context=WhatsappContext(
            message_uuid='uuid',
        ),
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
    )
    whatsapp_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'video': {
            'url': 'https://example.com/video.mp4',
            'caption': 'Video caption',
        },
        'context': {'message_uuid': 'uuid'},
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1',
        'channel': 'whatsapp',
        'message_type': 'video',
    }

    assert whatsapp_model.model_dump(by_alias=True) == whatsapp_dict


def test_whatsapp_file():
    whatsapp_model = WhatsappFile(
        to='1234567890',
        from_='1234567890',
        file=WhatsappFileResource(url='https://example.com/file.pdf'),
    )
    whatsapp_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'file': {'url': 'https://example.com/file.pdf'},
        'channel': 'whatsapp',
        'message_type': 'file',
    }

    assert whatsapp_model.model_dump(by_alias=True, exclude_none=True) == whatsapp_dict


def test_whatsapp_file_all_fields():
    whatsapp_model = WhatsappFile(
        to='1234567890',
        from_='1234567890',
        file=WhatsappFileResource(
            url='https://example.com/file.pdf',
            caption='File caption',
            name='file.pdf',
        ),
        context=WhatsappContext(
            message_uuid='uuid',
        ),
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
    )
    whatsapp_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'file': {
            'url': 'https://example.com/file.pdf',
            'caption': 'File caption',
            'name': 'file.pdf',
        },
        'context': {'message_uuid': 'uuid'},
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1',
        'channel': 'whatsapp',
        'message_type': 'file',
    }

    assert whatsapp_model.model_dump(by_alias=True) == whatsapp_dict


def test_whatsapp_template():
    whatsapp_model = WhatsappTemplate(
        to='1234567890',
        from_='1234567890',
        template=WhatsappTemplateResource(name='template'),
    )
    whatsapp_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'template': {'name': 'template'},
        'whatsapp': {'locale': 'en_US'},
        'channel': 'whatsapp',
        'message_type': 'template',
    }

    assert whatsapp_model.model_dump(by_alias=True, exclude_none=True) == whatsapp_dict


def test_whatsapp_template_all_fields():
    whatsapp_model = WhatsappTemplate(
        to='1234567890',
        from_='1234567890',
        template=WhatsappTemplateResource(
            name='template', parameters=['param1', 'param2']
        ),
        whatsapp=WhatsappTemplateSettings(locale='es_ES', policy='deterministic'),
        context=WhatsappContext(message_uuid='uuid'),
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
    )
    whatsapp_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'template': {'name': 'template', 'parameters': ['param1', 'param2']},
        'whatsapp': {'locale': 'es_ES', 'policy': 'deterministic'},
        'context': {'message_uuid': 'uuid'},
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1',
        'channel': 'whatsapp',
        'message_type': 'template',
    }

    assert whatsapp_model.model_dump(by_alias=True) == whatsapp_dict


def test_whatsapp_sticker_url():
    whatsapp_model = WhatsappSticker(
        to='1234567890',
        from_='1234567890',
        sticker=WhatsappStickerUrl(url='https://example.com/sticker.webp'),
    )
    whatsapp_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'sticker': {'url': 'https://example.com/sticker.webp'},
        'channel': 'whatsapp',
        'message_type': 'sticker',
    }

    assert whatsapp_model.model_dump(by_alias=True, exclude_none=True) == whatsapp_dict


def test_whatsapp_sticker_id():
    whatsapp_model = WhatsappSticker(
        to='1234567890', from_='1234567890', sticker=WhatsappStickerId(id='sticker-id')
    )
    whatsapp_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'sticker': {'id': 'sticker-id'},
        'channel': 'whatsapp',
        'message_type': 'sticker',
    }

    assert whatsapp_model.model_dump(by_alias=True, exclude_none=True) == whatsapp_dict


def test_whatsapp_custom():
    whatsapp_model = WhatsappCustom(to='1234567890', from_='1234567890')
    whatsapp_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'channel': 'whatsapp',
        'message_type': 'custom',
    }

    assert whatsapp_model.model_dump(by_alias=True, exclude_none=True) == whatsapp_dict


def test_whatsapp_custom_all_fields():
    whatsapp_model = WhatsappCustom(
        to='1234567890',
        from_='1234567890',
        custom={'key': 'value'},
        context=WhatsappContext(message_uuid='uuid'),
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
    )
    whatsapp_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'custom': {'key': 'value'},
        'context': {'message_uuid': 'uuid'},
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1',
        'channel': 'whatsapp',
        'message_type': 'custom',
    }

    assert whatsapp_model.model_dump(by_alias=True) == whatsapp_dict

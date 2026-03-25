import pytest
from pydantic import ValidationError
from vonage_messages.models import MmsAudio, MmsFile, MmsImage, MmsResource, MmsText, MmsVcard, MmsVideo
from vonage_messages.models.enums import WebhookVersion


def test_create_mms_resource():
    mms_resource = MmsResource(
        url='https://example.com/resource',
    )
    mms_resource_dict = {
        'url': 'https://example.com/resource',
    }

    assert mms_resource.model_dump(exclude_none=True) == mms_resource_dict


def test_create_mms_resource_with_caption():
    mms_resource = MmsResource(
        url='https://example.com/resource',
        caption='Resource caption',
    )
    mms_resource_dict = {
        'url': 'https://example.com/resource',
        'caption': 'Resource caption',
    }

    assert mms_resource.model_dump(exclude_none=True) == mms_resource_dict


def test_create_mms_resource_without_url():
    with pytest.raises(ValidationError) as err:
        mms_resource = MmsResource(
            caption='Resource caption',
        )
    assert "Field required" in str(err.value)


def test_create_mms_resource_with_caption_too_short():
    with pytest.raises(ValidationError) as err:
        mms_resource = MmsResource(
            url='https://example.com/resource',
            caption='',
        )
    assert "String should have at least 1 character" in str(err.value)


def test_create_mms_resource_with_caption_too_long():
    with pytest.raises(ValidationError) as err:
        mms_resource = MmsResource(
            url='https://example.com/resource',
            caption='a' * 3001,
        )
    assert "String should have at most 3000 characters" in str(err.value)


def test_create_mms_text():
    mms_model = MmsText(
        to='1234567890',
        from_='1234567890',
        text='Hello, world!',
    )
    mms_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'text': 'Hello, world!',
        'channel': 'mms',
        'message_type': 'text',
    }

    assert mms_model.model_dump(by_alias=True, exclude_none=True) == mms_dict


def test_create_mms_text_all_fields():
    mms_model = MmsText(
        to='1234567890',
        from_='1234567890',
        text='Hello, world!',
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
        ttl=600,
        trusted_recipient=True,
    )
    mms_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'text': 'Hello, world!',
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1',
        'ttl': 600,
        'trusted_recipient': True,
        'channel': 'mms',
        'message_type': 'text',
    }

    assert mms_model.model_dump(by_alias=True) == mms_dict


def test_create_mms_image():
    mms_model = MmsImage(
        to='1234567890',
        from_='1234567890',
        image=MmsResource(
            url='https://example.com/image.jpg',
        ),
    )
    mms_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'image': {
            'url': 'https://example.com/image.jpg',
        },
        'channel': 'mms',
        'message_type': 'image',
    }

    assert mms_model.model_dump(by_alias=True, exclude_none=True) == mms_dict


def test_create_mms_image_all_fields():
    mms_model = MmsImage(
        to='1234567890',
        from_='1234567890',
        image=MmsResource(
            url='https://example.com/image.jpg',
            caption='Image caption',
        ),
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
        ttl=600,
        trusted_recipient=True,
    )
    mms_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'image': {
            'url': 'https://example.com/image.jpg',
            'caption': 'Image caption',
        },
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1',
        'ttl': 600,
        'trusted_recipient': True,
        'channel': 'mms',
        'message_type': 'image',
    }

    assert mms_model.model_dump(by_alias=True) == mms_dict


def test_create_mms_vcard():
    mms_model = MmsVcard(
        to='1234567890',
        from_='1234567890',
        vcard=MmsResource(
            url='https://example.com/vcard.vcf',
        ),
    )
    mms_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'vcard': {
            'url': 'https://example.com/vcard.vcf',
        },
        'channel': 'mms',
        'message_type': 'vcard',
    }

    assert mms_model.model_dump(by_alias=True, exclude_none=True) == mms_dict


def test_create_mms_vcard_all_fields():
    mms_model = MmsVcard(
        to='1234567890',
        from_='1234567890',
        vcard=MmsResource(
            url='https://example.com/vcard.vcf',
            caption='Vcard caption',
        ),
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
        ttl=600,
        trusted_recipient=True,
    )
    mms_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'vcard': {
            'url': 'https://example.com/vcard.vcf',
            'caption': 'Vcard caption',
        },
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1',
        'ttl': 600,
        'trusted_recipient': True,
        'channel': 'mms',
        'message_type': 'vcard',
    }

    assert mms_model.model_dump(by_alias=True) == mms_dict


def test_create_mms_audio():
    mms_model = MmsAudio(
        to='1234567890',
        from_='1234567890',
        audio=MmsResource(
            url='https://example.com/audio.mp3',
        ),
    )
    mms_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'audio': {
            'url': 'https://example.com/audio.mp3',
        },
        'channel': 'mms',
        'message_type': 'audio',
    }

    assert mms_model.model_dump(by_alias=True, exclude_none=True) == mms_dict


def test_create_mms_audio_all_fields():
    mms_model = MmsAudio(
        to='1234567890',
        from_='1234567890',
        audio=MmsResource(
            url='https://example.com/audio.mp3',
            caption='Audio caption',
        ),
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
        ttl=600,
        trusted_recipient=True,
    )
    mms_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'audio': {
            'url': 'https://example.com/audio.mp3',
            'caption': 'Audio caption',
        },
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1',
        'ttl': 600,
        'trusted_recipient': True,
        'channel': 'mms',
        'message_type': 'audio',
    }

    assert mms_model.model_dump(by_alias=True) == mms_dict


def test_create_mms_video():
    mms_model = MmsVideo(
        to='1234567890',
        from_='1234567890',
        video=MmsResource(
            url='https://example.com/video.mp4',
        ),
    )
    mms_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'video': {
            'url': 'https://example.com/video.mp4',
        },
        'channel': 'mms',
        'message_type': 'video',
    }

    assert mms_model.model_dump(by_alias=True, exclude_none=True) == mms_dict


def test_create_mms_video_all_fields():
    mms_model = MmsVideo(
        to='1234567890',
        from_='1234567890',
        video=MmsResource(
            url='https://example.com/video.mp4',
            caption='Video caption',
        ),
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
        ttl=600,
        trusted_recipient=True,
    )
    mms_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'video': {
            'url': 'https://example.com/video.mp4',
            'caption': 'Video caption',
        },
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1',
        'ttl': 600,
        'trusted_recipient': True,
        'channel': 'mms',
        'message_type': 'video',
    }

    assert mms_model.model_dump(by_alias=True) == mms_dict


def test_create_mms_file():
    mms_model = MmsFile(
        to='1234567890',
        from_='1234567890',
        file=MmsResource(
            url='https://example.com/file.pdf',
        ),
    )
    mms_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'file': {
            'url': 'https://example.com/file.pdf',
        },
        'channel': 'mms',
        'message_type': 'file',
    }

    assert mms_model.model_dump(by_alias=True, exclude_none=True) == mms_dict


def test_create_mms_file_all_fields():
    mms_model = MmsFile(
        to='1234567890',
        from_='1234567890',
        file=MmsResource(
            url='https://example.com/file.pdf',
            caption='File caption',
        ),
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
        ttl=600,
        trusted_recipient=True,
    )
    mms_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'file': {
            'url': 'https://example.com/file.pdf',
            'caption': 'File caption',
        },
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1',
        'ttl': 600,
        'trusted_recipient': True,
        'channel': 'mms',
        'message_type': 'file',
    }

    assert mms_model.model_dump(by_alias=True) == mms_dict

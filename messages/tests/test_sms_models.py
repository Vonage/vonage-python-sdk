from vonage_messages.models import Sms, SmsOptions
from vonage_messages.models.enums import EncodingType, WebhookVersion


def test_create_sms():
    sms_model = Sms(
        to='1234567890',
        from_='1234567890',
        text='Hello, World!',
    )
    sms_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'text': 'Hello, World!',
        'channel': 'sms',
        'message_type': 'text',
    }

    assert sms_model.model_dump(by_alias=True, exclude_none=True) == sms_dict


def test_create_sms_all_fields():
    sms_model = Sms(
        to='1234567890',
        from_='1234567890',
        text='Hello, World!',
        sms=SmsOptions(
            encoding_type=EncodingType.TEXT,
            content_id='content-id',
            entity_id='entity-id',
        ),
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
        ttl=600,
    )
    sms_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'text': 'Hello, World!',
        'sms': {
            'encoding_type': 'text',
            'content_id': 'content-id',
            'entity_id': 'entity-id',
        },
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1',
        'ttl': 600,
        'channel': 'sms',
        'message_type': 'text',
    }

    assert sms_model.model_dump(by_alias=True) == sms_dict

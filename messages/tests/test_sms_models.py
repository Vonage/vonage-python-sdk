import pytest
from pydantic import ValidationError
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
            pool_id='abc123',
        ),
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
        ttl=600,
        trusted_recipient=True,
    )
    sms_dict = {
        'to': '1234567890',
        'from': '1234567890',
        'text': 'Hello, World!',
        'sms': {
            'encoding_type': 'text',
            'content_id': 'content-id',
            'entity_id': 'entity-id',
            'pool_id': 'abc123',
        },
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1',
        'ttl': 600,
        'trusted_recipient': True,
        'channel': 'sms',
        'message_type': 'text',
    }

    assert sms_model.model_dump(by_alias=True) == sms_dict


def test_create_sms_text_too_long():
    with pytest.raises(ValidationError) as err:
        Sms(
            to='1234567890',
            from_='1234567890',
            text='a' * 1001,
        )
    assert 'String should have at most 1000 characters' in str(err.value)


def test_create_sms_with_invalid_encoding_type():
    with pytest.raises(ValidationError) as err:
        Sms(
            to='1234567890',
            from_='1234567890',
            text='Hello, World!',
            sms=SmsOptions(encoding_type='invalid'),
        )
    assert 'Input should be' in str(err.value)


def test_create_sms_ttl_too_short():
    with pytest.raises(ValidationError) as err:
        Sms(
            to='1234567890',
            from_='1234567890',
            text='Hello, World!',
            ttl=19,
        )
    assert 'Number should be greater than or equal to 20' in str(err.value)


def test_create_sms_ttl_too_long():
    with pytest.raises(ValidationError) as err:
        Sms(
            to='1234567890',
            from_='1234567890',
            text='Hello, World!',
            ttl=604801,
        )
    assert 'Number should be less than or equal to 604800' in str(err.value)

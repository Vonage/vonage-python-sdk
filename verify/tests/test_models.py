from pytest import raises
from vonage_verify.enums import ChannelType, Locale
from vonage_verify.errors import VerifyError
from vonage_verify.requests import *


def test_create_silent_auth_channel():
    params = {
        'channel': ChannelType.SILENT_AUTH,
        'to': '1234567890',
        'redirect_url': 'https://example.com',
        'sandbox': True,
    }
    channel = SilentAuthChannel(**params)

    assert channel.model_dump() == params


def test_create_sms_channel():
    params = {
        'channel': ChannelType.SMS,
        'to': '1234567890',
        'from_': 'Vonage',
        'entity_id': '12345678901234567890',
        'content_id': '12345678901234567890',
        'app_hash': '12345678901',
    }
    channel = SmsChannel(**params)

    assert channel.model_dump() == params
    assert channel.model_dump(by_alias=True)['from'] == 'Vonage'

    params['from_'] = 'this.is!invalid'
    with raises(VerifyError):
        SmsChannel(**params)


def test_create_whatsapp_channel():
    params = {
        'channel': ChannelType.WHATSAPP,
        'to': '1234567890',
        'from_': 'Vonage',
    }
    channel = WhatsappChannel(**params)

    assert channel.model_dump() == params
    assert channel.model_dump(by_alias=True)['from'] == 'Vonage'

    params['from_'] = 'this.is!invalid'
    with raises(VerifyError):
        WhatsappChannel(**params)


def test_create_voice_channel():
    params = {
        'channel': ChannelType.VOICE,
        'to': '1234567890',
    }
    channel = VoiceChannel(**params)

    assert channel.model_dump() == params


def test_create_email_channel():
    params = {
        'channel': ChannelType.EMAIL,
        'to': 'customer@example.com',
        'from_': 'vonage@vonage.com',
    }
    channel = EmailChannel(**params)

    assert channel.model_dump() == params
    assert channel.model_dump(by_alias=True)['from'] == 'vonage@vonage.com'


def test_create_verify_request():
    silent_auth_channel = SilentAuthChannel(
        channel=ChannelType.SILENT_AUTH, to='1234567890'
    )

    sms_channel = SmsChannel(channel=ChannelType.SMS, to='1234567890', from_='Vonage')
    params = {
        'brand': 'Vonage',
        'workflow': [sms_channel],
    }
    # Basic request

    verify_request = VerifyRequest(**params)
    assert verify_request.brand == 'Vonage'
    assert verify_request.workflow == [sms_channel]

    # Multiple channel request
    workflow = [
        SilentAuthChannel(channel=ChannelType.SILENT_AUTH, to='1234567890'),
        SmsChannel(channel=ChannelType.SMS, to='1234567890', from_='Vonage'),
        WhatsappChannel(channel=ChannelType.WHATSAPP, to='1234567890', from_='Vonage'),
        VoiceChannel(channel=ChannelType.VOICE, to='1234567890'),
        EmailChannel(channel=ChannelType.EMAIL, to='customer@example.com'),
    ]
    params = {
        'brand': 'Vonage',
        'workflow': workflow,
    }
    verify_request = VerifyRequest(**params)
    assert verify_request.brand == 'Vonage'
    assert verify_request.workflow == workflow

    # All fields
    params = {
        'brand': 'Vonage',
        'workflow': [silent_auth_channel, sms_channel, sms_channel],
        'locale': Locale.EN_GB,
        'channel_timeout': 60,
        'client_ref': 'my-client-ref',
        'code_length': 6,
        'code': '123456',
    }
    verify_request = VerifyRequest(**params)
    assert verify_request.brand == 'Vonage'
    assert verify_request.workflow == [silent_auth_channel, sms_channel, sms_channel]
    assert verify_request.locale == Locale.EN_GB
    assert verify_request.channel_timeout == 60
    assert verify_request.client_ref == 'my-client-ref'
    assert verify_request.code_length == 6
    assert verify_request.code == '123456'


def test_create_verify_request_error():
    params = {
        'brand': 'Vonage',
        'workflow': [
            SmsChannel(channel=ChannelType.SMS, to='1234567890', from_='Vonage'),
            SilentAuthChannel(channel=ChannelType.SILENT_AUTH, to='1234567890'),
        ],
    }
    with raises(VerifyError) as e:
        VerifyRequest(**params)
    assert e.match('must be the first channel')

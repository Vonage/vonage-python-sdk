from vonage_voice.models import AnswerWebhook


def test_answer_webhook_sipheader_user_to_user_alias():
    payload = {
        'to': '442079460000',
        'from': '447700900000',
        'uuid': 'aaaaaaaa-bbbb-cccc-dddd-0123456789ab',
        'conversation_uuid': 'CON-aaaaaaaa-bbbb-cccc-dddd-0123456789ab',
        'SipHeader_User-to-User': '1234567890abcdef;encoding=hex',
    }

    hook = AnswerWebhook(**payload)

    assert hook.to == '442079460000'
    assert hook.from_ == '447700900000'
    assert (
        hook.sipheader_user_to_user == '1234567890abcdef;encoding=hex'
    ), 'Field should be populated from SipHeader_User-to-User'

    dumped = hook.model_dump(by_alias=True, exclude_none=True)
    assert (
        dumped['SipHeader_User-to-User'] == '1234567890abcdef;encoding=hex'
    ), 'Field should serialize back with the SipHeader_User-to-User key'

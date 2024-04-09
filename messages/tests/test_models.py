from vonage_verify_v2.enums import ChannelType
from vonage_verify_v2.requests import *


def test_create_silent_auth_channel():
    params = {
        'channel': ChannelType.SILENT_AUTH,
        'to': '1234567890',
        'redirect_url': 'https://example.com',
        'sandbox': True,
    }
    channel = SilentAuthChannel(**params)

    assert channel.model_dump() == params

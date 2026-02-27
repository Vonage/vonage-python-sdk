from vonage_users.common import WebsocketChannel


def test_websocket_channel_24k_audio():
    channel = WebsocketChannel(
        uri="wss://example.com/socket", content_type="audio/l16;rate=24000"
    )
    assert channel.model_dump(by_alias=True)["content-type"] == "audio/l16;rate=24000"

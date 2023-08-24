def test_getters(client, dummy_data):
    assert client.host() == dummy_data.host
    assert client.api_host() == dummy_data.api_host


def test_setters(client, dummy_data):
    try:
        client.host('host.vonage.com')
        client.api_host('host.vonage.com')
        assert client.host() != dummy_data.host
        assert client.api_host() != dummy_data.api_host
    except:
        assert False

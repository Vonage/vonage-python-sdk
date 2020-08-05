from util import *

@responses.activate
def test_getters(client, dummy_data):
    assert client.host() == dummy_data.host
    assert client.api_host() == dummy_data.api_host

@responses.activate
def test_setters(client, dummy_data):
    try:
        client.host('host.nexmo.com')
        client.api_host('host.nexmo.com')
        assert client.host() != dummy_data.host
        assert client.api_host() != dummy_data.api_host
    except:
        assert False

@responses.activate
def test_fail_setter_url_format(client, dummy_data):
    try:
        client.host('1000.1000')
        assert False
    except:
        assert True
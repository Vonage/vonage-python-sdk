try:
    from urllib.parse import urlparse, quote_plus
except ImportError:
    from urlparse import urlparse
    from urllib import quote_plus

from util import *

import nexmo


@responses.activate
def test_send_ussd_push_message(client, dummy_data):
    stub(responses.POST, 'https://rest.nexmo.com/ussd/json')

    params = {'from': 'MyCompany20', 'to': '447525856424', 'text': 'Hello'}

    assert isinstance(client.send_ussd_push_message(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'from=MyCompany20' in request_body()
    assert 'to=447525856424' in request_body()
    assert 'text=Hello' in request_body()


@responses.activate
def test_send_ussd_prompt_message(client, dummy_data):
    stub(responses.POST, 'https://rest.nexmo.com/ussd-prompt/json')

    params = {'from': 'long-virtual-number', 'to': '447525856424', 'text': 'Hello'}

    assert isinstance(client.send_ussd_prompt_message(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'from=long-virtual-number' in request_body()
    assert 'to=447525856424' in request_body()
    assert 'text=Hello' in request_body()


@responses.activate
def test_send_2fa_message(client, dummy_data):
    stub(responses.POST, 'https://rest.nexmo.com/sc/us/2fa/json')

    params = {'to': '16365553226', 'pin': '1234'}

    assert isinstance(client.send_2fa_message(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'to=16365553226' in request_body()
    assert 'pin=1234' in request_body()


@responses.activate
def test_send_event_alert_message(client, dummy_data):
    stub(responses.POST, 'https://rest.nexmo.com/sc/us/alert/json')

    params = {'to': '16365553226', 'server': 'host', 'link': 'http://example.com/'}

    assert isinstance(client.send_event_alert_message(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'to=16365553226' in request_body()
    assert 'server=host' in request_body()
    assert 'link=http%3A%2F%2Fexample.com%2F' in request_body()


@responses.activate
def test_send_marketing_message(client, dummy_data):
    stub(responses.POST, 'https://rest.nexmo.com/sc/us/marketing/json')

    params = {'from': 'short-code', 'to': '16365553226', 'keyword': 'NEXMO', 'text': 'Hello'}

    assert isinstance(client.send_marketing_message(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'from=short-code' in request_body()
    assert 'to=16365553226' in request_body()
    assert 'keyword=NEXMO' in request_body()
    assert 'text=Hello' in request_body()


@responses.activate
def test_get_event_alert_numbers(client, dummy_data):
    stub(responses.GET, 'https://rest.nexmo.com/sc/us/alert/opt-in/query/json')

    assert isinstance(client.get_event_alert_numbers(), dict)
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_resubscribe_event_alert_number(client, dummy_data):
    stub(responses.POST, 'https://rest.nexmo.com/sc/us/alert/opt-in/manage/json')

    params = {'msisdn': '441632960960'}

    assert isinstance(client.resubscribe_event_alert_number(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'msisdn=441632960960' in request_body()


def test_check_signature(dummy_data):
    params = {'a': '1', 'b': '2', 'timestamp': '1461605396', 'sig': '6af838ef94998832dbfc29020b564830'}

    client = nexmo.Client(key=dummy_data.api_key, secret=dummy_data.api_secret, signature_secret='secret')

    assert client.check_signature(params)


def test_signature(client, dummy_data):
    params = {'a': '1', 'b': '2', 'timestamp': '1461605396'}
    client = nexmo.Client(key=dummy_data.api_key, secret=dummy_data.api_secret, signature_secret='secret')
    assert client.signature(params) == '6af838ef94998832dbfc29020b564830'


def test_client_doesnt_require_api_key():
    client = nexmo.Client(application_id='myid', private_key='abc\nde')
    assert client is not None
    assert client.api_key is None
    assert client.api_secret is None


@responses.activate
def test_client_can_make_application_requests_without_api_key(dummy_data):
    stub(responses.POST, 'https://api.nexmo.com/v1/calls')

    client = nexmo.Client(application_id='myid', private_key=dummy_data.private_key)
    client.create_call("123455")

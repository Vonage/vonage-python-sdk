import re
import pytest
import responses

import jwt
import platform
import time
try:
    from urllib.parse import urlparse, quote_plus
except ImportError:
    from urlparse import urlparse
    from urllib import quote_plus

import nexmo


def request_body():
    return responses.calls[0].request.body


def request_query():
    return urlparse(responses.calls[0].request.url).query


def request_user_agent():
    return responses.calls[0].request.headers['User-Agent']


def request_authorization():
    return responses.calls[0].request.headers['Authorization'].decode('utf-8')


def request_content_type():
    return responses.calls[0].request.headers['Content-Type']


def stub(method, url):
    responses.add(method, url, body='{"key":"value"}', status=200, content_type='application/json')


def assert_re(pattern, string):
    __tracebackhide__ = True
    if not re.search(pattern, string):
        pytest.fail("Cannot find pattern %r in %r" % (pattern, string))


@responses.activate
def test_send_message(client, dummy_data):
    stub(responses.POST, 'https://rest.nexmo.com/sms/json')

    params = {'from': 'Python', 'to': '447525856424', 'text': 'Hey!'}

    assert isinstance(client.send_message(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'from=Python' in request_body()
    assert 'to=447525856424' in request_body()
    assert 'text=Hey%21' in request_body()


@responses.activate
def test_get_balance(client, dummy_data):
    stub(responses.GET, 'https://rest.nexmo.com/account/get-balance')

    assert isinstance(client.get_balance(), dict)
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_get_country_pricing(client, dummy_data):
    stub(responses.GET, 'https://rest.nexmo.com/account/get-pricing/outbound')

    assert isinstance(client.get_country_pricing('GB'), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'country=GB' in request_query()


@responses.activate
def test_get_prefix_pricing(client, dummy_data):
    stub(responses.GET, 'https://rest.nexmo.com/account/get-prefix-pricing/outbound')

    assert isinstance(client.get_prefix_pricing(44), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'prefix=44' in request_query()


@responses.activate
def test_get_sms_pricing(client, dummy_data):
    stub(responses.GET, 'https://rest.nexmo.com/account/get-phone-pricing/outbound/sms')

    assert isinstance(client.get_sms_pricing('447525856424'), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'phone=447525856424' in request_query()


@responses.activate
def test_get_voice_pricing(client, dummy_data):
    stub(responses.GET, 'https://rest.nexmo.com/account/get-phone-pricing/outbound/voice')

    assert isinstance(client.get_voice_pricing('447525856424'), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'phone=447525856424' in request_query()


@responses.activate
def test_update_settings(client, dummy_data):
    stub(responses.POST, 'https://rest.nexmo.com/account/settings')

    params = {'moCallBackUrl': 'http://example.com/callback'}

    assert isinstance(client.update_settings(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'moCallBackUrl=http%3A%2F%2Fexample.com%2Fcallback' in request_body()


@responses.activate
def test_topup(client, dummy_data):
    stub(responses.POST, 'https://rest.nexmo.com/account/top-up')

    params = {'trx': '00X123456Y7890123Z'}

    assert isinstance(client.topup(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'trx=00X123456Y7890123Z' in request_body()


@responses.activate
def test_get_account_numbers(client, dummy_data):
    stub(responses.GET, 'https://rest.nexmo.com/account/numbers')

    assert isinstance(client.get_account_numbers(size=25), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'size=25' in request_query()


@responses.activate
def test_get_available_numbers(client, dummy_data):
    stub(responses.GET, 'https://rest.nexmo.com/number/search')

    assert isinstance(client.get_available_numbers('CA', size=25), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'country=CA' in request_query()
    assert 'size=25' in request_query()


@responses.activate
def test_buy_number(client, dummy_data):
    stub(responses.POST, 'https://rest.nexmo.com/number/buy')

    params = {'country': 'US', 'msisdn': 'number'}

    assert isinstance(client.buy_number(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'country=US' in request_body()
    assert 'msisdn=number' in request_body()


@responses.activate
def test_cancel_number(client, dummy_data):
    stub(responses.POST, 'https://rest.nexmo.com/number/cancel')

    params = {'country': 'US', 'msisdn': 'number'}

    assert isinstance(client.cancel_number(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'country=US' in request_body()
    assert 'msisdn=number' in request_body()


@responses.activate
def test_update_number(client, dummy_data):
    stub(responses.POST, 'https://rest.nexmo.com/number/update')

    params = {'country': 'US', 'msisdn': 'number', 'moHttpUrl': 'callback'}

    assert isinstance(client.update_number(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'country=US' in request_body()
    assert 'msisdn=number' in request_body()
    assert 'moHttpUrl=callback' in request_body()


@responses.activate
def test_get_message(client, dummy_data):
    stub(responses.GET, 'https://rest.nexmo.com/search/message')

    assert isinstance(client.get_message('00A0B0C0'), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'id=00A0B0C0' in request_query()


@responses.activate
def test_get_message_rejections(client, dummy_data):
    stub(responses.GET, 'https://rest.nexmo.com/search/rejections')

    assert isinstance(client.get_message_rejections(date='YYYY-MM-DD'), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'date=YYYY-MM-DD' in request_query()


@responses.activate
def test_search_messages(client, dummy_data):
    stub(responses.GET, 'https://rest.nexmo.com/search/messages')

    assert isinstance(client.search_messages(to='1234567890', date='YYYY-MM-DD'), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'date=YYYY-MM-DD' in request_query()
    assert 'to=1234567890' in request_query()


@responses.activate
def test_search_messages_by_ids(client, dummy_data):
    stub(responses.GET, 'https://rest.nexmo.com/search/messages')

    assert isinstance(client.search_messages(ids=['00A0B0C0', '00A0B0C1', '00A0B0C2']), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'ids=00A0B0C0' in request_query()
    assert 'ids=00A0B0C1' in request_query()
    assert 'ids=00A0B0C2' in request_query()


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


@responses.activate
def test_initiate_call(client, dummy_data):
    stub(responses.POST, 'https://rest.nexmo.com/call/json')

    params = {'to': '16365553226', 'answer_url': 'http://example.com/answer'}

    assert isinstance(client.initiate_call(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'to=16365553226' in request_body()
    assert 'answer_url=http%3A%2F%2Fexample.com%2Fanswer' in request_body()


@responses.activate
def test_initiate_tts_call(client, dummy_data):
    stub(responses.POST, 'https://api.nexmo.com/tts/json')

    params = {'to': '16365553226', 'text': 'Hello'}

    assert isinstance(client.initiate_tts_call(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'to=16365553226' in request_body()
    assert 'text=Hello' in request_body()


@responses.activate
def test_initiate_tts_prompt_call(client, dummy_data):
    stub(responses.POST, 'https://api.nexmo.com/tts-prompt/json')

    params = {'to': '16365553226', 'text': 'Hello', 'max_digits': 4, 'bye_text': 'Goodbye'}

    assert isinstance(client.initiate_tts_prompt_call(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'to=16365553226' in request_body()
    assert 'text=Hello' in request_body()
    assert 'max_digits=4' in request_body()
    assert 'bye_text=Goodbye' in request_body()


@responses.activate
def test_start_verification(client, dummy_data):
    stub(responses.POST, 'https://api.nexmo.com/verify/json')

    params = {'number': '447525856424', 'brand': 'MyApp'}

    assert isinstance(client.start_verification(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'number=447525856424' in request_body()
    assert 'brand=MyApp' in request_body()


@responses.activate
def test_send_verification_request(client, dummy_data):
    stub(responses.POST, 'https://api.nexmo.com/verify/json')

    params = {'number': '447525856424', 'brand': 'MyApp'}

    assert isinstance(client.send_verification_request(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'number=447525856424' in request_body()
    assert 'brand=MyApp' in request_body()


@responses.activate
def test_check_verification(client, dummy_data):
    stub(responses.POST, 'https://api.nexmo.com/verify/check/json')

    assert isinstance(client.check_verification('8g88g88eg8g8gg9g90', code='123445'), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'code=123445' in request_body()
    assert 'request_id=8g88g88eg8g8gg9g90' in request_body()


@responses.activate
def test_check_verification_request(client, dummy_data):
    stub(responses.POST, 'https://api.nexmo.com/verify/check/json')

    params = {'code': '123445', 'request_id': '8g88g88eg8g8gg9g90'}

    assert isinstance(client.check_verification_request(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'code=123445' in request_body()
    assert 'request_id=8g88g88eg8g8gg9g90' in request_body()


@responses.activate
def test_get_verification(client, dummy_data):
    stub(responses.GET, 'https://api.nexmo.com/verify/search/json')

    assert isinstance(client.get_verification('xxx'), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'request_id=xxx' in request_query()


@responses.activate
def test_get_verification_request(client, dummy_data):
    stub(responses.GET, 'https://api.nexmo.com/verify/search/json')

    assert isinstance(client.get_verification_request('xxx'), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'request_id=xxx' in request_query()


@responses.activate
def test_cancel_verification(client, dummy_data):
    stub(responses.POST, 'https://api.nexmo.com/verify/control/json')

    assert isinstance(client.cancel_verification('8g88g88eg8g8gg9g90'), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'cmd=cancel' in request_body()
    assert 'request_id=8g88g88eg8g8gg9g90' in request_body()


@responses.activate
def test_trigger_next_verification_event(client, dummy_data):
    stub(responses.POST, 'https://api.nexmo.com/verify/control/json')

    assert isinstance(client.trigger_next_verification_event('8g88g88eg8g8gg9g90'), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'cmd=trigger_next_event' in request_body()
    assert 'request_id=8g88g88eg8g8gg9g90' in request_body()


@responses.activate
def test_control_verification_request(client, dummy_data):
    stub(responses.POST, 'https://api.nexmo.com/verify/control/json')

    params = {'cmd': 'cancel', 'request_id': '8g88g88eg8g8gg9g90'}

    assert isinstance(client.control_verification_request(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'cmd=cancel' in request_body()
    assert 'request_id=8g88g88eg8g8gg9g90' in request_body()


@responses.activate
def test_get_basic_number_insight(client, dummy_data):
    stub(responses.GET, 'https://api.nexmo.com/ni/basic/json')

    assert isinstance(client.get_basic_number_insight(number='447525856424'), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'number=447525856424' in request_query()


@responses.activate
def test_get_standard_number_insight(client, dummy_data):
    stub(responses.GET, 'https://api.nexmo.com/ni/standard/json')

    assert isinstance(client.get_standard_number_insight(number='447525856424'), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'number=447525856424' in request_query()


@responses.activate
def test_get_number_insight(client, dummy_data):
    stub(responses.GET, 'https://api.nexmo.com/number/lookup/json')

    assert isinstance(client.get_number_insight(number='447525856424'), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'number=447525856424' in request_query()


@responses.activate
def test_get_advanced_number_insight(client, dummy_data):
    stub(responses.GET, 'https://api.nexmo.com/ni/advanced/json')

    assert isinstance(client.get_advanced_number_insight(number='447525856424'), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'number=447525856424' in request_query()


@responses.activate
def test_request_number_insight(client, dummy_data):
    stub(responses.POST, 'https://rest.nexmo.com/ni/json')

    params = {'number': '447525856424', 'callback': 'https://example.com'}

    assert isinstance(client.request_number_insight(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'number=447525856424' in request_body()
    assert 'callback=https%3A%2F%2Fexample.com' in request_body()


@responses.activate
def test_get_applications(client, dummy_data):
    stub(responses.GET, 'https://api.nexmo.com/v1/applications')

    assert isinstance(client.get_applications(), dict)
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_get_application(client, dummy_data):
    stub(responses.GET, 'https://api.nexmo.com/v1/applications/xx-xx-xx-xx')

    assert isinstance(client.get_application('xx-xx-xx-xx'), dict)
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_create_application(client, dummy_data):
    stub(responses.POST, 'https://api.nexmo.com/v1/applications')

    params = {'name': 'Example App', 'type': 'voice'}

    assert isinstance(client.create_application(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert 'name=Example+App' in request_body()
    assert 'type=voice' in request_body()


@responses.activate
def test_update_application(client, dummy_data):
    stub(responses.PUT, 'https://api.nexmo.com/v1/applications/xx-xx-xx-xx')

    params = {'answer_url': 'https://example.com/ncco'}

    assert isinstance(client.update_application('xx-xx-xx-xx', params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == 'application/json'
    assert b'"answer_url": "https://example.com/ncco"' in request_body()


@responses.activate
def test_delete_application(client, dummy_data):
    responses.add(responses.DELETE, 'https://api.nexmo.com/v1/applications/xx-xx-xx-xx', status=204)

    assert None == client.delete_application('xx-xx-xx-xx')
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_create_call(client, dummy_data):
    stub(responses.POST, 'https://api.nexmo.com/v1/calls')

    params = {
        'to': [{'type': 'phone', 'number': '14843331234'}],
        'from': {'type': 'phone', 'number': '14843335555'},
        'answer_url': ['https://example.com/answer']
    }

    assert isinstance(client.create_call(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == 'application/json'


@responses.activate
def test_get_calls(client, dummy_data):
    stub(responses.GET, 'https://api.nexmo.com/v1/calls')

    assert isinstance(client.get_calls(), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert_re(r'\ABearer ', request_authorization())


@responses.activate
def test_get_call(client, dummy_data):
    stub(responses.GET, 'https://api.nexmo.com/v1/calls/xx-xx-xx-xx')

    assert isinstance(client.get_call('xx-xx-xx-xx'), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert_re(r'\ABearer ', request_authorization())


@responses.activate
def test_update_call(client, dummy_data):
    stub(responses.PUT, 'https://api.nexmo.com/v1/calls/xx-xx-xx-xx')

    assert isinstance(client.update_call('xx-xx-xx-xx', action='hangup'), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == 'application/json'
    assert request_body() == b'{"action": "hangup"}'


@responses.activate
def test_send_audio(client, dummy_data):
    stub(responses.PUT, 'https://api.nexmo.com/v1/calls/xx-xx-xx-xx/stream')

    assert isinstance(client.send_audio('xx-xx-xx-xx', stream_url='http://example.com/audio.mp3'), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == 'application/json'
    assert request_body() == b'{"stream_url": "http://example.com/audio.mp3"}'


@responses.activate
def test_stop_audio(client, dummy_data):
    stub(responses.DELETE, 'https://api.nexmo.com/v1/calls/xx-xx-xx-xx/stream')

    assert isinstance(client.stop_audio('xx-xx-xx-xx'), dict)
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_send_speech(client, dummy_data):
    stub(responses.PUT, 'https://api.nexmo.com/v1/calls/xx-xx-xx-xx/talk')

    assert isinstance(client.send_speech('xx-xx-xx-xx', text='Hello'), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == 'application/json'
    assert request_body() == b'{"text": "Hello"}'


@responses.activate
def test_stop_speech(client, dummy_data):
    stub(responses.DELETE, 'https://api.nexmo.com/v1/calls/xx-xx-xx-xx/talk')

    assert isinstance(client.stop_speech('xx-xx-xx-xx'), dict)
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_send_dtmf(client, dummy_data):
    stub(responses.PUT, 'https://api.nexmo.com/v1/calls/xx-xx-xx-xx/dtmf')

    assert isinstance(client.send_dtmf('xx-xx-xx-xx', digits='1234'), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == 'application/json'
    assert request_body() == b'{"digits": "1234"}'


@responses.activate
def test_user_provided_authorization(client, dummy_data):
    stub(responses.GET, 'https://api.nexmo.com/v1/calls/xx-xx-xx-xx')

    application_id = 'different-nexmo-application-id'
    nbf = int(time.time())
    exp = nbf + 3600

    client.auth(application_id=application_id, nbf=nbf, exp=exp)
    client.get_call('xx-xx-xx-xx')

    token = request_authorization().split()[1]

    token = jwt.decode(token, dummy_data.public_key, algorithm='RS256')

    assert token['application_id'] == application_id
    assert token['nbf'] == nbf
    assert token['exp'] == exp


@responses.activate
def test_authorization_with_private_key_path(dummy_data):
    stub(responses.GET, 'https://api.nexmo.com/v1/calls/xx-xx-xx-xx')

    private_key = 'test/private_key.txt'

    client = nexmo.Client(
        key=dummy_data.api_key,
        secret=dummy_data.api_secret,
        application_id=dummy_data.application_id,
        private_key=private_key,
    )
    client.get_call('xx-xx-xx-xx')

    token = jwt.decode(request_authorization().split()[1], dummy_data.public_key, algorithm='RS256')
    assert token['application_id'] == dummy_data.application_id


@responses.activate
def test_authorization_with_private_key_object(client, dummy_data):
    stub(responses.GET, 'https://api.nexmo.com/v1/calls/xx-xx-xx-xx')

    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization

    private_key = serialization.load_pem_private_key(dummy_data.private_key.encode('utf-8'), password=None,
                                                     backend=default_backend())
    client.get_call('xx-xx-xx-xx')

    token = jwt.decode(request_authorization().split()[1], dummy_data.public_key, algorithm='RS256')
    assert token['application_id'] == dummy_data.application_id


@responses.activate
def test_authentication_error(client):
    responses.add(responses.POST, 'https://rest.nexmo.com/sms/json', status=401)

    with pytest.raises(nexmo.AuthenticationError):
        client.send_message({})


@responses.activate
def test_client_error(client):
    responses.add(responses.POST, 'https://rest.nexmo.com/sms/json', status=400)

    with pytest.raises(nexmo.ClientError) as excinfo:
        client.send_message({})
    excinfo.match(r'400 response from rest.nexmo.com')


@responses.activate
def test_server_error(client):
    responses.add(responses.POST, 'https://rest.nexmo.com/sms/json', status=500)

    with pytest.raises(nexmo.ServerError) as excinfo:
        client.send_message({})
    excinfo.match(r'500 response from rest.nexmo.com')


@responses.activate
def test_application_info_options(dummy_data):
    app_name, app_version = 'ExampleApp', 'X.Y.Z'

    stub(responses.GET, 'https://rest.nexmo.com/account/get-balance')

    client = nexmo.Client(key=dummy_data.api_key, secret=dummy_data.api_secret, app_name=app_name,
                          app_version=app_version)
    user_agent = '/'.join(
        ['nexmo-python', nexmo.__version__, platform.python_version(), app_name, app_version])

    assert isinstance(client.get_balance(), dict)
    assert request_user_agent() == user_agent


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

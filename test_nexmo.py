try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus

import unittest, nexmo, responses, platform, jwt, time


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


def read_file(path):
    with open(path) as input_file:
        return input_file.read()


class NexmoClientTestCase(unittest.TestCase):
    def setUp(self):
        self.api_key = 'nexmo-api-key'
        self.api_secret = 'nexmo-api-secret'
        self.application_id = 'nexmo-application-id'
        self.private_key = read_file('test/private_key.txt')
        self.public_key = read_file('test/public_key.txt')
        self.user_agent = 'nexmo-python/{0}/{1}'.format(nexmo.__version__, platform.python_version())
        self.client = nexmo.Client(key=self.api_key, secret=self.api_secret, application_id=self.application_id,
                                   private_key=self.private_key)

        if not hasattr(self, 'assertRegex'):
            self.assertRegex = self.assertRegexpMatches

        if not hasattr(self, 'assertRaisesRegex'):
            self.assertRaisesRegex = self.assertRaisesRegexp

    def stub(self, method, url):
        responses.add(method, url, body='{"key":"value"}', status=200, content_type='application/json')

    @responses.activate
    def test_send_message(self):
        self.stub(responses.POST, 'https://rest.nexmo.com/sms/json')

        params = {'from': 'Python', 'to': '447525856424', 'text': 'Hey!'}

        self.assertIsInstance(self.client.send_message(params), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('from=Python', request_body())
        self.assertIn('to=447525856424', request_body())
        self.assertIn('text=Hey%21', request_body())

    @responses.activate
    def test_get_balance(self):
        self.stub(responses.GET, 'https://rest.nexmo.com/account/get-balance')

        self.assertIsInstance(self.client.get_balance(), dict)
        self.assertEqual(request_user_agent(), self.user_agent)

    @responses.activate
    def test_get_country_pricing(self):
        self.stub(responses.GET, 'https://rest.nexmo.com/account/get-pricing/outbound')

        self.assertIsInstance(self.client.get_country_pricing('GB'), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('country=GB', request_query())

    @responses.activate
    def test_get_prefix_pricing(self):
        self.stub(responses.GET, 'https://rest.nexmo.com/account/get-prefix-pricing/outbound')

        self.assertIsInstance(self.client.get_prefix_pricing(44), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('prefix=44', request_query())

    @responses.activate
    def test_get_sms_pricing(self):
        self.stub(responses.GET, 'https://rest.nexmo.com/account/get-phone-pricing/outbound/sms')

        self.assertIsInstance(self.client.get_sms_pricing('447525856424'), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('phone=447525856424', request_query())

    @responses.activate
    def test_get_voice_pricing(self):
        self.stub(responses.GET, 'https://rest.nexmo.com/account/get-phone-pricing/outbound/voice')

        self.assertIsInstance(self.client.get_voice_pricing('447525856424'), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('phone=447525856424', request_query())

    @responses.activate
    def test_update_settings(self):
        self.stub(responses.POST, 'https://rest.nexmo.com/account/settings')

        params = {'moCallBackUrl': 'http://example.com/callback'}

        self.assertIsInstance(self.client.update_settings(params), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('moCallBackUrl=http%3A%2F%2Fexample.com%2Fcallback', request_body())

    @responses.activate
    def test_topup(self):
        self.stub(responses.POST, 'https://rest.nexmo.com/account/top-up')

        params = {'trx': '00X123456Y7890123Z'}

        self.assertIsInstance(self.client.topup(params), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('trx=00X123456Y7890123Z', request_body())

    @responses.activate
    def test_get_account_numbers(self):
        self.stub(responses.GET, 'https://rest.nexmo.com/account/numbers')

        self.assertIsInstance(self.client.get_account_numbers(size=25), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('size=25', request_query())

    @responses.activate
    def test_get_available_numbers(self):
        self.stub(responses.GET, 'https://rest.nexmo.com/number/search')

        self.assertIsInstance(self.client.get_available_numbers('CA', size=25), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('country=CA', request_query())
        self.assertIn('size=25', request_query())

    @responses.activate
    def test_buy_number(self):
        self.stub(responses.POST, 'https://rest.nexmo.com/number/buy')

        params = {'country': 'US', 'msisdn': 'number'}

        self.assertIsInstance(self.client.buy_number(params), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('country=US', request_body())
        self.assertIn('msisdn=number', request_body())

    @responses.activate
    def test_cancel_number(self):
        self.stub(responses.POST, 'https://rest.nexmo.com/number/cancel')

        params = {'country': 'US', 'msisdn': 'number'}

        self.assertIsInstance(self.client.cancel_number(params), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('country=US', request_body())
        self.assertIn('msisdn=number', request_body())

    @responses.activate
    def test_update_number(self):
        self.stub(responses.POST, 'https://rest.nexmo.com/number/update')

        params = {'country': 'US', 'msisdn': 'number', 'moHttpUrl': 'callback'}

        self.assertIsInstance(self.client.update_number(params), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('country=US', request_body())
        self.assertIn('msisdn=number', request_body())
        self.assertIn('moHttpUrl=callback', request_body())

    @responses.activate
    def test_get_message(self):
        self.stub(responses.GET, 'https://rest.nexmo.com/search/message')

        self.assertIsInstance(self.client.get_message('00A0B0C0'), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('id=00A0B0C0', request_query())

    @responses.activate
    def test_get_message_rejections(self):
        self.stub(responses.GET, 'https://rest.nexmo.com/search/rejections')

        self.assertIsInstance(self.client.get_message_rejections(date='YYYY-MM-DD'), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('date=YYYY-MM-DD', request_query())

    @responses.activate
    def test_search_messages(self):
        self.stub(responses.GET, 'https://rest.nexmo.com/search/messages')

        self.assertIsInstance(self.client.search_messages(to='1234567890', date='YYYY-MM-DD'), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('date=YYYY-MM-DD', request_query())
        self.assertIn('to=1234567890', request_query())

    @responses.activate
    def test_search_messages_by_ids(self):
        self.stub(responses.GET, 'https://rest.nexmo.com/search/messages')

        self.assertIsInstance(self.client.search_messages(ids=['00A0B0C0', '00A0B0C1', '00A0B0C2']), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('ids=00A0B0C0', request_query())
        self.assertIn('ids=00A0B0C1', request_query())
        self.assertIn('ids=00A0B0C2', request_query())

    @responses.activate
    def test_send_ussd_push_message(self):
        self.stub(responses.POST, 'https://rest.nexmo.com/ussd/json')

        params = {'from': 'MyCompany20', 'to': '447525856424', 'text': 'Hello'}

        self.assertIsInstance(self.client.send_ussd_push_message(params), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('from=MyCompany20', request_body())
        self.assertIn('to=447525856424', request_body())
        self.assertIn('text=Hello', request_body())

    @responses.activate
    def test_send_ussd_prompt_message(self):
        self.stub(responses.POST, 'https://rest.nexmo.com/ussd-prompt/json')

        params = {'from': 'long-virtual-number', 'to': '447525856424', 'text': 'Hello'}

        self.assertIsInstance(self.client.send_ussd_prompt_message(params), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('from=long-virtual-number', request_body())
        self.assertIn('to=447525856424', request_body())
        self.assertIn('text=Hello', request_body())

    @responses.activate
    def test_send_2fa_message(self):
        self.stub(responses.POST, 'https://rest.nexmo.com/sc/us/2fa/json')

        params = {'to': '16365553226', 'pin': '1234'}

        self.assertIsInstance(self.client.send_2fa_message(params), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('to=16365553226', request_body())
        self.assertIn('pin=1234', request_body())

    @responses.activate
    def test_send_event_alert_message(self):
        self.stub(responses.POST, 'https://rest.nexmo.com/sc/us/alert/json')

        params = {'to': '16365553226', 'server': 'host', 'link': 'http://example.com/'}

        self.assertIsInstance(self.client.send_event_alert_message(params), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('to=16365553226', request_body())
        self.assertIn('server=host', request_body())
        self.assertIn('link=http%3A%2F%2Fexample.com%2F', request_body())

    @responses.activate
    def test_send_marketing_message(self):
        self.stub(responses.POST, 'https://rest.nexmo.com/sc/us/marketing/json')

        params = {'from': 'short-code', 'to': '16365553226', 'keyword': 'NEXMO', 'text': 'Hello'}

        self.assertIsInstance(self.client.send_marketing_message(params), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('from=short-code', request_body())
        self.assertIn('to=16365553226', request_body())
        self.assertIn('keyword=NEXMO', request_body())
        self.assertIn('text=Hello', request_body())

    @responses.activate
    def test_get_event_alert_numbers(self):
        self.stub(responses.GET, 'https://rest.nexmo.com/sc/us/alert/opt-in/query/json')

        self.assertIsInstance(self.client.get_event_alert_numbers(), dict)
        self.assertEqual(request_user_agent(), self.user_agent)

    @responses.activate
    def test_resubscribe_event_alert_number(self):
        self.stub(responses.POST, 'https://rest.nexmo.com/sc/us/alert/opt-in/manage/json')

        params = {'msisdn': '441632960960'}

        self.assertIsInstance(self.client.resubscribe_event_alert_number(params), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('msisdn=441632960960', request_body())

    @responses.activate
    def test_initiate_call(self):
        self.stub(responses.POST, 'https://rest.nexmo.com/call/json')

        params = {'to': '16365553226', 'answer_url': 'http://example.com/answer'}

        self.assertIsInstance(self.client.initiate_call(params), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('to=16365553226', request_body())
        self.assertIn('answer_url=http%3A%2F%2Fexample.com%2Fanswer', request_body())

    @responses.activate
    def test_initiate_tts_call(self):
        self.stub(responses.POST, 'https://api.nexmo.com/tts/json')

        params = {'to': '16365553226', 'text': 'Hello'}

        self.assertIsInstance(self.client.initiate_tts_call(params), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('to=16365553226', request_body())
        self.assertIn('text=Hello', request_body())

    @responses.activate
    def test_initiate_tts_prompt_call(self):
        self.stub(responses.POST, 'https://api.nexmo.com/tts-prompt/json')

        params = {'to': '16365553226', 'text': 'Hello', 'max_digits': 4, 'bye_text': 'Goodbye'}

        self.assertIsInstance(self.client.initiate_tts_prompt_call(params), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('to=16365553226', request_body())
        self.assertIn('text=Hello', request_body())
        self.assertIn('max_digits=4', request_body())
        self.assertIn('bye_text=Goodbye', request_body())

    @responses.activate
    def test_start_verification(self):
        self.stub(responses.POST, 'https://api.nexmo.com/verify/json')

        params = {'number': '447525856424', 'brand': 'MyApp'}

        self.assertIsInstance(self.client.start_verification(params), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('number=447525856424', request_body())
        self.assertIn('brand=MyApp', request_body())

    @responses.activate
    def test_send_verification_request(self):
        self.stub(responses.POST, 'https://api.nexmo.com/verify/json')

        params = {'number': '447525856424', 'brand': 'MyApp'}

        self.assertIsInstance(self.client.send_verification_request(params), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('number=447525856424', request_body())
        self.assertIn('brand=MyApp', request_body())

    @responses.activate
    def test_check_verification(self):
        self.stub(responses.POST, 'https://api.nexmo.com/verify/check/json')

        self.assertIsInstance(self.client.check_verification('8g88g88eg8g8gg9g90', code='123445'), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('code=123445', request_body())
        self.assertIn('request_id=8g88g88eg8g8gg9g90', request_body())

    @responses.activate
    def test_check_verification_request(self):
        self.stub(responses.POST, 'https://api.nexmo.com/verify/check/json')

        params = {'code': '123445', 'request_id': '8g88g88eg8g8gg9g90'}

        self.assertIsInstance(self.client.check_verification_request(params), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('code=123445', request_body())
        self.assertIn('request_id=8g88g88eg8g8gg9g90', request_body())

    @responses.activate
    def test_get_verification(self):
        self.stub(responses.GET, 'https://api.nexmo.com/verify/search/json')

        self.assertIsInstance(self.client.get_verification('xxx'), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('request_id=xxx', request_query())

    @responses.activate
    def test_get_verification_request(self):
        self.stub(responses.GET, 'https://api.nexmo.com/verify/search/json')

        self.assertIsInstance(self.client.get_verification_request('xxx'), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('request_id=xxx', request_query())

    @responses.activate
    def test_cancel_verification(self):
        self.stub(responses.POST, 'https://api.nexmo.com/verify/control/json')

        self.assertIsInstance(self.client.cancel_verification('8g88g88eg8g8gg9g90'), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('cmd=cancel', request_body())
        self.assertIn('request_id=8g88g88eg8g8gg9g90', request_body())

    @responses.activate
    def test_trigger_next_verification_event(self):
        self.stub(responses.POST, 'https://api.nexmo.com/verify/control/json')

        self.assertIsInstance(self.client.trigger_next_verification_event('8g88g88eg8g8gg9g90'), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('cmd=trigger_next_event', request_body())
        self.assertIn('request_id=8g88g88eg8g8gg9g90', request_body())

    @responses.activate
    def test_control_verification_request(self):
        self.stub(responses.POST, 'https://api.nexmo.com/verify/control/json')

        params = {'cmd': 'cancel', 'request_id': '8g88g88eg8g8gg9g90'}

        self.assertIsInstance(self.client.control_verification_request(params), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('cmd=cancel', request_body())
        self.assertIn('request_id=8g88g88eg8g8gg9g90', request_body())

    @responses.activate
    def test_get_basic_number_insight(self):
        self.stub(responses.GET, 'https://api.nexmo.com/ni/basic/json')

        self.assertIsInstance(self.client.get_basic_number_insight(number='447525856424'), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('number=447525856424', request_query())

    @responses.activate
    def test_get_standard_number_insight(self):
        self.stub(responses.GET, 'https://api.nexmo.com/ni/standard/json')

        self.assertIsInstance(self.client.get_standard_number_insight(number='447525856424'), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('number=447525856424', request_query())

    @responses.activate
    def test_get_number_insight(self):
        self.stub(responses.GET, 'https://api.nexmo.com/number/lookup/json')

        self.assertIsInstance(self.client.get_number_insight(number='447525856424'), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('number=447525856424', request_query())

    @responses.activate
    def test_get_advanced_number_insight(self):
        self.stub(responses.GET, 'https://api.nexmo.com/ni/advanced/json')

        self.assertIsInstance(self.client.get_advanced_number_insight(number='447525856424'), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('number=447525856424', request_query())

    @responses.activate
    def test_request_number_insight(self):
        self.stub(responses.POST, 'https://rest.nexmo.com/ni/json')

        params = {'number': '447525856424', 'callback': 'https://example.com'}

        self.assertIsInstance(self.client.request_number_insight(params), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('number=447525856424', request_body())
        self.assertIn('callback=https%3A%2F%2Fexample.com', request_body())

    @responses.activate
    def test_get_applications(self):
        self.stub(responses.GET, 'https://api.nexmo.com/v1/applications')

        self.assertIsInstance(self.client.get_applications(), dict)
        self.assertEqual(request_user_agent(), self.user_agent)

    @responses.activate
    def test_get_application(self):
        self.stub(responses.GET, 'https://api.nexmo.com/v1/applications/xx-xx-xx-xx')

        self.assertIsInstance(self.client.get_application('xx-xx-xx-xx'), dict)
        self.assertEqual(request_user_agent(), self.user_agent)

    @responses.activate
    def test_create_application(self):
        self.stub(responses.POST, 'https://api.nexmo.com/v1/applications')

        params = {'name': 'Example App', 'type': 'voice'}

        self.assertIsInstance(self.client.create_application(params), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertIn('name=Example+App', request_body())
        self.assertIn('type=voice', request_body())

    @responses.activate
    def test_update_application(self):
        self.stub(responses.PUT, 'https://api.nexmo.com/v1/applications/xx-xx-xx-xx')

        params = {'answer_url': 'https://example.com/ncco'}

        self.assertIsInstance(self.client.update_application('xx-xx-xx-xx', params), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertEqual(request_content_type(), 'application/json')
        self.assertIn(b'"answer_url": "https://example.com/ncco"', request_body())

    @responses.activate
    def test_delete_application(self):
        responses.add(responses.DELETE, 'https://api.nexmo.com/v1/applications/xx-xx-xx-xx', status=204)

        self.assertEqual(None, self.client.delete_application('xx-xx-xx-xx'))
        self.assertEqual(request_user_agent(), self.user_agent)

    @responses.activate
    def test_create_call(self):
        self.stub(responses.POST, 'https://api.nexmo.com/v1/calls')

        params = {
            'to': [{'type': 'phone', 'number': '14843331234'}],
            'from': {'type': 'phone', 'number': '14843335555'},
            'answer_url': ['https://example.com/answer']
        }

        self.assertIsInstance(self.client.create_call(params), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertEqual(request_content_type(), 'application/json')

    @responses.activate
    def test_get_calls(self):
        self.stub(responses.GET, 'https://api.nexmo.com/v1/calls')

        self.assertIsInstance(self.client.get_calls(), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertRegex(request_authorization(), r'\ABearer ')

    @responses.activate
    def test_get_call(self):
        self.stub(responses.GET, 'https://api.nexmo.com/v1/calls/xx-xx-xx-xx')

        self.assertIsInstance(self.client.get_call('xx-xx-xx-xx'), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertRegex(request_authorization(), r'\ABearer ')

    @responses.activate
    def test_update_call(self):
        self.stub(responses.PUT, 'https://api.nexmo.com/v1/calls/xx-xx-xx-xx')

        self.assertIsInstance(self.client.update_call('xx-xx-xx-xx', action='hangup'), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertEqual(request_content_type(), 'application/json')
        self.assertEqual(request_body(), b'{"action": "hangup"}')

    @responses.activate
    def test_send_audio(self):
        self.stub(responses.PUT, 'https://api.nexmo.com/v1/calls/xx-xx-xx-xx/stream')

        self.assertIsInstance(self.client.send_audio('xx-xx-xx-xx', stream_url='http://example.com/audio.mp3'), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertEqual(request_content_type(), 'application/json')
        self.assertEqual(request_body(), b'{"stream_url": "http://example.com/audio.mp3"}')

    @responses.activate
    def test_stop_audio(self):
        self.stub(responses.DELETE, 'https://api.nexmo.com/v1/calls/xx-xx-xx-xx/stream')

        self.assertIsInstance(self.client.stop_audio('xx-xx-xx-xx'), dict)
        self.assertEqual(request_user_agent(), self.user_agent)

    @responses.activate
    def test_send_speech(self):
        self.stub(responses.PUT, 'https://api.nexmo.com/v1/calls/xx-xx-xx-xx/talk')

        self.assertIsInstance(self.client.send_speech('xx-xx-xx-xx', text='Hello'), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertEqual(request_content_type(), 'application/json')
        self.assertEqual(request_body(), b'{"text": "Hello"}')

    @responses.activate
    def test_stop_speech(self):
        self.stub(responses.DELETE, 'https://api.nexmo.com/v1/calls/xx-xx-xx-xx/talk')

        self.assertIsInstance(self.client.stop_speech('xx-xx-xx-xx'), dict)
        self.assertEqual(request_user_agent(), self.user_agent)

    @responses.activate
    def test_send_dtmf(self):
        self.stub(responses.PUT, 'https://api.nexmo.com/v1/calls/xx-xx-xx-xx/dtmf')

        self.assertIsInstance(self.client.send_dtmf('xx-xx-xx-xx', digits='1234'), dict)
        self.assertEqual(request_user_agent(), self.user_agent)
        self.assertEqual(request_content_type(), 'application/json')
        self.assertEqual(request_body(), b'{"digits": "1234"}')

    @responses.activate
    def test_user_provided_authorization(self):
        self.stub(responses.GET, 'https://api.nexmo.com/v1/calls/xx-xx-xx-xx')

        application_id = 'different-nexmo-application-id'
        nbf = int(time.time())
        exp = nbf + 3600

        self.client.auth(application_id=application_id, nbf=nbf, exp=exp)
        self.client.get_call('xx-xx-xx-xx')

        token = request_authorization().split()[1]

        token = jwt.decode(token, self.public_key, algorithm='RS256')

        self.assertEqual(token['application_id'], application_id)
        self.assertEqual(token['nbf'], nbf)
        self.assertEqual(token['exp'], exp)

    @responses.activate
    def test_authorization_with_private_key_path(self):
        self.stub(responses.GET, 'https://api.nexmo.com/v1/calls/xx-xx-xx-xx')

        private_key = 'test/private_key.txt'

        self.client = nexmo.Client(key=self.api_key, secret=self.api_secret, application_id=self.application_id,
                                   private_key=private_key)
        self.client.get_call('xx-xx-xx-xx')

        token = request_authorization().split()[1]

        token = jwt.decode(token, self.public_key, algorithm='RS256')

        self.assertEqual(token['application_id'], self.application_id)

    @responses.activate
    def test_authorization_with_private_key_object(self):
        self.stub(responses.GET, 'https://api.nexmo.com/v1/calls/xx-xx-xx-xx')

        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import serialization

        private_key = serialization.load_pem_private_key(self.private_key.encode('utf-8'), password=None,
                                                         backend=default_backend())

        self.client = nexmo.Client(key=self.api_key, secret=self.api_secret, application_id=self.application_id,
                                   private_key=private_key)
        self.client.get_call('xx-xx-xx-xx')

        token = request_authorization().split()[1]

        token = jwt.decode(token, self.public_key, algorithm='RS256')

        self.assertEqual(token['application_id'], self.application_id)

    @responses.activate
    def test_authentication_error(self):
        responses.add(responses.POST, 'https://rest.nexmo.com/sms/json', status=401)

        self.assertRaises(nexmo.AuthenticationError, self.client.send_message, {})

    @responses.activate
    def test_client_error(self):
        responses.add(responses.POST, 'https://rest.nexmo.com/sms/json', status=400)

        message = '400 response from rest.nexmo.com'

        self.assertRaisesRegex(nexmo.ClientError, message, self.client.send_message, {})

    @responses.activate
    def test_server_error(self):
        responses.add(responses.POST, 'https://rest.nexmo.com/sms/json', status=500)

        message = '500 response from rest.nexmo.com'

        self.assertRaisesRegex(nexmo.ServerError, message, self.client.send_message, {})

    @responses.activate
    def test_application_info_options(self):
        app_name, app_version = 'ExampleApp', 'X.Y.Z'

        self.stub(responses.GET, 'https://rest.nexmo.com/account/get-balance')

        self.client = nexmo.Client(key=self.api_key, secret=self.api_secret, app_name=app_name, app_version=app_version)
        self.user_agent = '/'.join(
            ['nexmo-python', nexmo.__version__, platform.python_version(), app_name, app_version])

        self.assertIsInstance(self.client.get_balance(), dict)
        self.assertEqual(request_user_agent(), self.user_agent)

    def test_check_signature(self):
        params = {'a': '1', 'b': '2', 'timestamp': '1461605396', 'sig': '6af838ef94998832dbfc29020b564830'}

        self.client = nexmo.Client(key=self.api_key, secret=self.api_secret, signature_secret='secret')

        self.assertTrue(self.client.check_signature(params))

    def test_signature(self):
        params = {'a': '1', 'b': '2', 'timestamp': '1461605396'}

        self.client = nexmo.Client(key=self.api_key, secret=self.api_secret, signature_secret='secret')

        self.assertEqual(self.client.signature(params), '6af838ef94998832dbfc29020b564830')

    def test_client_doesnt_require_api_key(self):
        client = nexmo.Client(application_id='myid', private_key='abc\nde')
        self.assertIsNotNone(client)
        self.assertIsNone(client.api_key)
        self.assertIsNone(client.api_secret)

    @responses.activate
    def test_client_can_make_application_requests_without_api_key(self):
        self.stub(responses.POST, 'https://api.nexmo.com/v1/calls')

        client = nexmo.Client(application_id='myid', private_key=self.private_key)
        client.create_call("123455")


if __name__ == '__main__':
    unittest.main()

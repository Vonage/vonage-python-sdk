try:
  from urllib.parse import urlparse
except ImportError:
  from urlparse import urlparse

try:
  from urllib.parse import quote_plus
except ImportError:
  from urllib import quote_plus

import unittest, nexmo, responses, platform


class NexmoClientTestCase(unittest.TestCase):
  def setUp(self):
    self.api_key = 'nexmo-api-key'
    self.api_secret = 'nexmo-api-secret'
    self.user_agent = 'nexmo-python/{0}/{1}'.format(nexmo.__version__, platform.python_version())
    self.client = nexmo.Client(key=self.api_key, secret=self.api_secret)

    if not hasattr(self, 'assertRaisesRegex'):
      self.assertRaisesRegex = self.assertRaisesRegexp

  def stub(self, method, url):
    responses.add(method, url, body='{"key":"value"}', status=200, content_type='application/json')

  def assertOK(self, response):
    self.assertEqual(self.user_agent, responses.calls[0].request.headers['User-Agent'])
    self.assertIsInstance(response, dict)

  def assertRequestQueryIncludes(self, param):
    self.assertIn(param, urlparse(responses.calls[0].request.url).query)

  def assertRequestBodyIncludes(self, params):
    body = responses.calls[0].request.body

    for k in params:
      param = quote_plus(str(k)) + '=' + quote_plus(str(params[k]))

      self.assertIn(param, body)

  @responses.activate
  def test_send_message(self):
    self.stub(responses.POST, 'https://rest.nexmo.com/sms/json')

    params = {'from': 'ruby', 'to': '447525856424', 'text': 'Hey!'}

    self.assertOK(self.client.send_message(params))
    self.assertRequestBodyIncludes(params)

  @responses.activate
  def test_get_balance(self):
    self.stub(responses.GET, 'https://rest.nexmo.com/account/get-balance')

    self.assertOK(self.client.get_balance())

  @responses.activate
  def test_get_country_pricing(self):
    self.stub(responses.GET, 'https://rest.nexmo.com/account/get-pricing/outbound')

    self.assertOK(self.client.get_country_pricing('GB'))
    self.assertRequestQueryIncludes('country=GB')

  @responses.activate
  def test_get_prefix_pricing(self):
    self.stub(responses.GET, 'https://rest.nexmo.com/account/get-prefix-pricing/outbound')

    self.assertOK(self.client.get_prefix_pricing(44))
    self.assertRequestQueryIncludes('prefix=44')

  @responses.activate
  def test_update_settings(self):
    self.stub(responses.POST, 'https://rest.nexmo.com/account/settings')

    params = {'moCallBackUrl': 'http://example.com/callback'}

    self.assertOK(self.client.update_settings(params))
    self.assertRequestBodyIncludes(params)

  @responses.activate
  def test_topup(self):
    self.stub(responses.POST, 'https://rest.nexmo.com/account/top-up')

    params = {'trx': '00X123456Y7890123Z'}

    self.assertOK(self.client.topup(params))
    self.assertRequestBodyIncludes(params)

  @responses.activate
  def test_get_account_numbers(self):
    self.stub(responses.GET, 'https://rest.nexmo.com/account/numbers')

    self.assertOK(self.client.get_account_numbers(size=25))
    self.assertRequestQueryIncludes('size=25')

  @responses.activate
  def test_get_available_numbers(self):
    self.stub(responses.GET, 'https://rest.nexmo.com/number/search')

    self.assertOK(self.client.get_available_numbers('CA', size=25))
    self.assertRequestQueryIncludes('country=CA')
    self.assertRequestQueryIncludes('size=25')

  @responses.activate
  def test_buy_number(self):
    self.stub(responses.POST, 'https://rest.nexmo.com/number/buy')

    params = {'country': 'US', 'msisdn': 'number'}

    self.assertOK(self.client.buy_number(params))
    self.assertRequestBodyIncludes(params)

  @responses.activate
  def test_cancel_number(self):
    self.stub(responses.POST, 'https://rest.nexmo.com/number/cancel')

    params = {'country': 'US', 'msisdn': 'number'}

    self.assertOK(self.client.cancel_number(params))
    self.assertRequestBodyIncludes(params)

  @responses.activate
  def test_update_number(self):
    self.stub(responses.POST, 'https://rest.nexmo.com/number/update')

    params = {'country': 'US', 'msisdn': 'number', 'moHttpUrl': 'callback'}

    self.assertOK(self.client.update_number(params))
    self.assertRequestBodyIncludes(params)

  @responses.activate
  def test_get_message(self):
    self.stub(responses.GET, 'https://rest.nexmo.com/search/message')

    self.assertOK(self.client.get_message('00A0B0C0'))
    self.assertRequestQueryIncludes('id=00A0B0C0')

  @responses.activate
  def test_get_message_rejections(self):
    self.stub(responses.GET, 'https://rest.nexmo.com/search/rejections')

    self.assertOK(self.client.get_message_rejections(date='YYYY-MM-DD'))
    self.assertRequestQueryIncludes('date=YYYY-MM-DD')

  @responses.activate
  def test_search_messages(self):
    self.stub(responses.GET, 'https://rest.nexmo.com/search/messages')

    self.assertOK(self.client.search_messages(to='1234567890', date='YYYY-MM-DD'))
    self.assertRequestQueryIncludes('date=YYYY-MM-DD')
    self.assertRequestQueryIncludes('to=1234567890')

  @responses.activate
  def test_search_messages_by_ids(self):
    self.stub(responses.GET, 'https://rest.nexmo.com/search/messages')

    self.assertOK(self.client.search_messages(ids=['00A0B0C0', '00A0B0C1', '00A0B0C2']))
    self.assertRequestQueryIncludes('ids=00A0B0C0')
    self.assertRequestQueryIncludes('ids=00A0B0C1')
    self.assertRequestQueryIncludes('ids=00A0B0C2')

  @responses.activate
  def test_send_ussd_push_message(self):
    self.stub(responses.POST, 'https://rest.nexmo.com/ussd/json')

    params = {'from': 'MyCompany20', 'to': '447525856424', 'text': 'Hello'}

    self.assertOK(self.client.send_ussd_push_message(params))
    self.assertRequestBodyIncludes(params)

  @responses.activate
  def test_send_ussd_prompt_message(self):
    self.stub(responses.POST, 'https://rest.nexmo.com/ussd-prompt/json')

    params = {'from': 'long-virtual-number', 'to': '447525856424', 'text': 'Hello'}

    self.assertOK(self.client.send_ussd_prompt_message(params))
    self.assertRequestBodyIncludes(params)

  @responses.activate
  def test_send_2fa_message(self):
    self.stub(responses.POST, 'https://rest.nexmo.com/sc/us/2fa/json')

    params = {'to': '16365553226', 'pin': '1234'}

    self.assertOK(self.client.send_2fa_message(params))
    self.assertRequestBodyIncludes(params)

  @responses.activate
  def test_send_event_alert_message(self):
    self.stub(responses.POST, 'https://rest.nexmo.com/sc/us/alert/json')

    params = {'to': '16365553226', 'server': 'host', 'link': 'http://example.com/'}

    self.assertOK(self.client.send_event_alert_message(params))
    self.assertRequestBodyIncludes(params)

  @responses.activate
  def test_send_marketing_message(self):
    self.stub(responses.POST, 'https://rest.nexmo.com/sc/us/marketing/json')

    params = {'from': 'short-code', 'to': '16365553226', 'keyword': 'NEXMO', 'text': 'Hello'}

    self.assertOK(self.client.send_marketing_message(params))
    self.assertRequestBodyIncludes(params)

  @responses.activate
  def test_initiate_call(self):
    self.stub(responses.POST, 'https://rest.nexmo.com/call/json')

    params = {'to': '16365553226', 'answer_url': 'http://example.com/answer'}

    self.assertOK(self.client.initiate_call(params))
    self.assertRequestBodyIncludes(params)

  @responses.activate
  def test_initiate_tts_call(self):
    self.stub(responses.POST, 'https://api.nexmo.com/tts/json')

    params = {'to': '16365553226', 'text': 'Hello'}

    self.assertOK(self.client.initiate_tts_call(params))
    self.assertRequestBodyIncludes(params)

  @responses.activate
  def test_initiate_tts_prompt_call(self):
    self.stub(responses.POST, 'https://api.nexmo.com/tts-prompt/json')

    params = {'to': '16365553226', 'text': 'Hello', 'max_digits': 4, 'bye_text': 'Goodbye'}

    self.assertOK(self.client.initiate_tts_prompt_call(params))
    self.assertRequestBodyIncludes(params)

  @responses.activate
  def test_send_verification_request(self):
    self.stub(responses.POST, 'https://api.nexmo.com/verify/json')

    params = {'number': '447525856424', 'brand': 'MyApp'}

    self.assertOK(self.client.send_verification_request(params))
    self.assertRequestBodyIncludes(params)

  @responses.activate
  def test_check_verification_request(self):
    self.stub(responses.POST, 'https://api.nexmo.com/verify/check/json')

    params = {'code': '123445', 'request_id': '8g88g88eg8g8gg9g90'}

    self.assertOK(self.client.check_verification_request(params))
    self.assertRequestBodyIncludes(params)

  @responses.activate
  def test_get_verification_request(self):
    self.stub(responses.GET, 'https://api.nexmo.com/verify/search/json')

    self.assertOK(self.client.get_verification_request('xxx'))
    self.assertRequestQueryIncludes('request_id=xxx')

  @responses.activate
  def test_control_verification_request(self):
    self.stub(responses.POST, 'https://api.nexmo.com/verify/control/json')

    params = {'cmd': 'cancel', 'request_id': '8g88g88eg8g8gg9g90'}

    self.assertOK(self.client.control_verification_request(params))
    self.assertRequestBodyIncludes(params)

  @responses.activate
  def test_get_basic_number_insight(self):
    self.stub(responses.GET, 'https://api.nexmo.com/number/format/json')

    self.assertOK(self.client.get_basic_number_insight(number='447525856424'))
    self.assertRequestQueryIncludes('number=447525856424')

  @responses.activate
  def test_get_number_insight(self):
    self.stub(responses.GET, 'https://api.nexmo.com/number/lookup/json')

    self.assertOK(self.client.get_number_insight(number='447525856424'))
    self.assertRequestQueryIncludes('number=447525856424')

  @responses.activate
  def test_request_number_insight(self):
    self.stub(responses.POST, 'https://rest.nexmo.com/ni/json')

    params = {'number': '447525856424', 'callback': 'https://example.com'}

    self.assertOK(self.client.request_number_insight(params))
    self.assertRequestBodyIncludes(params)

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


if __name__ == '__main__':
  unittest.main()

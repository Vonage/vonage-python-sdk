try:
  from urllib.parse import urljoin
except ImportError:
  from urlparse import urljoin

import requests, os


class Error(Exception):
  pass


class AuthenticationError(Error):
  pass


class Client():
  def __init__(self, **kwargs):
    self.api_key = kwargs.get('key', None) or os.environ['NEXMO_API_KEY']

    self.api_secret = kwargs.get('secret', None) or os.environ['NEXMO_API_SECRET']

    self.host = 'rest.nexmo.com'

  def send_message(self, params):
    return self.post('/sms/json', params)

  def get_balance(self):
    return self.get('/account/get-balance')

  def get_country_pricing(self, country_code):
    return self.get('/account/get-pricing/outbound', {'country': country_code})

  def get_prefix_pricing(self, prefix):
    return self.get('/account/get-prefix-pricing/outbound', {'prefix': prefix})

  def get_account_numbers(self, params=None, **kwargs):
    return self.get('/account/numbers', params or kwargs)

  def get_available_numbers(self, country_code, params=None, **kwargs):
    return self.get('/number/search', self.merge(params or kwargs, {'country': country_code}))

  def buy_number(self, params=None, **kwargs):
    return self.post('/number/buy', params or kwargs)

  def cancel_number(self, params=None, **kwargs):
    return self.post('/number/cancel', params or kwargs)

  def update_number(self, params=None, **kwargs):
    return self.post('/number/update', params or kwargs)

  def get_message(self, message_id):
    return self.get('/search/message', {'id': message_id})

  def get_message_rejections(self, params=None, **kwargs):
    return self.get('/search/rejections', params or kwargs)

  def search_messages(self, params=None, **kwargs):
    return self.get('/search/messages', params or kwargs)

  def send_ussd_push_message(self, params=None, **kwargs):
    return self.post('/ussd/json', params or kwargs)

  def send_ussd_prompt_message(self, params=None, **kwargs):
    return self.post('/ussd-prompt/json', params or kwargs)

  def send_2fa_message(self, params=None, **kwargs):
    return self.post('/sc/us/2fa/json', params or kwargs)

  def send_event_alert_message(self, params=None, **kwargs):
    return self.post('/sc/us/alert/json', params or kwargs)

  def send_marketing_message(self, params=None, **kwargs):
    return self.post('/sc/us/marketing/json', params or kwargs)

  def initiate_call(self, params=None, **kwargs):
    return self.post('/call/json', params or kwargs)

  def initiate_tts_call(self, params=None, **kwargs):
    return self.post('https://api.nexmo.com/tts/json', params or kwargs)

  def initiate_tts_prompt_call(self, params=None, **kwargs):
    return self.post('https://api.nexmo.com/tts-prompt/json', params or kwargs)

  def send_verification_request(self, params=None, **kwargs):
    return self.post('https://api.nexmo.com/verify/json', params or kwargs)

  def check_verification_request(self, params=None, **kwargs):
    return self.post('https://api.nexmo.com/verify/check/json', params or kwargs)

  def get_verification_request(self, request_id):
    return self.get('https://api.nexmo.com/verify/search/json', {'request_id': request_id})

  def control_verification_request(self, params=None, **kwargs):
    return self.post('https://api.nexmo.com/verify/control/json', params or kwargs)

  def request_number_insight(self, params=None, **kwargs):
    return self.post('/ni/json', params or kwargs)

  def get(self, request_uri, params={}):
    uri = urljoin('https://' + self.host, request_uri)

    params = self.merge(params, {'api_key': self.api_key, 'api_secret': self.api_secret})

    return self.parse(requests.get(uri, params=params))

  def post(self, request_uri, params):
    uri = urljoin('https://' + self.host, request_uri)

    params = self.merge(params, {'api_key': self.api_key, 'api_secret': self.api_secret})

    return self.parse(requests.post(uri, data=params))

  def parse(self, response):
    if response.status_code == 401:
      raise AuthenticationError
    elif 200 <= response.status_code < 300:
      return response.json()
    else:
      message = "unexpected http {code} response from nexmo api".format(code=response.status_code)

      raise Error(message)

  def merge(self, d1, d2):
    d3 = {}
    d3.update(d1)
    d3.update(d2)

    return d3

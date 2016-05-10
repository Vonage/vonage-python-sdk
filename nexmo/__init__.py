__version__ = '1.2.0'


import requests, os

from platform import python_version


class Error(Exception):
  pass


class ClientError(Error):
  pass


class ServerError(Error):
  pass


class AuthenticationError(ClientError):
  pass


class Client():
  def __init__(self, **kwargs):
    self.api_key = kwargs.get('key', None) or os.environ['NEXMO_API_KEY']

    self.api_secret = kwargs.get('secret', None) or os.environ['NEXMO_API_SECRET']

    self.headers = {'User-Agent': 'nexmo-python/{0}/{1}'.format(__version__, python_version())}

    self.host = 'rest.nexmo.com'

    self.api_host = 'api.nexmo.com'

  def send_message(self, params):
    return self.post(self.host, '/sms/json', params)

  def get_balance(self):
    return self.get(self.host, '/account/get-balance')

  def get_country_pricing(self, country_code):
    return self.get(self.host, '/account/get-pricing/outbound', {'country': country_code})

  def get_prefix_pricing(self, prefix):
    return self.get(self.host, '/account/get-prefix-pricing/outbound', {'prefix': prefix})

  def update_settings(self, params=None, **kwargs):
    return self.post(self.host, '/account/settings', params or kwargs)

  def topup(self, params=None, **kwargs):
    return self.post(self.host, '/account/top-up', params or kwargs)

  def get_account_numbers(self, params=None, **kwargs):
    return self.get(self.host, '/account/numbers', params or kwargs)

  def get_available_numbers(self, country_code, params=None, **kwargs):
    return self.get(self.host, '/number/search', dict(params or kwargs, country=country_code))

  def buy_number(self, params=None, **kwargs):
    return self.post(self.host, '/number/buy', params or kwargs)

  def cancel_number(self, params=None, **kwargs):
    return self.post(self.host, '/number/cancel', params or kwargs)

  def update_number(self, params=None, **kwargs):
    return self.post(self.host, '/number/update', params or kwargs)

  def get_message(self, message_id):
    return self.get(self.host, '/search/message', {'id': message_id})

  def get_message_rejections(self, params=None, **kwargs):
    return self.get(self.host, '/search/rejections', params or kwargs)

  def search_messages(self, params=None, **kwargs):
    return self.get(self.host, '/search/messages', params or kwargs)

  def send_ussd_push_message(self, params=None, **kwargs):
    return self.post(self.host, '/ussd/json', params or kwargs)

  def send_ussd_prompt_message(self, params=None, **kwargs):
    return self.post(self.host, '/ussd-prompt/json', params or kwargs)

  def send_2fa_message(self, params=None, **kwargs):
    return self.post(self.host, '/sc/us/2fa/json', params or kwargs)

  def send_event_alert_message(self, params=None, **kwargs):
    return self.post(self.host, '/sc/us/alert/json', params or kwargs)

  def send_marketing_message(self, params=None, **kwargs):
    return self.post(self.host, '/sc/us/marketing/json', params or kwargs)

  def initiate_call(self, params=None, **kwargs):
    return self.post(self.host, '/call/json', params or kwargs)

  def initiate_tts_call(self, params=None, **kwargs):
    return self.post(self.api_host, '/tts/json', params or kwargs)

  def initiate_tts_prompt_call(self, params=None, **kwargs):
    return self.post(self.api_host, '/tts-prompt/json', params or kwargs)

  def send_verification_request(self, params=None, **kwargs):
    return self.post(self.api_host, '/verify/json', params or kwargs)

  def check_verification_request(self, params=None, **kwargs):
    return self.post(self.api_host, '/verify/check/json', params or kwargs)

  def get_verification_request(self, request_id):
    return self.get(self.api_host, '/verify/search/json', {'request_id': request_id})

  def control_verification_request(self, params=None, **kwargs):
    return self.post(self.api_host, '/verify/control/json', params or kwargs)

  def get_basic_number_insight(self, params=None, **kwargs):
    return self.get(self.api_host, '/number/format/json', params or kwargs)

  def get_number_insight(self, params=None, **kwargs):
    return self.get(self.api_host, '/number/lookup/json', params or kwargs)

  def request_number_insight(self, params=None, **kwargs):
    return self.post(self.host, '/ni/json', params or kwargs)

  def get(self, host, request_uri, params={}):
    uri = 'https://' + host + request_uri

    params = dict(params, api_key=self.api_key, api_secret=self.api_secret)

    return self.parse(host, requests.get(uri, params=params, headers=self.headers))

  def post(self, host, request_uri, params):
    uri = 'https://' + host + request_uri

    params = dict(params, api_key=self.api_key, api_secret=self.api_secret)

    return self.parse(host, requests.post(uri, data=params, headers=self.headers))

  def parse(self, host, response):
    if response.status_code == 401:
      raise AuthenticationError
    elif 200 <= response.status_code < 300:
      return response.json()
    elif 400 <= response.status_code < 500:
      message = "{code} response from {host}".format(code=response.status_code, host=host)

      raise ClientError(message)
    elif 500 <= response.status_code < 600:
      message = "{code} response from {host}".format(code=response.status_code, host=host)

      raise ServerError(message)

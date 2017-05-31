__version__ = '1.5.0'

import requests, os, warnings, hashlib, hmac, jwt, time, uuid, sys

from platform import python_version

if sys.version_info[0] == 3:
    string_types = (str, bytes)
else:
    string_types = (unicode, str)


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
        self.api_key = kwargs.get('key', None) or os.environ.get('NEXMO_API_KEY', None)

        self.api_secret = kwargs.get('secret', None) or os.environ.get('NEXMO_API_SECRET', None)

        self.signature_secret = kwargs.get('signature_secret', None) or os.environ.get('NEXMO_SIGNATURE_SECRET', None)

        self.application_id = kwargs.get('application_id', None)

        self.private_key = kwargs.get('private_key', None)

        if isinstance(self.private_key, string_types) and '\n' not in self.private_key:
            with open(self.private_key, 'rb') as key_file:
                self.private_key = key_file.read()

        self.host = 'rest.nexmo.com'

        self.api_host = 'api.nexmo.com'

        user_agent = 'nexmo-python/{0}/{1}'.format(__version__, python_version())

        if 'app_name' in kwargs and 'app_version' in kwargs:
            user_agent += '/{0}/{1}'.format(kwargs['app_name'], kwargs['app_version'])

        self.headers = {'User-Agent': user_agent}

        self.auth_params = {}

    def auth(self, params=None, **kwargs):
        self.auth_params = params or kwargs

    def send_message(self, params):
        return self.post(self.host, '/sms/json', params)

    def get_balance(self):
        return self.get(self.host, '/account/get-balance')

    def get_country_pricing(self, country_code):
        return self.get(self.host, '/account/get-pricing/outbound', {'country': country_code})

    def get_prefix_pricing(self, prefix):
        return self.get(self.host, '/account/get-prefix-pricing/outbound', {'prefix': prefix})

    def get_sms_pricing(self, number):
        return self.get(self.host, '/account/get-phone-pricing/outbound/sms', {'phone': number})

    def get_voice_pricing(self, number):
        return self.get(self.host, '/account/get-phone-pricing/outbound/voice', {'phone': number})

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

    def get_event_alert_numbers(self):
        return self.get(self.host, '/sc/us/alert/opt-in/query/json')

    def resubscribe_event_alert_number(self, params=None, **kwargs):
        return self.post(self.host, '/sc/us/alert/opt-in/manage/json', params or kwargs)

    def initiate_call(self, params=None, **kwargs):
        return self.post(self.host, '/call/json', params or kwargs)

    def initiate_tts_call(self, params=None, **kwargs):
        return self.post(self.api_host, '/tts/json', params or kwargs)

    def initiate_tts_prompt_call(self, params=None, **kwargs):
        return self.post(self.api_host, '/tts-prompt/json', params or kwargs)

    def start_verification(self, params=None, **kwargs):
        return self.post(self.api_host, '/verify/json', params or kwargs)

    def send_verification_request(self, params=None, **kwargs):
        warnings.warn('nexmo.Client#send_verification_request is deprecated (use #start_verification instead)',
                      DeprecationWarning, stacklevel=2)

        return self.post(self.api_host, '/verify/json', params or kwargs)

    def check_verification(self, request_id, params=None, **kwargs):
        return self.post(self.api_host, '/verify/check/json', dict(params or kwargs, request_id=request_id))

    def check_verification_request(self, params=None, **kwargs):
        warnings.warn('nexmo.Client#check_verification_request is deprecated (use #check_verification instead)',
                      DeprecationWarning, stacklevel=2)

        return self.post(self.api_host, '/verify/check/json', params or kwargs)

    def get_verification(self, request_id):
        return self.get(self.api_host, '/verify/search/json', {'request_id': request_id})

    def get_verification_request(self, request_id):
        warnings.warn('nexmo.Client#get_verification_request is deprecated (use #get_verification instead)',
                      DeprecationWarning, stacklevel=2)

        return self.get(self.api_host, '/verify/search/json', {'request_id': request_id})

    def cancel_verification(self, request_id):
        return self.post(self.api_host, '/verify/control/json', {'request_id': request_id, 'cmd': 'cancel'})

    def trigger_next_verification_event(self, request_id):
        return self.post(self.api_host, '/verify/control/json', {'request_id': request_id, 'cmd': 'trigger_next_event'})

    def control_verification_request(self, params=None, **kwargs):
        warnings.warn('nexmo.Client#control_verification_request is deprecated', DeprecationWarning, stacklevel=2)

        return self.post(self.api_host, '/verify/control/json', params or kwargs)

    def get_basic_number_insight(self, params=None, **kwargs):
        return self.get(self.api_host, '/ni/basic/json', params or kwargs)

    def get_standard_number_insight(self, params=None, **kwargs):
        return self.get(self.api_host, '/ni/standard/json', params or kwargs)

    def get_number_insight(self, params=None, **kwargs):
        warnings.warn('nexmo.Client#get_number_insight is deprecated (use #get_standard_number_insight instead)',
                      DeprecationWarning, stacklevel=2)

        return self.get(self.api_host, '/number/lookup/json', params or kwargs)

    def get_advanced_number_insight(self, params=None, **kwargs):
        return self.get(self.api_host, '/ni/advanced/json', params or kwargs)

    def request_number_insight(self, params=None, **kwargs):
        return self.post(self.host, '/ni/json', params or kwargs)

    def get_applications(self, params=None, **kwargs):
        return self.get(self.api_host, '/v1/applications', params or kwargs)

    def get_application(self, application_id):
        return self.get(self.api_host, '/v1/applications/' + application_id)

    def create_application(self, params=None, **kwargs):
        return self.post(self.api_host, '/v1/applications', params or kwargs)

    def update_application(self, application_id, params=None, **kwargs):
        return self.put(self.api_host, '/v1/applications/' + application_id, params or kwargs)

    def delete_application(self, application_id):
        return self.delete(self.api_host, '/v1/applications/' + application_id)

    def create_call(self, params=None, **kwargs):
        return self.__post('/v1/calls', params or kwargs)

    def get_calls(self, params=None, **kwargs):
        return self.__get('/v1/calls', params or kwargs)

    def get_call(self, uuid):
        return self.__get('/v1/calls/' + uuid)

    def update_call(self, uuid, params=None, **kwargs):
        return self.__put('/v1/calls/' + uuid, params or kwargs)

    def send_audio(self, uuid, params=None, **kwargs):
        return self.__put('/v1/calls/' + uuid + '/stream', params or kwargs)

    def stop_audio(self, uuid):
        return self.__delete('/v1/calls/' + uuid + '/stream')

    def send_speech(self, uuid, params=None, **kwargs):
        return self.__put('/v1/calls/' + uuid + '/talk', params or kwargs)

    def stop_speech(self, uuid):
        return self.__delete('/v1/calls/' + uuid + '/talk')

    def send_dtmf(self, uuid, params=None, **kwargs):
        return self.__put('/v1/calls/' + uuid + '/dtmf', params or kwargs)

    def check_signature(self, params):
        params = dict(params)

        signature = params.pop('sig', '')

        return hmac.compare_digest(signature, self.signature(params))

    def signature(self, params):
        md5 = hashlib.md5()

        for key in sorted(params):
            md5.update('&{0}={1}'.format(key, params[key]).encode('utf-8'))

        md5.update(self.signature_secret.encode('utf-8'))

        return md5.hexdigest()

    def get(self, host, request_uri, params={}):
        uri = 'https://' + host + request_uri

        params = dict(params, api_key=self.api_key, api_secret=self.api_secret)

        return self.parse(host, requests.get(uri, params=params, headers=self.headers))

    def post(self, host, request_uri, params):
        uri = 'https://' + host + request_uri

        params = dict(params, api_key=self.api_key, api_secret=self.api_secret)

        return self.parse(host, requests.post(uri, data=params, headers=self.headers))

    def put(self, host, request_uri, params):
        uri = 'https://' + host + request_uri

        params = dict(params, api_key=self.api_key, api_secret=self.api_secret)

        return self.parse(host, requests.put(uri, json=params, headers=self.headers))

    def delete(self, host, request_uri):
        uri = 'https://' + host + request_uri

        params = dict(api_key=self.api_key, api_secret=self.api_secret)

        return self.parse(host, requests.delete(uri, params=params, headers=self.headers))

    def parse(self, host, response):
        if response.status_code == 401:
            raise AuthenticationError
        elif response.status_code == 204:
            return None
        elif 200 <= response.status_code < 300:
            return response.json()
        elif 400 <= response.status_code < 500:
            message = "{code} response from {host}".format(code=response.status_code, host=host)

            raise ClientError(message)
        elif 500 <= response.status_code < 600:
            message = "{code} response from {host}".format(code=response.status_code, host=host)

            raise ServerError(message)

    def __get(self, request_uri, params={}):
        uri = 'https://' + self.api_host + request_uri

        return self.parse(self.api_host, requests.get(uri, params=params, headers=self.__headers()))

    def __post(self, request_uri, params):
        uri = 'https://' + self.api_host + request_uri

        return self.parse(self.api_host, requests.post(uri, json=params, headers=self.__headers()))

    def __put(self, request_uri, params):
        uri = 'https://' + self.api_host + request_uri

        return self.parse(self.api_host, requests.put(uri, json=params, headers=self.__headers()))

    def __delete(self, request_uri):
        uri = 'https://' + self.api_host + request_uri

        return self.parse(self.api_host, requests.delete(uri, headers=self.__headers()))

    def __headers(self):
        iat = int(time.time())

        payload = dict(self.auth_params)
        payload.setdefault('application_id', self.application_id)
        payload.setdefault('iat', iat)
        payload.setdefault('exp', iat + 60)
        payload.setdefault('jti', str(uuid.uuid4()))

        token = jwt.encode(payload, self.private_key, algorithm='RS256')

        return dict(self.headers, Authorization=b'Bearer ' + token)

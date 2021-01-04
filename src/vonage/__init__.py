from ._internal import ApplicationV2, BasicAuthenticatedServer, _format_date_param
from .errors import *
from .voice import *
from .sms import *
from .verify import *
from datetime import datetime
import logging
from platform import python_version

import base64
import hashlib
import hmac
import jwt
import os
import pytz
import requests
import sys
import time
from uuid import uuid4
import warnings
import re
from deprecated import deprecated


string_types = (str, bytes)
from urllib.parse import urlparse

try:
    from json import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError


__version__ = "2.4.0"

logger = logging.getLogger("nexmo")


class Client:
    """
    Create a Client object to start making calls to Nexmo APIs.

    Most methods corresponding to Nexmo API calls are on this class itself,
    although newer APIs are under namespaces like :attr:`Client.application_v2`.

    The credentials you provide when instantiating a Client determine which
    methods can be called. Consult the `Nexmo API docs <https://developer.nexmo.com/api/>`_ for details of the
    authentication used by the APIs you wish to use, and instantiate your
    Client with the appropriate credentials.

    :param str key: Your Nexmo API key
    :param str secret: Your Nexmo API secret.
    :param str signature_secret: Your Nexmo API signature secret.
        You may need to have this enabled by Nexmo support. It is only used for SMS authentication.
    :param str signature_method:
        The encryption method used for signature encryption. This must match the method
        configured in the Nexmo Dashboard. We recommend `sha256` or `sha512`.
        This should be one of `md5`, `sha1`, `sha256`, or `sha512` if using HMAC digests.
        If you want to use a simple MD5 hash, leave this as `None`.
    :param str application_id: Your application ID if calling methods which use JWT authentication.
    :param str private_key: Your private key if calling methods which use JWT authentication.
        This should either be a str containing the key in its PEM form, or a path to a private key file.
    :param str app_name: This optional value is added to the user-agent header
        provided by this library and can be used by Nexmo to track your app statistics.
    :param str app_version: This optional value is added to the user-agent header
        provided by this library and can be used by Nexmo to track your app statistics.
    """

    def __init__(
        self,
        key=None,
        secret=None,
        signature_secret=None,
        signature_method=None,
        application_id=None,
        private_key=None,
        app_name=None,
        app_version=None,
    ):
        self.api_key = key or os.environ.get("VONAGE_API_KEY", None)

        self.api_secret = secret or os.environ.get("VONAGE_API_SECRET", None)

        self.signature_secret = signature_secret or os.environ.get(
            "VONAGE_SIGNATURE_SECRET", None
        )

        self.signature_method = signature_method or os.environ.get(
            "VONAGE_SIGNATURE_METHOD", None
        )

        if self.signature_method in {"md5", "sha1", "sha256", "sha512"}:
            self.signature_method = getattr(hashlib, signature_method)

        self.application_id = application_id

        self.private_key = private_key

        if isinstance(self.private_key, string_types) and "\n" not in self.private_key:
            with open(self.private_key, "rb") as key_file:
                self.private_key = key_file.read()

        self.__host_pattern = "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$|^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)+([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$"

        self.__host = "rest.nexmo.com"

        self.__api_host = "api.nexmo.com"

        user_agent = "vonage-python/{version} python/{python_version}".format(
            version=__version__, python_version=python_version()
        )

        if app_name and app_version:
            user_agent += " {app_name}/{app_version}".format(
                app_name=app_name, app_version=app_version
            )

        self.headers = {"User-Agent": user_agent}

        self.auth_params = {}

        api_server = BasicAuthenticatedServer(
            "https://api.nexmo.com",
            user_agent=user_agent,
            api_key=self.api_key,
            api_secret=self.api_secret,
        )
        self.application_v2 = ApplicationV2(api_server)

        self.session = requests.Session()

    # Get and Set __host attribute
    def host(self, value=None):
        if value is None:
            return self.__host
        elif not re.match(self.__host_pattern, value):
            raise Exception("Error: Invalid format for host")
        else:
            self.__host = value

    # Gets And sets __api_host attribute
    def api_host(self, value=None):
        if value is None:
            return self.__api_host
        elif not re.match(self.__host_pattern, value):
            raise Exception("Error: Invalid format for api_host")
        else:
            self.__api_host = value

    def auth(self, params=None, **kwargs):
        self.auth_params = params or kwargs

    @deprecated(
        reason="vonage.Client#send_message is deprecated. Use Sms#send_message instead"
    )
    def send_message(self, params):
        """
        Send an SMS message.
        Requires a client initialized with `key` and either `secret` or `signature_secret`.
        ::
            client.send_message({
                "to": MY_CELLPHONE,
                "from": MY_VONAGE_NUMBER,
                "text": "Hello From Nexmo!",
            })
        :param dict params: A dict of values described at `Send an SMS <https://developer.nexmo.com/api/sms#send-an-sms>`_
        """
        return self.post(self.host(), "/sms/json", params, supports_signature_auth=True)

    def get_balance(self):
        return self.get(self.host(), "/account/get-balance")

    def get_country_pricing(self, country_code):
        return self.get(
            self.host(), "/account/get-pricing/outbound", {"country": country_code}
        )

    def get_prefix_pricing(self, prefix):
        return self.get(
            self.host(), "/account/get-prefix-pricing/outbound", {"prefix": prefix}
        )

    def get_sms_pricing(self, number):
        return self.get(
            self.host(), "/account/get-phone-pricing/outbound/sms", {"phone": number}
        )

    def get_voice_pricing(self, number):
        return self.get(
            self.host(), "/account/get-phone-pricing/outbound/voice", {"phone": number}
        )

    def update_settings(self, params=None, **kwargs):
        return self.post(self.host(), "/account/settings", params or kwargs)

    def topup(self, params=None, **kwargs):
        return self.post(self.host(), "/account/top-up", params or kwargs)

    def get_account_numbers(self, params=None, **kwargs):
        return self.get(self.host(), "/account/numbers", params or kwargs)

    def get_available_numbers(self, country_code, params=None, **kwargs):
        return self.get(
            self.host(), "/number/search", dict(params or kwargs, country=country_code)
        )

    def buy_number(self, params=None, **kwargs):
        return self.post(self.host(), "/number/buy", params or kwargs)

    def cancel_number(self, params=None, **kwargs):
        return self.post(self.host(), "/number/cancel", params or kwargs)

    def update_number(self, params=None, **kwargs):
        return self.post(self.host(), "/number/update", params or kwargs)

    def get_message(self, message_id):
        return self.get(self.host(), "/search/message", {"id": message_id})

    def get_message_rejections(self, params=None, **kwargs):
        return self.get(self.host(), "/search/rejections", params or kwargs)

    def search_messages(self, params=None, **kwargs):
        return self.get(self.host(), "/search/messages", params or kwargs)

    def send_ussd_push_message(self, params=None, **kwargs):
        return self.post(self.host(), "/ussd/json", params or kwargs)

    def send_ussd_prompt_message(self, params=None, **kwargs):
        return self.post(self.host(), "/ussd-prompt/json", params or kwargs)

    def send_2fa_message(self, params=None, **kwargs):
        return self.post(self.host(), "/sc/us/2fa/json", params or kwargs)

    def submit_sms_conversion(self, message_id, delivered=True, timestamp=None):
        """
        Notify Nexmo that an SMS was successfully received.

        :param message_id: The `message-id` str returned by the send_message call.
        :param delivered: A `bool` indicating that the message was or was not successfully delivered.
        :param timestamp: A `datetime` object containing the time the SMS arrived.
        :return: The parsed response from the server. On success, the bytestring b'OK'
        """
        params = {
            "message-id": message_id,
            "delivered": delivered,
            "timestamp": timestamp or datetime.now(pytz.utc),
        }
        # Ensure timestamp is a string:
        _format_date_param(params, "timestamp")
        return self.post(self.api_host(), "/conversions/sms", params)

    def send_event_alert_message(self, params=None, **kwargs):
        return self.post(self.host(), "/sc/us/alert/json", params or kwargs)

    def send_marketing_message(self, params=None, **kwargs):
        return self.post(self.host(), "/sc/us/marketing/json", params or kwargs)

    def get_event_alert_numbers(self):
        return self.get(self.host(), "/sc/us/alert/opt-in/query/json")

    def resubscribe_event_alert_number(self, params=None, **kwargs):
        return self.post(
            self.host(), "/sc/us/alert/opt-in/manage/json", params or kwargs
        )

    def initiate_call(self, params=None, **kwargs):
        return self.post(self.host(), "/call/json", params or kwargs)

    def initiate_tts_call(self, params=None, **kwargs):
        return self.post(self.api_host(), "/tts/json", params or kwargs)

    def initiate_tts_prompt_call(self, params=None, **kwargs):
        return self.post(self.api_host(), "/tts-prompt/json", params or kwargs)

    @deprecated(
        reason="vonage.Client#start_verification is deprecated. Use Verify#start_verification instead"
    )
    def start_verification(self, params=None, **kwargs):
        return self.post(self.api_host(), "/verify/json", params or kwargs)

    def send_verification_request(self, params=None, **kwargs):
        warnings.warn(
            "vonage.Client#send_verification_request is deprecated (use Verify#start_verification instead)",
            DeprecationWarning,
            stacklevel=2,
        )

        return self.post(self.api_host(), "/verify/json", params or kwargs)

    @deprecated(
        reason="vonage.Client#check_verification is deprecated. Use Verify#check instead"
    )
    def check_verification(self, request_id, params=None, **kwargs):
        return self.post(
            self.api_host(),
            "/verify/check/json",
            dict(params or kwargs, request_id=request_id),
        )

    def check_verification_request(self, params=None, **kwargs):
        warnings.warn(
            "vonage.Client#check_verification_request is deprecated (use Verify#check instead)",
            DeprecationWarning,
            stacklevel=2,
        )

        return self.post(self.api_host(), "/verify/check/json", params or kwargs)

    @deprecated(
        reason="vonage.Client#start_psd2_verification_request is deprecated. Use Verify#psd2 instead"
    )
    def start_psd2_verification_request(self, params=None, **kwargs):
        return self.post(self.api_host(), "/verify/psd2/json", params or kwargs)

    @deprecated(
        reason="vonage.Client#get_verification is deprecated. Use Verify#search instead"
    )
    def get_verification(self, request_id):
        return self.get(
            self.api_host(), "/verify/search/json", {"request_id": request_id}
        )

    def get_verification_request(self, request_id):
        warnings.warn(
            "vonage.Client#get_verification_request is deprecated (use Verify#search instead)",
            DeprecationWarning,
            stacklevel=2,
        )

        return self.get(
            self.api_host(), "/verify/search/json", {"request_id": request_id}
        )

    @deprecated(
        reason="vonage.Client#cancel_verification is deprecated. Use Verify#cancel instead"
    )
    def cancel_verification(self, request_id):
        return self.post(
            self.api_host(),
            "/verify/control/json",
            {"request_id": request_id, "cmd": "cancel"},
        )

    @deprecated(
        reason="vonage.Client#trigger_next_verification_event is deprecated. Use Verify#trigger_next_event instead"
    )
    def trigger_next_verification_event(self, request_id):
        return self.post(
            self.api_host(),
            "/verify/control/json",
            {"request_id": request_id, "cmd": "trigger_next_event"},
        )

    def control_verification_request(self, params=None, **kwargs):
        warnings.warn(
            "vonage.Client#control_verification_request is deprecated",
            DeprecationWarning,
            stacklevel=2,
        )

        return self.post(self.api_host(), "/verify/control/json", params or kwargs)

    def get_basic_number_insight(self, params=None, **kwargs):
        return self.get(self.api_host(), "/ni/basic/json", params or kwargs)

    def get_standard_number_insight(self, params=None, **kwargs):
        return self.get(self.api_host(), "/ni/standard/json", params or kwargs)

    def get_number_insight(self, params=None, **kwargs):
        warnings.warn(
            "vonage.Client#get_number_insight is deprecated (use #get_standard_number_insight instead)",
            DeprecationWarning,
            stacklevel=2,
        )

        return self.get(self.api_host(), "/number/lookup/json", params or kwargs)

    def get_async_advanced_number_insight(self, params=None, **kwargs):
        argoparams = params or kwargs
        if "callback" in argoparams:
            return self.get(
                self.api_host(), "/ni/advanced/async/json", params or kwargs
            )
        else:
            raise ClientError(
                "Error: Callback needed for async advanced number insight"
            )

    def get_advanced_number_insight(self, params=None, **kwargs):
        return self.get(self.api_host(), "/ni/advanced/json", params or kwargs)

    def request_number_insight(self, params=None, **kwargs):
        return self.post(self.host(), "/ni/json", params or kwargs)

    def get_applications(self, params=None, **kwargs):
        warnings.warn(
            "vonage.Client#get_applications is deprecated (use methods from #application_v2 instead)",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get(self.api_host(), "/v1/applications", params or kwargs)

    def get_application(self, application_id):
        warnings.warn(
            "vonage.Client#get_application is deprecated (use methods from #application_v2 instead)",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.get(
            self.api_host(),
            "/v1/applications/{application_id}".format(application_id=application_id),
        )

    def create_application(self, params=None, **kwargs):
        warnings.warn(
            "vonage.Client#create_application is deprecated (use methods from #application_v2 instead)",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.post(self.api_host(), "/v1/applications", params or kwargs)

    def update_application(self, application_id, params=None, **kwargs):
        warnings.warn(
            "vonage.Client#update_application is deprecated (use methods from #application_v2 instead)",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.put(
            self.api_host(),
            "/v1/applications/{application_id}".format(application_id=application_id),
            params or kwargs,
        )

    def delete_application(self, application_id):
        warnings.warn(
            "vonage.Client#delete_application is deprecated (use methods from #application_v2 instead)",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.delete(
            self.api_host(),
            "/v1/applications/{application_id}".format(application_id=application_id),
        )

    @deprecated(
        reason="vonage.Client#create_call is deprecated. Use Voice#create_call instead"
    )
    def create_call(self, params=None, **kwargs):
        return self._jwt_signed_post("/v1/calls", params or kwargs)

    @deprecated(
        reason="vonage.Client#get_calls is deprecated. Use Voice#get_calls instead"
    )
    def get_calls(self, params=None, **kwargs):
        return self._jwt_signed_get("/v1/calls", params or kwargs)

    @deprecated(
        reason="vonage.Client#get_call is deprecated. Use Voice#get_call instead"
    )
    def get_call(self, uuid):
        return self._jwt_signed_get("/v1/calls/{uuid}".format(uuid=uuid))

    @deprecated(
        reason="vonage.Client#update_call is deprecated. Use Voice#update_call instead"
    )
    def update_call(self, uuid, params=None, **kwargs):
        return self._jwt_signed_put(
            "/v1/calls/{uuid}".format(uuid=uuid), params or kwargs
        )

    @deprecated(
        reason="vonage.Client#send_audio is deprecated. Use Voice#send_audio instead"
    )
    def send_audio(self, uuid, params=None, **kwargs):
        return self._jwt_signed_put(
            "/v1/calls/{uuid}/stream".format(uuid=uuid), params or kwargs
        )

    @deprecated(
        reason="vonage.Client#stop_audio is deprecated. Use Voice#stop_audio instead"
    )
    def stop_audio(self, uuid):
        return self._jwt_signed_delete("/v1/calls/{uuid}/stream".format(uuid=uuid))

    @deprecated(
        reason="vonage.Client#send_speech is deprecated. Use Voice#send_speech instead"
    )
    def send_speech(self, uuid, params=None, **kwargs):
        return self._jwt_signed_put(
            "/v1/calls/{uuid}/talk".format(uuid=uuid), params or kwargs
        )

    @deprecated(
        reason="vonage.Client#stop_speech is deprecated. Use Voice#stop_speech instead"
    )
    def stop_speech(self, uuid):
        return self._jwt_signed_delete("/v1/calls/{uuid}/talk".format(uuid=uuid))

    @deprecated(
        reason="vonage.Client#send_dtmf is deprecated. Use Voice#send_dtmf instead"
    )
    def send_dtmf(self, uuid, params=None, **kwargs):
        return self._jwt_signed_put(
            "/v1/calls/{uuid}/dtmf".format(uuid=uuid), params or kwargs
        )

    def get_recording(self, url):
        hostname = urlparse(url).hostname
        return self.parse(hostname, self.session.get(url, headers=self._headers()))

    def redact_transaction(self, id, product, type=None):
        params = {"id": id, "product": product}
        if type is not None:
            params["type"] = type
        return self._post_json(self.api_host(), "/v1/redact/transaction", params)

    def list_secrets(self, api_key):
        return self.get(
            self.api_host(),
            "/accounts/{api_key}/secrets".format(api_key=api_key),
            header_auth=True,
        )

    def get_secret(self, api_key, secret_id):
        return self.get(
            self.api_host(),
            "/accounts/{api_key}/secrets/{secret_id}".format(
                api_key=api_key, secret_id=secret_id
            ),
            header_auth=True,
        )

    def create_secret(self, api_key, secret):
        body = {"secret": secret}
        return self._post_json(
            self.api_host(), "/accounts/{api_key}/secrets".format(api_key=api_key), body
        )

    def delete_secret(self, api_key, secret_id):
        return self.delete(
            self.api_host(),
            "/accounts/{api_key}/secrets/{secret_id}".format(
                api_key=api_key, secret_id=secret_id
            ),
            header_auth=True,
        )

    def check_signature(self, params):
        params = dict(params)
        signature = params.pop("sig", "").lower()
        return hmac.compare_digest(signature, self.signature(params))

    def signature(self, params):
        if self.signature_method:
            hasher = hmac.new(
                self.signature_secret.encode(), digestmod=self.signature_method
            )
        else:
            hasher = hashlib.md5()

        # Add timestamp if not already present
        if not params.get("timestamp"):
            params["timestamp"] = int(time.time())

        for key in sorted(params):
            value = params[key]

            if isinstance(value, str):
                value = value.replace("&", "_").replace("=", "_")

            hasher.update("&{key}={value}".format(key=key, value=value).encode("utf-8"))

        if self.signature_method is None:
            hasher.update(self.signature_secret.encode())

        return hasher.hexdigest()

    def get(self, host, request_uri, params=None, header_auth=False):
        uri = "https://{host}{request_uri}".format(host=host, request_uri=request_uri)
        headers = self.headers
        if header_auth:
            h = base64.b64encode(
                (
                    "{api_key}:{api_secret}".format(
                        api_key=self.api_key, api_secret=self.api_secret
                    ).encode("utf-8")
                )
            ).decode("ascii")
            headers = dict(headers or {}, Authorization="Basic {hash}".format(hash=h))
        else:
            params = dict(
                params or {}, api_key=self.api_key, api_secret=self.api_secret
            )
        logger.debug("GET to %r with params %r, headers %r", uri, params, headers)
        return self.parse(host, self.session.get(uri, params=params, headers=headers))

    def post(
        self,
        host,
        request_uri,
        params,
        supports_signature_auth=False,
        header_auth=False,
    ):
        """
        Low-level method to make a post request to a Nexmo API server.
        This method automatically adds authentication, picking the first applicable authentication method from the following:
        - If the supports_signature_auth param is True, and the client was instantiated with a signature_secret, then signature authentication will be used.
        - If the header_auth param is True, then basic authentication will be used, with the client's key and secret.
        - Otherwise the client's key and secret are appended to the post request's params.
        :param bool supports_signature_auth: Preferentially use signature authentication if a signature_secret was provided when initializing this client.
        :param bool header_auth: Use basic authentication instead of adding api_key and api_secret to the request params.
        """
        uri = "https://{host}{request_uri}".format(host=host, request_uri=request_uri)
        headers = self.headers
        if supports_signature_auth and self.signature_secret:
            params["api_key"] = self.api_key
            params["sig"] = self.signature(params)
        elif header_auth:
            h = base64.b64encode(
                (
                    "{api_key}:{api_secret}".format(
                        api_key=self.api_key, api_secret=self.api_secret
                    ).encode("utf-8")
                )
            ).decode("ascii")
            headers = dict(headers or {}, Authorization="Basic {hash}".format(hash=h))
        else:
            params = dict(params, api_key=self.api_key, api_secret=self.api_secret)
        logger.debug("POST to %r with params %r, headers %r", uri, params, headers)
        return self.parse(host, self.session.post(uri, data=params, headers=headers))

    def _post_json(self, host, request_uri, json):
        """
        Post json to `request_uri`, using basic auth.
        """
        uri = "https://{host}{request_uri}".format(host=host, request_uri=request_uri)
        auth = base64.b64encode(
            (
                "{api_key}:{api_secret}".format(
                    api_key=self.api_key, api_secret=self.api_secret
                ).encode("utf-8")
            )
        ).decode("ascii")
        headers = dict(
            self.headers or {}, Authorization="Basic {hash}".format(hash=auth)
        )
        logger.debug(
            "POST to %r with body: %r, headers: %r", request_uri, json, headers
        )
        return self.parse(host, self.session.post(uri, headers=headers, json=json))

    def put(self, host, request_uri, params, header_auth=False):
        uri = "https://{host}{request_uri}".format(host=host, request_uri=request_uri)

        headers = self.headers
        if header_auth:
            h = base64.b64encode(
                (
                    "{api_key}:{api_secret}".format(
                        api_key=self.api_key, api_secret=self.api_secret
                    ).encode("utf-8")
                )
            ).decode("ascii")
            # Must create a new headers dict here, otherwise we'd be mutating `self.headers`:
            headers = dict(headers or {}, Authorization="Basic {hash}".format(hash=h))
        else:
            params = dict(params, api_key=self.api_key, api_secret=self.api_secret)
        logger.debug("PUT to %r with params %r, headers %r", uri, params, headers)
        return self.parse(host, self.session.put(uri, json=params, headers=headers))

    def delete(self, host, request_uri, header_auth=False):
        uri = "https://{host}{request_uri}".format(host=host, request_uri=request_uri)

        params = None
        headers = self.headers
        if header_auth:
            h = base64.b64encode(
                (
                    "{api_key}:{api_secret}".format(
                        api_key=self.api_key, api_secret=self.api_secret
                    ).encode("utf-8")
                )
            ).decode("ascii")
            # Must create a new headers dict here, otherwise we'd be mutating `self.headers`:
            headers = dict(headers or {}, Authorization="Basic {hash}".format(hash=h))
        else:
            params = {"api_key": self.api_key, "api_secret": self.api_secret}
        logger.debug("DELETE to %r with params %r, headers %r", uri, params, headers)
        return self.parse(
            host, self.session.delete(uri, params=params, headers=headers)
        )

    def parse(self, host, response):
        logger.debug("Response headers %r", response.headers)
        if response.status_code == 401:
            raise AuthenticationError
        elif response.status_code == 204:
            return None
        elif 200 <= response.status_code < 300:

            # Strip off any encoding from the content-type header:
            content_mime = response.headers.get("content-type").split(";", 1)[0]
            if content_mime == "application/json":
                return response.json()
            else:
                return response.content
        elif 400 <= response.status_code < 500:
            logger.warning(
                "Client error: %s %r", response.status_code, response.content
            )
            message = "{code} response from {host}".format(
                code=response.status_code, host=host
            )

            # Test for standard error format:
            try:
                error_data = response.json()
                if (
                    "type" in error_data
                    and "title" in error_data
                    and "detail" in error_data
                ):
                    message = "{title}: {detail} ({type})".format(
                        title=error_data["title"],
                        detail=error_data["detail"],
                        type=error_data["type"],
                    )
            except JSONDecodeError:
                pass
            raise ClientError(message)
        elif 500 <= response.status_code < 600:
            logger.warning(
                "Server error: %s %r", response.status_code, response.content
            )
            message = "{code} response from {host}".format(
                code=response.status_code, host=host
            )
            raise ServerError(message)

    def _jwt_signed_get(self, request_uri, params=None):
        uri = "https://{api_host}{request_uri}".format(
            api_host=self.api_host(), request_uri=request_uri
        )

        return self.parse(
            self.api_host(),
            self.session.get(uri, params=params or {}, headers=self._headers()),
        )

    def _jwt_signed_post(self, request_uri, params):
        uri = "https://{api_host}{request_uri}".format(
            api_host=self.api_host(), request_uri=request_uri
        )

        return self.parse(
            self.api_host(),
            self.session.post(uri, json=params, headers=self._headers()),
        )

    def _jwt_signed_put(self, request_uri, params):
        uri = "https://{api_host}{request_uri}".format(
            api_host=self.api_host(), request_uri=request_uri
        )

        return self.parse(
            self.api_host(), self.session.put(uri, json=params, headers=self._headers())
        )

    def _jwt_signed_delete(self, request_uri):
        uri = "https://{api_host}{request_uri}".format(
            api_host=self.api_host(), request_uri=request_uri
        )

        return self.parse(
            self.api_host(), self.session.delete(uri, headers=self._headers())
        )

    def _headers(self):
        token = self.generate_application_jwt()
        return dict(self.headers, Authorization=b"Bearer " + token)

    def generate_application_jwt(self, when=None):
        iat = int(when if when is not None else time.time())

        payload = dict(self.auth_params)
        payload.setdefault("application_id", self.application_id)
        payload.setdefault("iat", iat)
        payload.setdefault("exp", iat + 60)
        payload.setdefault("jti", str(uuid4()))

        token = jwt.encode(payload, self.private_key, algorithm="RS256")

        # If token is string transform it to byte type
        if(type(token) is str):
            token = bytes(token, 'utf-8')

        return token

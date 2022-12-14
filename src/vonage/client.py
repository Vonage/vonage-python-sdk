import vonage

from .account import Account
from .application import ApplicationV2, Application
from .errors import *
from .messages import Messages
from .number_insight import NumberInsight
from .numbers import Numbers
from .redact import Redact
from .short_codes import ShortCodes
from .sms import Sms
from .ussd import Ussd
from .video import Video
from .voice import Voice
from .verify import Verify

import logging
from platform import python_version

import base64
import hashlib
import hmac
import jwt
import os
import time
import re
from uuid import uuid4

from requests.adapters import HTTPAdapter
from requests.sessions import Session

string_types = (str, bytes)

try:
    from json import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

logger = logging.getLogger("vonage")

class Client:
    """
    Create a Client object to start making calls to Vonage/Nexmo APIs.

    The credentials you provide when instantiating a Client determine which
    methods can be called. Consult the `Vonage API docs <https://developer.vonage.com/concepts/guides/authentication/>`
    for details of the authentication used by the APIs you wish to use, and instantiate your
    client with the appropriate credentials.

    :param str key: Your Vonage API key
    :param str secret: Your Vonage API secret.
    :param str signature_secret: Your Vonage API signature secret.
        You may need to have this enabled by Vonage support. It is only used for SMS authentication.
    :param str signature_method:
        The encryption method used for signature encryption. This must match the method
        configured in the Vonage Dashboard. We recommend `sha256` or `sha512`.
        This should be one of `md5`, `sha1`, `sha256`, or `sha512` if using HMAC digests.
        If you want to use a simple MD5 hash, leave this as `None`.
    :param str application_id: Your application ID if calling methods which use JWT authentication.
    :param str private_key: Your private key, for calling methods which use JWT authentication.
        This should either be a str containing the key in its PEM form, or a path to a private key file.
    :param str app_name: This optional value is added to the user-agent header
        provided by this library and can be used to track your app statistics.
    :param str app_version: This optional value is added to the user-agent header
        provided by this library and can be used to track your app statistics.
    :param timeout: (optional) How many seconds to wait for the server to send data
        before giving up, as a float, or a (connect timeout, read
        timeout) tuple. If set this timeout is used for every call to the Vonage enpoints
    :type timeout: float or tuple
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
        timeout=None, 
        pool_connections=10, 
        pool_maxsize=10, 
        max_retries=3
    ):
        self.api_key = key or os.environ.get("VONAGE_API_KEY", None)
        self.api_secret = secret or os.environ.get("VONAGE_API_SECRET", None)

        self.signature_secret = signature_secret or os.environ.get("VONAGE_SIGNATURE_SECRET", None)
        self.signature_method = signature_method or os.environ.get("VONAGE_SIGNATURE_METHOD", None)

        if self.signature_method in {"md5", "sha1", "sha256", "sha512"}:
            self.signature_method = getattr(hashlib, signature_method)

        self._jwt_auth_params = {}

        if private_key is not None and application_id is not None:
            self.application_id = application_id
            self._private_key = private_key

            if isinstance(self._private_key, string_types) and re.search("[.][a-zA-Z0-9_]+$", self._private_key):
                with open(self._private_key, "rb") as key_file:
                    self._private_key = key_file.read()

        self._host = "rest.nexmo.com"
        self._api_host = "api.nexmo.com"
        self._video_host = "video.api.vonage.com"

        user_agent = f"vonage-python/{vonage.__version__} python/{python_version()}"

        if app_name and app_version:
            user_agent += f" {app_name}/{app_version}"

        self.headers = {"User-Agent": user_agent, "Accept": "application/json"}

        self.account = Account(self)
        self.application = Application(self)
        self.messages = Messages(self)
        self.number_insight = NumberInsight(self)
        self.numbers = Numbers(self)
        self.short_codes = ShortCodes(self)
        self.sms = Sms(self)
        self.ussd = Ussd(self)
        self.video = Video(self)
        self.verify = Verify(self)
        self.voice = Voice(self)

        self.timeout = timeout
        self.session = Session()
        self.adapter = HTTPAdapter(
            pool_connections=pool_connections, 
            pool_maxsize=pool_maxsize, 
            max_retries=max_retries
        )
        self.session.mount("https://", self.adapter)

    # Get and Set _host attribute
    def host(self, value=None):
        if value is None:
            return self._host
        else:
            self._host = value

    # Gets And Set _api_host attribute
    def api_host(self, value=None):
        if value is None:
            return self._api_host
        else:
            self._api_host = value

    def video_host(self, value=None):
        if value is None:
            return self._video_host
        else:
            self._video_host = value

    def auth(self, params=None, **kwargs):
        self._jwt_auth_params = params or kwargs

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

            hasher.update(f"&{key}={value}".encode("utf-8"))

        if self.signature_method is None:
            hasher.update(self.signature_secret.encode())

        return hasher.hexdigest()

    def get(self, host, request_uri, params=None, auth_type=None):
        uri = f"https://{host}{request_uri}"
        self._request_headers = self.headers

        if auth_type == 'jwt':
            self._request_headers = self._add_jwt_to_request_headers()
        elif auth_type == 'params':
            params = dict(
                params or {}, api_key=self.api_key, api_secret=self.api_secret
            )
        elif auth_type == 'header':
            hash = base64.b64encode(
                f"{self.api_key}:{self.api_secret}".encode("utf-8")
            ).decode("ascii")
            self._request_headers = dict(self.headers or {}, Authorization=f"Basic {hash}")
        else:
            raise InvalidAuthenticationTypeError(
                f'Invalid authentication type. Must be one of "jwt", "header" or "params".'
            )

        logger.debug(f"GET to {repr(uri)} with params {repr(params)}, headers {repr(self._request_headers)}")
        return self.parse(
            host, 
            self.session.get(uri, params=params, headers=self._request_headers, timeout=self.timeout))

    def post(self, host, request_uri, params, auth_type=None, body_is_json=True, supports_signature_auth=False):
        """
        Low-level method to make a post request to an API server.
        This method automatically adds authentication, picking the first applicable authentication method from the following:
        - If the supports_signature_auth param is True, and the client was instantiated with a signature_secret, 
            then signature authentication will be used.
        :param bool supports_signature_auth: Preferentially use signature authentication if a signature_secret was provided 
            when initializing this client.
        """
        uri = f"https://{host}{request_uri}"
        self._request_headers = self.headers
        
        if supports_signature_auth and self.signature_secret:
            params["api_key"] = self.api_key
            params["sig"] = self.signature(params)
        elif auth_type == 'jwt':
            self._request_headers = self._add_jwt_to_request_headers()
        elif auth_type == 'params':
            params = dict(
                params, api_key=self.api_key, api_secret=self.api_secret
            )
        elif auth_type == 'header':
            hash = base64.b64encode(
                f"{self.api_key}:{self.api_secret}".encode("utf-8")
            ).decode("ascii")
            self._request_headers = dict(self.headers or {}, Authorization=f"Basic {hash}")
        else:
            raise InvalidAuthenticationTypeError(
                f'Invalid authentication type. Must be one of "jwt", "header" or "params".'
            )
        
        logger.debug(f"POST to {repr(uri)} with params {repr(params)}, headers {repr(self._request_headers)}")
        if body_is_json:
            return self.parse(
                host, self.session.post(uri, json=params, headers=self._request_headers, timeout=self.timeout))
        else:
            return self.parse(
                host, self.session.post(uri, data=params, headers=self._request_headers, timeout=self.timeout))

    def put(self, host, request_uri, params, auth_type=None):
        uri = f"https://{host}{request_uri}"
        self._request_headers = self.headers

        if auth_type == 'jwt':
            self._request_headers = self._add_jwt_to_request_headers()
        elif auth_type == 'header':
            hash = base64.b64encode(
                f"{self.api_key}:{self.api_secret}".encode("utf-8")
            ).decode("ascii")
            self._request_headers = dict(self._request_headers or {}, Authorization=f"Basic {hash}")
        else:
            raise InvalidAuthenticationTypeError(
                f'Invalid authentication type. Must be one of "jwt" or "header".'
            )

        logger.debug(f"PUT to {repr(uri)} with params {repr(params)}, headers {repr(self._request_headers)}")
        # All APIs that currently use put methods require a json-formatted body so don't need to check this
        return self.parse(host, self.session.put(uri, json=params, headers=self._request_headers, timeout=self.timeout))

    def patch(self, host, request_uri, params, auth_type='jwt'):
        uri = f"https://{host}{request_uri}"
        self._request_headers = self.headers

        if auth_type == 'jwt':
            self._request_headers = self._add_jwt_to_request_headers()
        else:
            raise InvalidAuthenticationTypeError(
                f"""Invalid authentication type. Must be "jwt", as only the Video API 
                    (which uses jwt auth) currently uses this method."""
            )

        logger.debug(f"PATCH to {repr(uri)} with params {repr(params)}, headers {repr(self._request_headers)}")
        # Only the Video API currently uses this method, so we will always send a json-formatted body
        return self.parse(host, self.session.patch(uri, json=params, headers=self._request_headers))

    def delete(self, host, request_uri, auth_type=None):
        uri = f"https://{host}{request_uri}"
        self._request_headers = self.headers

        if auth_type == 'jwt':
            self._request_headers = self._add_jwt_to_request_headers()
        elif auth_type =='header':
            hash = base64.b64encode(
                f"{self.api_key}:{self.api_secret}".encode("utf-8")
            ).decode("ascii")
            self._request_headers = dict(self._request_headers or {}, Authorization=f"Basic {hash}")
        else:
            raise InvalidAuthenticationTypeError(
                f'Invalid authentication type. Must be one of "jwt", "header" or "params".'
            )

        logger.debug(f"DELETE to {repr(uri)} with headers {repr(self._request_headers)}")
        return self.parse(
            host, self.session.delete(uri, headers=self._request_headers, timeout=self.timeout)
        )

    def parse(self, host, response):
        logger.debug(f"Response headers {repr(response.headers)}")
        if response.status_code == 401:
            raise AuthenticationError(
                "Authentication failed. Check you're using a valid authentication method."
            )
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
                f"Client error: {response.status_code} {repr(response.content)}"
            )
            message = f"{response.status_code} response from {host}"

            # Test for standard error format:
            try:
                error_data = response.json()
                if (
                    "type" in error_data
                    and "title" in error_data
                    and "detail" in error_data
                ):
                    title=error_data["title"]
                    detail=error_data["detail"]
                    type=error_data["type"]
                    message = f"{title}: {detail} ({type})"

            except JSONDecodeError:
                pass
            raise ClientError(message)
        elif 500 <= response.status_code < 600:
            logger.warning(f"Server error: {response.status_code} {repr(response.content)}")
            message = f"{response.status_code} response from {host}"
            raise ServerError(message)

    def _add_jwt_to_request_headers(self):
        return dict(self.headers, Authorization=b"Bearer " + self._generate_application_jwt())

    def _generate_application_jwt(self):
        iat = int(time.time())

        payload = dict(self._jwt_auth_params)
        payload.setdefault("application_id", self.application_id)
        payload.setdefault("iat", iat)
        payload.setdefault("exp", iat + 60)
        payload.setdefault("jti", str(uuid4()))

        token = jwt.encode(payload, self._private_key, algorithm="RS256")

        # If token is string transform it to byte type
        if(type(token) is str):
            token = bytes(token, 'utf-8')

        return token

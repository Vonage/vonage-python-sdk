import vonage

from ._internal import _format_date_param
from .account import Account
from .application import ApplicationV2, BasicAuthenticatedServer
from .errors import *
from .messages import Messages
from .number_insight import NumberInsight
from .numbers import Numbers
from .short_codes import ShortCodes
from .sms import Sms
from .ussd import Ussd
from .voice import Voice
from .verify import Verify

import logging
from datetime import datetime
from platform import python_version

import base64
import hashlib
import hmac
import jwt
import os
import pytz
import requests
import time
from uuid import uuid4
import warnings 
import re
from deprecated import deprecated


string_types = (str, bytes)

try:
    from json import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

logger = logging.getLogger("vonage")

class Client:
    """
    Create a Client object to start making calls to Vonage/Nexmo APIs.

    Note on deprecations: most public-facing APIs that are called directly from this class (e.g. voice, 
    sms, number insight) have been deprecated and will instead be called from modules that house 
    the relevant classes (e.g. `voice.py`, `sms.py`). Change your code to call these classes directly
    as they will be removed in a later release!
    
    Newer APIs are under namespaces like :attr:`Client.application_v2`.

    The credentials you provide when instantiating a Client determine which
    methods can be called. Consult the `Vonage API docs <https://developer.vonage.com/api/>`_ for details of the
    authentication used by the APIs you wish to use, and instantiate your
    Client with the appropriate credentials.

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
    :param str private_key: Your private key if calling methods which use JWT authentication.
        This should either be a str containing the key in its PEM form, or a path to a private key file.
    :param str app_name: This optional value is added to the user-agent header
        provided by this library and can be used by Vonage to track your app statistics.
    :param str app_version: This optional value is added to the user-agent header
        provided by this library and can be used by Vonage to track your app statistics.
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

        self.__host_pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$|^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)+([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$"

        self.__host = "rest.nexmo.com"

        self.__api_host = "api.nexmo.com"

        user_agent = f"vonage-python/{vonage.__version__} python/{python_version()}"

        if app_name and app_version:
            user_agent += f" {app_name}/{app_version}"

        self.headers = {"User-Agent": user_agent, "Accept": "application/json"}

        self.auth_params = {}

        api_server = BasicAuthenticatedServer(
            "https://api.nexmo.com",
            user_agent=user_agent,
            api_key=self.api_key,
            api_secret=self.api_secret,
        )
        self.application_v2 = ApplicationV2(api_server)
        
        self.account = Account(self)
        self.messages = Messages(self)
        self.number_insight = NumberInsight(self)
        self.numbers = Numbers(self)
        self.short_codes = ShortCodes(self)
        self.sms = Sms(self)
        self.ussd = Ussd(self)
        self.verify = Verify(self)
        self.voice = Voice(self)

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

    def redact_transaction(self, id, product, type=None):
        params = {"id": id, "product": product}
        if type is not None:
            params["type"] = type
        return self._post_json(self.api_host(), "/v1/redact/transaction", params)

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

    def get(self, host, request_uri, params=None, header_auth=False):
        uri = f"https://{host}{request_uri}"
        headers = self.headers
        if header_auth:
            hash = base64.b64encode(
                f"{self.api_key}:{self.api_secret}".encode("utf-8")
            ).decode("ascii")
            headers = dict(headers or {}, Authorization=f"Basic {hash}")
        else:
            params = dict(
                params or {}, api_key=self.api_key, api_secret=self.api_secret
            )
        logger.debug(f"GET to {repr(uri)} with params {repr(params)}, headers {repr(headers)}")
        return self.parse(host, self.session.get(uri, params=params, headers=headers))

    def post(
        self,
        host,
        request_uri,
        params,
        supports_signature_auth=False,
        header_auth=False,
        additional_headers=None
    ):
        """
        Low-level method to make a post request to a Vonage API server, which may have a Nexmo url.
        This method automatically adds authentication, picking the first applicable authentication method from the following:
        - If the supports_signature_auth param is True, and the client was instantiated with a signature_secret, then signature authentication will be used.
        - If the header_auth param is True, then basic authentication will be used, with the client's key and secret.
        - Otherwise the client's key and secret are appended to the post request's params.
        :param bool supports_signature_auth: Preferentially use signature authentication if a signature_secret was provided when initializing this client.
        :param bool header_auth: Use basic authentication instead of adding api_key and api_secret to the request params.
        """
        uri = f"https://{host}{request_uri}"
        
        if not additional_headers:
            headers = {**self.headers}
        else:
            headers = {**self.headers, **additional_headers}

        if supports_signature_auth and self.signature_secret:
            params["api_key"] = self.api_key
            params["sig"] = self.signature(params)
        elif header_auth:
            hash = base64.b64encode(
                f"{self.api_key}:{self.api_secret}".encode("utf-8")
            ).decode("ascii")
            headers = dict(headers or {}, Authorization=f"Basic {hash}")
        else:
            params = dict(params, api_key=self.api_key, api_secret=self.api_secret)
        logger.debug(
            f"POST to {repr(uri)} with params {repr(params)}, headers {repr(headers)}"
        )
        return self.parse(host, self.session.post(uri, data=params, headers=headers))

    def _post_json(self, host, request_uri, json):
        """
        Post json to `request_uri`, using basic auth.
        """
        uri = f"https://{host}{request_uri}"
        auth = base64.b64encode(
            f"{self.api_key}:{self.api_secret}".encode("utf-8")
        ).decode("ascii")
        headers = dict(
            self.headers or {}, Authorization=f"Basic {auth}"
        )
        logger.debug(
            f"POST to %{repr(request_uri)} with body: {repr(json)}, headers: {repr(headers)}"
        )
        return self.parse(host, self.session.post(uri, headers=headers, json=json))

    def put(self, host, request_uri, params, header_auth=False):
        uri = f"https://{host}{request_uri}"

        headers = self.headers
        if header_auth:
            hash = base64.b64encode(
                f"{self.api_key}:{self.api_secret}".encode("utf-8")
            ).decode("ascii")
            # Must create a new headers dict here, otherwise we'd be mutating `self.headers`:
            headers = dict(headers or {}, Authorization=f"Basic {hash}")
        else:
            params = dict(params, api_key=self.api_key, api_secret=self.api_secret)
        logger.debug(f"PUT to {repr(uri)} with params {repr(params)}, headers {repr(headers)}")
        return self.parse(host, self.session.put(uri, json=params, headers=headers))

    def delete(self, host, request_uri, header_auth=False):
        uri = f"https://{host}{request_uri}"

        params = None
        headers = self.headers
        if header_auth:
            hash = base64.b64encode(
                f"{self.api_key}:{self.api_secret}".encode("utf-8")
            ).decode("ascii")
            # Must create a new headers dict here, otherwise we'd be mutating `self.headers`:
            headers = dict(headers or {}, Authorization=f"Basic {hash}")
        else:
            params = {"api_key": self.api_key, "api_secret": self.api_secret}
        logger.debug(f"DELETE to {repr(uri)} with params {repr(params)}, headers {repr(headers)}")
        return self.parse(
            host, self.session.delete(uri, params=params, headers=headers)
        )

    def parse(self, host, response):
        logger.debug(f"Response headers {repr(response.headers)}")
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

    def _jwt_signed_get(self, request_uri, params=None):
        uri = f"https://{self.api_host()}{request_uri}"

        return self.parse(
            self.api_host(),
            self.session.get(uri, params=params or {}, headers=self._headers()),
        )

    def _jwt_signed_post(self, request_uri, params):
        uri = f"https://{self.api_host()}{request_uri}"

        return self.parse(
            self.api_host(),
            self.session.post(uri, json=params, headers=self._headers()),
        )

    def _jwt_signed_put(self, request_uri, params):
        uri = f"https://{self.api_host()}{request_uri}"

        return self.parse(
            self.api_host(), self.session.put(uri, json=params, headers=self._headers())
        )

    def _jwt_signed_delete(self, request_uri):
        uri = f"https://{self.api_host()}{request_uri}"

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

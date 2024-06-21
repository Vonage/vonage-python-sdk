from typing import Optional

from vonage_application.application import Application
from vonage_http_client import Auth, HttpClient, HttpClientOptions
from vonage_messages import Messages
from vonage_number_insight import NumberInsight
from vonage_sms import Sms
from vonage_users import Users
from vonage_verify import Verify
from vonage_verify_v2 import VerifyV2
from vonage_voice import Voice

from ._version import __version__


class Vonage:
    """Main Server SDK class for using Vonage APIs.

    When creating an instance, it will create the authentication objects and
    an HTTP Client needed for using Vonage APIs.
    Use an instance of this class to access the Vonage APIs, e.g. to access
    methods associated with the Vonage SMS API, call `vonage.sms.method_name()`.

    Args:
        auth (Auth): Class dealing with authentication objects and methods.
        http_client_options (HttpClientOptions, optional): Options for the HTTP client.
    """

    def __init__(
        self, auth: Auth, http_client_options: Optional[HttpClientOptions] = None
    ):
        self._http_client = HttpClient(auth, http_client_options, __version__)

        self.application = Application(self._http_client)
        self.messages = Messages(self._http_client)
        self.number_insight = NumberInsight(self._http_client)
        self.sms = Sms(self._http_client)
        self.users = Users(self._http_client)
        self.verify = Verify(self._http_client)
        self.verify_v2 = VerifyV2(self._http_client)
        self.voice = Voice(self._http_client)

    @property
    def http_client(self):
        return self._http_client

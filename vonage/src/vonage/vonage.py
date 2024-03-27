from typing import Optional

from vonage_http_client.auth import Auth
from vonage_http_client.http_client import HttpClient, HttpClientOptions
from vonage_number_insight_v2.number_insight_v2 import NumberInsightV2
from vonage_sms.sms import Sms
from vonage_users.users import Users

from ._version import __version__


class Vonage:
    """Main Server SDK class for using Vonage APIs.

    Args:
        auth (Auth): Class dealing with authentication objects and methods.
        http_client_options (HttpClientOptions, optional): Options for the HTTP client.
    """

    def __init__(
        self, auth: Auth, http_client_options: Optional[HttpClientOptions] = None
    ):
        self._http_client = HttpClient(auth, http_client_options, __version__)

        self.number_insight_v2 = NumberInsightV2(self._http_client)
        self.sms = Sms(self._http_client)
        self.users = Users(self._http_client)

    @property
    def http_client(self):
        return self._http_client

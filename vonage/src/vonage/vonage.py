from typing import Optional

from http_client.auth import Auth

from http_client.http_client import HttpClient, HttpClientOptions
from number_insight_v2.number_insight_v2 import NumberInsightv2


class Vonage:
    """Main Server SDK class for using Vonage APIs.

    Args:
        auth (Auth): Class dealing with authentication objects and methods.
        http_client_options (HttpClientOptions, optional): Options for the HTTP client.
    """

    def __init__(
        self, auth: Auth, http_client_options: Optional[HttpClientOptions] = None
    ):
        self._http_client = HttpClient(auth, http_client_options)

        self.number_insight_v2 = NumberInsightv2(self._http_client)

    @property
    def http_client(self):
        return self._http_client
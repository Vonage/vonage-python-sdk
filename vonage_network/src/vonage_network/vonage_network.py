from platform import python_version
from typing import Optional

from vonage_http_client import Auth, HttpClient, HttpClientOptions
from vonage_network_sim_swap import NetworkSimSwap

from ._version import __version__


class VonageNetwork:
    """Main Server SDK class for using Vonage Network APIs.

    When creating an instance, it will create the authentication objects and
    an HTTP Client needed for using Vonage Network APIs.

    Use an instance of this class to access the Vonage Network APIs, e.g. to access
    methods associated with the Vonage Sim Swap API, call `vonage_network.sim_swap.method_name()`.

    Args:
        auth (Auth): Class dealing with authentication objects and methods.
        http_client_options (HttpClientOptions, optional): Options for the HTTP client.
    """

    def __init__(
        self, auth: Auth, http_client_options: Optional[HttpClientOptions] = None
    ):
        self._http_client = HttpClient(auth, http_client_options, __version__)
        self._http_client._user_agent = (
            f'vonage-network-python-sdk/{__version__} python/{python_version()}'
        )

        self.sim_swap = NetworkSimSwap(self._http_client)

    @property
    def http_client(self):
        return self._http_client

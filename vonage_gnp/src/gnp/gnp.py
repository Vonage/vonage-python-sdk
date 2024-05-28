from typing import Optional

from vonage_http_client import Auth, HttpClient, HttpClientOptions

from gnp_sim_swap import SimSwap

from ._version import __version__


class VonageGnp:
    """Main Server SDK class for using Vonage GNP APIs.

    When creating an instance, it will create the authentication objects and
    an HTTP Client needed for using Vonage APIs.
    Use an instance of this class to access the Vonage GNP APIs, e.g. to access
    methods associated with the Vonage Sim Swap API, call `vonage_gnp.sim_swap.method_name()`.

    Args:
        auth (Auth): Class dealing with authentication objects and methods.
        http_client_options (HttpClientOptions, optional): Options for the HTTP client.
    """

    def __init__(
        self, auth: Auth, http_client_options: Optional[HttpClientOptions] = None
    ):
        self._http_client = HttpClient(auth, http_client_options, __version__)

        self.sim_swap = SimSwap()

    @property
    def http_client(self):
        return self._http_client

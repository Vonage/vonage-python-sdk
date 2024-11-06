from pydantic import validate_call
from vonage_http_client import HttpClient
from vonage_network_auth import NetworkAuth
from vonage_network_sim_swap.requests import SimSwapCheckRequest

from .responses import LastSwapDate, SwapStatus


class NetworkSimSwap:
    """Class containing methods for working with the Vonage SIM Swap Network API."""

    def __init__(self, http_client: HttpClient):
        self._http_client = http_client
        self._host = 'api-eu.vonage.com'

        self._auth_type = 'oauth2'
        self._network_auth = NetworkAuth(self._http_client)

    @property
    def http_client(self) -> HttpClient:
        """The HTTP client used to make requests to the Network Sim Swap API.

        Returns:
            HttpClient: The HTTP client used to make requests to the Network Sim Swap API.
        """
        return self._http_client

    @validate_call
    def check(self, sim_swap_request: SimSwapCheckRequest) -> SwapStatus:
        """Check if a SIM swap has been performed in a given time frame.

        Args:
            sim_swap_request (SimSwapCheckRequest): The request model to check if a SIM
                has been swapped.

        Returns:
            SwapStatus: Class containing the Swap Status response.
        """
        token = self._network_auth.get_sim_swap_camara_token(
            number=sim_swap_request.phone_number,
            scope='dpv:FraudPreventionAndDetection#check-sim-swap',
        )

        return self._http_client.post(
            self._host,
            '/camara/sim-swap/v040/check',
            params=sim_swap_request.model_dump(by_alias=True, exclude_none=True),
            auth_type=self._auth_type,
            token=token,
        )

    @validate_call
    def get_last_swap_date(self, phone_number: str) -> LastSwapDate:
        """Get the last SIM swap date for a phone number.

        Args:
            phone_number (str): The phone number to check. Use the E.164 format with
                or without a leading +.

        Returns:
            LastSwapDate: Class containing the Last Swap Date response.
        """
        token = self._network_auth.get_sim_swap_camara_token(
            number=phone_number,
            scope='dpv:FraudPreventionAndDetection#retrieve-sim-swap-date',
        )
        return self._http_client.post(
            self._host,
            '/camara/sim-swap/v040/retrieve-date',
            params={'phoneNumber': phone_number},
            auth_type=self._auth_type,
            token=token,
        )

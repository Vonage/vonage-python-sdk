from pydantic import validate_call
from vonage_camara_auth import CamaraAuth
from vonage_http_client import HttpClient
from vonage_utils.types import PhoneNumber

from .responses import LastSwapDate, SwapStatus


class SimSwap:
    """Class containing methods for working with the Vonage SIM Swap API."""

    def __init__(self, http_client: HttpClient):
        self._http_client = http_client
        self._host = 'api-eu.vonage.com'

        self._auth_type = 'oauth2'
        self._camara_auth = CamaraAuth(self._http_client)

    @validate_call
    def check(self, phone_number: PhoneNumber, max_age: int = None) -> SwapStatus:
        """Check if a SIM swap has been performed in a given time frame.

        Args:
            phone_number (str): The phone number to check. Use the E.164 format without a leading +.
            max_age (int, optional): Period in hours to be checked for SIM swap.

        Returns:

        """
        token = self._camara_auth.get_oauth2_user_token(
            number=phone_number, scope='dpv:FraudPreventionAndDetection#check-sim-swap'
        )

        return self._http_client.post(
            self._host,
            '/camara/sim-swap/v040/check',
            params={'phoneNumber': phone_number, 'maxAge': max_age},
            auth_type=self._auth_type,
            oauth_token=token,
        )

    @validate_call
    def get_last_swap_date(self, phone_number: PhoneNumber) -> LastSwapDate:
        """Get the last SIM swap date for a phone number.

        Args:
            phone_number (str): The phone number to check. Use the E.164 format without a leading +.

        Returns:

        """
        token = self._camara_auth.get_oauth2_user_token(
            number=phone_number,
            scope='dpv:FraudPreventionAndDetection#retrieve-sim-swap-date',
        )
        return self._http_client.post(
            self._host,
            '/camara/sim-swap/v040/retrieve-date',
            params={'phoneNumber': phone_number},
            auth_type=self._auth_type,
            oauth_token=token,
        )

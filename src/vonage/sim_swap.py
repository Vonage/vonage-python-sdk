from __future__ import annotations
from typing import TYPE_CHECKING

from .camara_auth import CamaraAuth

if TYPE_CHECKING:
    from vonage import Client


class SimSwap:
    """Class containing methods for working with the Vonage SIM Swap API."""

    def __init__(self, client: Client):
        self._client = client
        self._auth_type = 'oauth2'
        self._camara_auth = CamaraAuth(client)

    def check(self, phone_number: str, max_age: int = None):
        """Check if a SIM swap has been performed in a given time frame.

        Args:
            phone_number (str): The phone number to check. Use the E.164 format without a leading +.
            max_age (int, optional): Period in hours to be checked for SIM swap.

        Returns:
            The response from the API as a dict.
        """
        oicd_response = self._camara_auth.make_oidc_request(
            number=phone_number, scope='dpv:FraudPreventionAndDetection#check-sim-swap'
        )
        token = self._camara_auth.request_backend_camara_token(oicd_response)

        params = {'phoneNumber': phone_number}
        if max_age:
            params['maxAge'] = max_age

        return self._client.post(
            'api-eu.vonage.com',
            '/camara/sim-swap/v040/check',
            params=params,
            auth_type=self._auth_type,
            oauth_token=token,
        )

    def get_last_swap_date(self, phone_number: str):
        """Get the last SIM swap date for a phone number.

        Args:
            phone_number (str): The phone number to check. Use the E.164 format without a leading +.

        Returns:
            The response from the API as a dict.
        """
        oicd_response = self._camara_auth.make_oidc_request(
            number=phone_number,
            scope='dpv:FraudPreventionAndDetection#retrieve-sim-swap-date',
        )
        token = self._camara_auth.request_backend_camara_token(oicd_response)
        return self._client.post(
            'api-eu.vonage.com',
            '/camara/sim-swap/v040/retrieve-date',
            params={'phoneNumber': phone_number},
            auth_type=self._auth_type,
            oauth_token=token,
        )

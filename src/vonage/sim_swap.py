from __future__ import annotations
from typing import TYPE_CHECKING

from .errors import SimSwapError

if TYPE_CHECKING:
    from vonage import Client


class SimSwap:
    """Class containing methods for working with the Vonage SIM Swap API."""

    def __init__(self, client: Client):
        self._client = client
        self._auth_type = ''

    def check(self, phone_number: str, max_age: int):
        """Check if a SIM swap has been performed in a given time frame.

        Args:
            phone_number: The phone number to check.
            max_age: The maximum age of the check in hours.

        Returns:
            The response from the API as a dict.
        """
        return self._client.post(
            'api-eu.vonage.com',
            '/camara/sim-swap/v040/check',
            params={'phoneNumber': phone_number, 'maxAge': max_age},
            auth_type=self._auth_type,
        )

    def get_last_swap_date(self, phone_number: str):
        """Get the last SIM swap date for a phone number.

        Args:
            phone_number: The phone number to check.

        Returns:
            The response from the API as a dict.
        """
        return self._client.get(
            'api-eu.vonage.com',
            '/camara/sim-swap/v040/retrieve-date',
            params={'phoneNumber': phone_number},
            auth_type=self._auth_type,
        )

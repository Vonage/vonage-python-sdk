from __future__ import annotations
from typing import TYPE_CHECKING

from .errors import NumberVerificationError

if TYPE_CHECKING:
    from vonage import Client


class NumberVerification:
    """Class containing methods for working with the Vonage SIM Swap API."""

    def __init__(self, client: Client):
        self._client = client
        self._auth_type = ''

    def verify_number(self, number: str):
        """Verifies if the specified phone number (plain text or hashed format) matches the one that the user is currently using.

        Args:
            number: The phone number to verify, either in plain text or as a SDK-256 hash of the phone number in E.164 format.

        Returns:
            The response from the API as a dict.
        """
        if len(number) == 64:
            params = {'hashedPhoneNumber': number}
        else:
            params = {'phoneNumber': number}

        return self._client.post(
            'api-eu.vonage.com',
            '/camara/number-verification/v040/verify',
            params=params,
            auth_type=self._auth_type,
        )

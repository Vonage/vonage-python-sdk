from __future__ import annotations
from typing import TYPE_CHECKING

from vonage.errors import NumberVerificationError

from .camara_auth import CamaraAuth

if TYPE_CHECKING:
    from vonage import Client


class NumberVerification:
    """Class containing methods for working with the Vonage Number Verification API."""

    def __init__(self, client: Client):
        self._client = client
        self._auth_type = 'oauth2'
        self._camara_auth = CamaraAuth(client)
        self._nvtoken = None

    def get_oidc_url(
        self,
        redirect_uri: str,
        state: str = None,
        login_hint: str = None,
        scope: str = 'openid dpv:FraudPreventionAndDetection#number-verification-verify-read',
    ):
        """Get the URL to use for authentication in a front-end application.

        Args:
            redirect_uri (str): The URI to redirect to after authentication.
            scope (str): The scope of the request.
            state (str): A unique identifier for the request. Can be any string.
            login_hint (str): The phone number to use for the request.

        Returns:
            The URL to use to make an OIDC request in a front-end application.
        """
        return self._camara_auth.get_oidc_url(
            redirect_uri=redirect_uri,
            scope=scope,
            state=state,
            login_hint=login_hint,
        )

    def exchange_code_for_token(self, code: str, redirect_uri: str) -> str:
        return self._camara_auth.request_frontend_camara_token(code, redirect_uri)

    def verify(self, access_token: str, phone_number: str = None, hashed_phone_number: str = None):
        """Verify a phone number using the Number Verification API."""

        if phone_number and hashed_phone_number:
            raise NumberVerificationError(
                'Only one of "phone_number" and "hashed_phone_number" can be provided.'
            )
        if phone_number:
            params = {'phoneNumber': phone_number}
        elif hashed_phone_number:
            params = {'hashedPhoneNumber': hashed_phone_number}

        return self._client.post(
            'api-eu.vonage.com',
            '/camara/number-verification/v031/verify',
            params=params,
            auth_type=self._auth_type,
            oauth_token=access_token,
        )

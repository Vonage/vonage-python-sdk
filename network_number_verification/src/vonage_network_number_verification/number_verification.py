from urllib.parse import urlencode, urlunparse

from pydantic import validate_call
from vonage_http_client import HttpClient
from vonage_network_auth import NetworkAuth
from vonage_network_number_verification.requests import CreateOidcUrl
from vonage_network_number_verification.responses import NumberVerificationResponse


class NetworkNumberVerification:
    """Class containing methods for working with the Vonage Number Verification Network
    API."""

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
    def get_oidc_url(self, url_settings: CreateOidcUrl) -> str:
        """Get the URL to use for authentication in a front-end application.

        Args:
            url_settings (CreateOidcUrl): The settings to use for the URL. Settings include:
                - redirect_uri (str): The URI to redirect to after authentication.
                - state (str, optional): A unique identifier for the request. Can be any string.
                - login_hint (str, optional): The phone number to use for the request.

        Returns:
            str: The URL to use to make an OIDC request in a front-end application.
        """
        base_url = 'https://oidc.idp.vonage.com/oauth2/auth'

        params = {
            'client_id': self._http_client.auth.application_id,
            'redirect_uri': url_settings.redirect_uri,
            'response_type': 'code',
            'scope': url_settings.scope,
        }
        if url_settings.state is not None:
            params['state'] = url_settings.state
        if url_settings.login_hint is not None:
            if url_settings.login_hint.startswith('+'):
                params['login_hint'] = url_settings.login_hint
            else:
                params['login_hint'] = f'+{url_settings.login_hint}'

        full_url = urlunparse(('', '', base_url, '', urlencode(params), ''))
        return full_url

    @validate_call
    def get_oidc_token(
        self, oidc_response: dict, grant_type: str = 'urn:openid:params:grant-type:ciba'
    ):
        """Request a Camara token using an authentication request ID given as a response
        to the OIDC request."""
        params = {
            'grant_type': grant_type,
            'auth_req_id': oidc_response['auth_req_id'],
        }
        return self._request_camara_token(params)

    @validate_call
    def verify(
        self, access_token: str, phone_number: str = None, hashed_phone_number: str = None
    ) -> NumberVerificationResponse:
        """Verify if the specified phone number matches the one that the user is currently
        using.

        Note: To use this method, the user must be connected to mobile data rather than
        Wi-Fi.

        Args:
            access_token (str): The access token to use for the request.
            phone_number (str, optional): The phone number to verify. Use the E.164 format with
                or without a leading +.
            hashed_phone_number (str, optional): The hashed phone number to verify.

        Returns:
            NumberVerificationResponse: Class containing the Number Verification response
                containing the device verification information.
        """
        return self._http_client.post(
            self._host,
            '/camara/number-verification/v031/verify',
            params={
                'phoneNumber': phone_number,
                'hashedPhoneNumber': hashed_phone_number,
            },
            auth_type=self._auth_type,
            token=access_token,
        )

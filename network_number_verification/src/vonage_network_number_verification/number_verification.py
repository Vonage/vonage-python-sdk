from pydantic import validate_call
from vonage_http_client import HttpClient
from vonage_network_auth import NetworkAuth
from vonage_network_auth.requests import CreateOidcUrl
from vonage_network_number_verification.requests import NumberVerificationRequest
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
        return self._network_auth.get_oidc_url(url_settings)

    @validate_call
    def exchange_code_for_token(self, code: str, redirect_uri: str) -> str:
        """Exchange an OIDC authorization code for a CAMARA access token.

        Args:
            code (str): The authorization code to use.
            redirect_uri (str): The URI to redirect to after authentication.

        Returns:
            str: The access token to use for further requests.
        """
        return self._network_auth.get_number_verification_camara_token(code, redirect_uri)

    @validate_call
    def verify(
        self, number_verification_params: NumberVerificationRequest
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
        params = {}
        if number_verification_params.phone_number is not None:
            params = {'phoneNumber': number_verification_params.phone_number}
        else:
            params = {'hashedPhoneNumber': number_verification_params.hashed_phone_number}

        response = self._http_client.post(
            self._host,
            '/camara/number-verification/v031/verify',
            params=params,
            auth_type=self._auth_type,
            token=number_verification_params.access_token,
        )

        return NumberVerificationResponse(**response)

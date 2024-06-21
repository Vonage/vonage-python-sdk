from pydantic import validate_call
from vonage_http_client.http_client import HttpClient

from .responses import OidcResponse, TokenResponse


class NetworkAuth:
    """Class containing methods for authenticating Network APIs following Camara standards."""

    def __init__(self, http_client: HttpClient):
        self._http_client = http_client
        self._host = 'api-eu.vonage.com'
        self._auth_type = 'jwt'
        self._sent_data_type = 'form'

    @property
    def http_client(self) -> HttpClient:
        """The HTTP client used to make requests to the Network Auth API.

        Returns:
            HttpClient: The HTTP client used to make requests to the Network Auth API.
        """
        return self._http_client

    @validate_call
    def get_oauth2_user_token(self, number: str, scope: str) -> str:
        """Get an OAuth2 user token for a given number and scope.

        Args:
            number (str): The phone number to authenticate.
            scope (str): The scope of the token.

        Returns:
            str: The OAuth2 user token.
        """
        oidc_response = self.make_oidc_request(number, scope)
        token_response = self.request_access_token(oidc_response.auth_req_id)
        return token_response.access_token

    @validate_call
    def make_oidc_request(self, number: str, scope: str) -> OidcResponse:
        """Make an OIDC request to authenticate a user.

        Args:
            number (str): The phone number to authenticate.
            scope (str): The scope of the token.

        Returns:
            OidcResponse: A response containing the authentication request ID.
        """
        number = self._ensure_plus_prefix(number)
        params = {'login_hint': number, 'scope': scope}

        response = self._http_client.post(
            self._host,
            '/oauth2/bc-authorize',
            params,
            self._auth_type,
            self._sent_data_type,
        )
        return OidcResponse(**response)

    @validate_call
    def request_access_token(
        self, auth_req_id: str, grant_type: str = 'urn:openid:params:grant-type:ciba'
    ) -> TokenResponse:
        """Request a Camara access token using an authentication request ID given as a response to
        an OIDC request."""
        params = {'auth_req_id': auth_req_id, 'grant_type': grant_type}

        response = self._http_client.post(
            self._host,
            '/oauth2/token',
            params,
            self._auth_type,
            self._sent_data_type,
        )
        return TokenResponse(**response)

    def _ensure_plus_prefix(self, number: str) -> str:
        """Ensure that the number has a plus prefix.

        Args:
            number (str): The phone number to check.

        Returns:
            str: The phone number with a plus prefix.
        """
        if number.startswith('+'):
            return number
        return f'+{number}'

from urllib.parse import urlencode, urlunparse

from pydantic import validate_call
from vonage_http_client.http_client import HttpClient
from vonage_network_auth.requests import CreateOidcUrl

from .responses import OidcResponse, TokenResponse


class NetworkAuth:
    """Class containing methods for authenticating Network APIs following CAMARA
    standards."""

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
    def get_oidc_url(self, url_settings: CreateOidcUrl) -> str:
        """Get the URL to use for authentication in a front-end application.

        Args:
            url_settings (CreateOidcUrl): The settings to use for the URL. Settings include:
                - redirect_uri (str): The URI to redirect to after authentication.
                - state (str): A unique identifier for the request. Can be any string.
                - login_hint (str): The phone number to use for the request.

        Returns:
            str: The URL to use to make an OIDC request in a front-end application.
        """
        base_url = 'https://oidc.idp.vonage.com/oauth2/auth'

        params = {
            'client_id': self._http_client.auth.application_id,
            'redirect_uri': url_settings.redirect_uri,
            'response_type': 'code',
            'scope': url_settings.scope,
            'state': url_settings.state,
            'login_hint': self._ensure_plus_prefix(url_settings.login_hint),
        }

        full_url = urlunparse(('', '', base_url, '', urlencode(params), ''))
        return full_url

    @validate_call
    def get_number_verification_camara_token(self, code: str, redirect_uri: str) -> str:
        """Exchange an OIDC authorization code for a CAMARA access token.

        Args:
            code (str): The authorization code to use.
            redirect_uri (str): The URI to redirect to after authentication.

        Returns:
            str: The access token to use for further requests.
        """
        params = {
            'code': code,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }
        return self._request_access_token(params).access_token

    @validate_call
    def get_sim_swap_camara_token(self, number: str, scope: str) -> str:
        """Get an OAuth2 user token for a given number and scope, to do a sim swap check.
        A CAMARA token is requested using the number and scope, and the token is returned.

        Args:
            number (str): The phone number to authenticate.
            scope (str): The scope of the token.

        Returns:
            str: The OAuth2 user token.
        """
        oidc_response = self.make_oidc_auth_id_request(number, scope)
        token_response = self.request_sim_swap_access_token(oidc_response.auth_req_id)
        return token_response.access_token

    @validate_call
    def make_oidc_auth_id_request(self, number: str, scope: str) -> OidcResponse:
        """Make an OIDC request for an authentication ID. The auth ID is then used to
        request a JWT. Returns a response containing the authentication request ID that
        can be used to generate an authorised JWT. Follows the Camara standard.

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
    def request_sim_swap_access_token(
        self, auth_req_id: str, grant_type: str = 'urn:openid:params:grant-type:ciba'
    ) -> TokenResponse:
        """Request a Camara access token for a SIM Swap check using an authentication
        request ID given as a response to an OIDC request.

        Args:
            auth_req_id (str): The authentication request ID.
            grant_type (str, optional): The grant type.

        Returns:
            TokenResponse: A response containing the access token.
        """
        params = {'auth_req_id': auth_req_id, 'grant_type': grant_type}

        return self._request_access_token(params)

    @validate_call
    def _request_access_token(self, params: dict) -> TokenResponse:
        """Request a Camara access token using an authentication request ID given as a
        response to an OIDC request.

        Args:
            auth_req_id (str): The authentication request ID.
            grant_type (str, optional): The grant type.

        Returns:
            TokenResponse: A response containing the access token.
        """
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

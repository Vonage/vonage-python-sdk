from pydantic import validate_call
from vonage_http_client.http_client import HttpClient
from .responses import OidcResponse, TokenResponse


class CamaraAuth:
    """Class containing methods for authenticating APIs following Camara standards."""

    def __init__(self, http_client: HttpClient):
        self._http_client = http_client
        self._host = 'api-eu.vonage.com'
        self._auth_type = 'jwt'
        self._sent_data_type = 'form'

    @property
    def http_client(self) -> HttpClient:
        """The HTTP client used to make requests to the Users API.

        Returns:
            HttpClient: The HTTP client used to make requests to the Users API.
        """
        return self._http_client

    @validate_call
    def get_oauth2_user_token(self, number: str, scope: str) -> str:
        oidc_response = self._make_oidc_request(number, scope)
        token_response = self._request_camara_token(oidc_response.auth_req_id)
        return token_response.access_token

    def _make_oidc_request(self, number: str, scope: str) -> OidcResponse:
        """Make an OIDC request to authenticate a user.

        Returns a code that can be used to request a Camara token."""

        login_hint = f'tel:+{number}'
        params = {'login_hint': login_hint, 'scope': scope}

        response = self._http_client.post(
            self._host,
            '/oauth2/bc-authorize',
            params,
            self._auth_type,
            self._sent_data_type,
        )
        return OidcResponse(**response)

    def _request_camara_token(
        self, auth_req_id: str, grant_type: str = 'urn:openid:params:grant-type:ciba'
    ) -> TokenResponse:
        """Request a Camara token using an authentication request ID given as a
        response to the OIDC request.
        """
        params = {'auth_req_id': auth_req_id, 'grant_type': grant_type}

        response = self._http_client.post(
            self._host,
            '/oauth2/token',
            params,
            self._auth_type,
            self._sent_data_type,
        )
        return TokenResponse(**response)

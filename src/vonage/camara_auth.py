from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vonage import Client


class CamaraAuth:
    """Class containing methods for authenticating APIs following Camara standards."""

    def __init__(self, client: Client):
        self._client = client
        self._auth_type = 'jwt'

    def make_oidc_request(self, number: str, scope: str):
        """Make an OIDC request to authenticate a user.

        Returns a code that can be used to request a Camara token."""

        login_hint = f'tel:+{number}'
        params = {'login_hint': login_hint, 'scope': scope}

        return self._client.post(
            'api-eu.vonage.com',
            '/oauth2/bc-authorize',
            params=params,
            auth_type=self._auth_type,
            body_is_json=False,
        )

    def request_camara_token(
        self, oidc_response: dict, grant_type: str = 'urn:openid:params:grant-type:ciba'
    ):
        """Request a Camara token using an authentication request ID given as a
        response to the OIDC request.
        """
        params = {
            'grant_type': grant_type,
            'auth_req_id': oidc_response['auth_req_id'],
        }

        token_response = self._client.post(
            'api-eu.vonage.com',
            '/oauth2/token',
            params=params,
            auth_type=self._auth_type,
            body_is_json=False,
        )
        return token_response['access_token']

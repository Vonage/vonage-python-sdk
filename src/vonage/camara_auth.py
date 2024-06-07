from __future__ import annotations
from typing import TYPE_CHECKING
from urllib.parse import urlencode, urlunparse


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
        base_url = 'https://oidc.idp.vonage.com/oauth2/auth'

        params = {
            'client_id': self._client.application_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': scope,
        }
        if state:
            params['state'] = state
        if login_hint:
            if login_hint.startswith('+'):
                params['login_hint'] = login_hint
            else:
                params['login_hint'] = f'+{login_hint}'

        full_url = urlunparse(('', '', base_url, '', urlencode(params), ''))
        return full_url

    def request_backend_camara_token(
        self, oidc_response: dict, grant_type: str = 'urn:openid:params:grant-type:ciba'
    ):
        """Request a Camara token using an authentication request ID given as a
        response to the OIDC request.
        """
        params = {
            'grant_type': grant_type,
            'auth_req_id': oidc_response['auth_req_id'],
        }
        return self._request_camara_token(params)

    def request_frontend_camara_token(self, code: str, redirect_uri: str):
        """Request a Camara token using a code from an OIDC response."""
        params = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
        }
        return self._request_camara_token(params)

    def _request_camara_token(self, params: dict):
        token_response = self._client.post(
            'api-eu.vonage.com',
            '/oauth2/token',
            params=params,
            auth_type=self._auth_type,
            body_is_json=False,
        )
        return token_response['access_token']

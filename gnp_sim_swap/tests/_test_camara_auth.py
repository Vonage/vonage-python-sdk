from os.path import abspath

import responses

from testutils import build_response, get_mock_jwt_auth
from vonage_camara_auth import CamaraAuth, camara_auth
from vonage_camara_auth.responses import OidcResponse
from vonage_http_client.http_client import HttpClient

path = abspath(__file__)


camara_auth = CamaraAuth(HttpClient(get_mock_jwt_auth()))


def test_http_client_property():
    http_client = camara_auth.http_client
    assert isinstance(http_client, HttpClient)


@responses.activate
def test_oidc_request():
    build_response(
        path,
        'POST',
        'https://api-eu.vonage.com/oauth2/bc-authorize',
        'oidc_request.json',
    )

    response = camara_auth._make_oidc_request(
        number='447700900000',
        scope='dpv:FraudPreventionAndDetection#check-sim-swap',
    )

    assert response.auth_req_id == '0dadaeb4-7c79-4d39-b4b0-5a6cc08bf537'
    assert response.expires_in == '120'
    assert response.interval == '2'


@responses.activate
def test_request_camara_access_token():
    build_response(
        path,
        'POST',
        'https://api-eu.vonage.com/oauth2/token',
        'token_request.json',
    )

    oidc_response_dict = {
        'auth_req_id': '0dadaeb4-7c79-4d39-b4b0-5a6cc08bf537',
        'expires_in': '120',
        'interval': '2',
    }
    oidc_response = OidcResponse(**oidc_response_dict)
    response = camara_auth._request_camara_token(oidc_response.auth_req_id)

    assert (
        response.access_token
        == 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZWZhdWx0IiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.3wWzV6t8bFJUZ6k0WJ9kY3J2kNw9v5zXJ8x1J5g1v2k'
    )
    assert response.token_type == 'A-VALID-TOKEN-TYPE'
    assert response.refresh_token == 'A-VALID-REFRESH-TOKEN'


@responses.activate
def test_whole_oauth2_flow():
    build_response(
        path,
        'POST',
        'https://api-eu.vonage.com/oauth2/bc-authorize',
        'oidc_request.json',
    )
    build_response(
        path,
        'POST',
        'https://api-eu.vonage.com/oauth2/token',
        'token_request.json',
    )

    access_token = camara_auth.get_oauth2_user_token(
        number='447700900000', scope='dpv:FraudPreventionAndDetection#check-sim-swap'
    )
    assert (
        access_token
        == 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZWZhdWx0IiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.3wWzV6t8bFJUZ6k0WJ9kY3J2kNw9v5zXJ8x1J5g1v2k'
    )

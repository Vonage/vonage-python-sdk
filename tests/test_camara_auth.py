from vonage.camara_auth import CamaraAuth
from util import *

import responses


@responses.activate
def test_oidc_request(camara_auth: CamaraAuth):
    stub(
        responses.POST,
        'https://api-eu.vonage.com/oauth2/bc-authorize',
        fixture_path='camara_auth/oidc_request.json',
    )

    response = camara_auth.make_oidc_request(
        number='447700900000',
        scope='dpv:FraudPreventionAndDetection#check-sim-swap',
    )

    assert response['auth_req_id'] == '0dadaeb4-7c79-4d39-b4b0-5a6cc08bf537'
    assert response['expires_in'] == '120'
    assert response['interval'] == '2'


@responses.activate
def test_request_camara_access_token(camara_auth: CamaraAuth):
    stub(
        responses.POST,
        'https://api-eu.vonage.com/oauth2/token',
        fixture_path='camara_auth/token_request.json',
    )

    oidc_response = {
        'auth_req_id': '0dadaeb4-7c79-4d39-b4b0-5a6cc08bf537',
        'expires_in': '120',
        'interval': '2',
    }
    response = camara_auth.request_camara_token(oidc_response)

    assert (
        response
        == 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZWZhdWx0IiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.3wWzV6t8bFJUZ6k0WJ9kY3J2kNw9v5zXJ8x1J5g1v2k'
    )

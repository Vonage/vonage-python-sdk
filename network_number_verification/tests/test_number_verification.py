from os.path import abspath
from unittest.mock import MagicMock, patch

import responses
from pytest import raises
from vonage_http_client.http_client import HttpClient
from vonage_network_auth.requests import CreateOidcUrl
from vonage_network_number_verification.errors import NetworkNumberVerificationError
from vonage_network_number_verification.number_verification import (
    NetworkNumberVerification,
)
from vonage_network_number_verification.requests import NumberVerificationRequest

from testutils import build_response, get_mock_jwt_auth

path = abspath(__file__)

number_verification = NetworkNumberVerification(HttpClient(get_mock_jwt_auth()))


def test_http_client_property():
    http_client = number_verification.http_client
    assert isinstance(http_client, HttpClient)


def test_get_oidc_url():
    url_options = CreateOidcUrl(
        redirect_uri='https://example.com/callback',
        state='state_id',
        login_hint='447700900000',
    )
    response = number_verification.get_oidc_url(url_options)

    assert (
        response
        == 'https://oidc.idp.vonage.com/oauth2/auth?client_id=test_application_id&redirect_uri=https%3A%2F%2Fexample.com%2Fcallback&response_type=code&scope=openid+dpv%3AFraudPreventionAndDetection%23number-verification-verify-read&state=state_id&login_hint=%2B447700900000'
    )


@patch('vonage_network_auth.NetworkAuth.get_number_verification_camara_token')
@responses.activate
def test_verify_number(mock_get_number_verification_camara_token: MagicMock):
    build_response(
        path,
        'POST',
        'https://api-eu.vonage.com/oauth2/token',
        'token_request.json',
    )

    mock_get_number_verification_camara_token.return_value = 'token'

    build_response(
        path,
        'POST',
        'https://api-eu.vonage.com/camara/number-verification/v031/verify',
        'verify_number.json',
    )

    number_verification_params = NumberVerificationRequest(
        code='token',
        redirect_uri='https://example.com/callback',
        phone_number='447700900000',
    )
    response = number_verification.verify(number_verification_params)

    assert response.device_phone_number_verified == True


@patch('vonage_network_auth.NetworkAuth.get_number_verification_camara_token')
@responses.activate
def test_verify_hashed_number(mock_get_number_verification_camara_token: MagicMock):
    build_response(
        path,
        'POST',
        'https://api-eu.vonage.com/oauth2/token',
        'token_request.json',
    )

    mock_get_number_verification_camara_token.return_value = 'token'

    build_response(
        path,
        'POST',
        'https://api-eu.vonage.com/camara/number-verification/v031/verify',
        'verify_number.json',
    )

    number_verification_params = NumberVerificationRequest(
        code='token',
        redirect_uri='https://example.com/callback',
        hashed_phone_number='d867b6540ac8db72d860d67d3d612a1621adcf3277573e9299be1153b6d0de15',
    )
    response = number_verification.verify(number_verification_params)

    assert response.device_phone_number_verified == True


def test_verify_number_model_errors():
    with raises(NetworkNumberVerificationError):
        number_verification.verify(
            NumberVerificationRequest(
                code='code', redirect_uri='https://example.com/callback'
            )
        )

    with raises(NetworkNumberVerificationError):
        number_verification.verify(
            NumberVerificationRequest(
                code='code',
                redirect_uri='https://example.com/callback',
                phone_number='447700900000',
                hashed_phone_number='hash',
            )
        )

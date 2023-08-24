from time import time
from unittest.mock import patch
from pytest import raises

from vonage import Client, ClientError

now = int(time())


def test_auth_sets_claims_from_kwargs(client):
    client.auth(jti='asdfzxcv1234', nbf=now + 100, exp=now + 1000)
    assert client._jwt_claims['jti'] == 'asdfzxcv1234'
    assert client._jwt_claims['nbf'] == now + 100
    assert client._jwt_claims['exp'] == now + 1000


def test_auth_sets_claims_from_dict(client):
    custom_jwt_claims = {'jti': 'asdfzxcv1234', 'nbf': now + 100, 'exp': now + 1000}
    client.auth(custom_jwt_claims)
    assert client._jwt_claims['jti'] == 'asdfzxcv1234'
    assert client._jwt_claims['nbf'] == now + 100
    assert client._jwt_claims['exp'] == now + 1000


test_jwt = b'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBsaWNhdGlvbl9pZCI6ImFzZGYxMjM0IiwiaWF0IjoxNjg1NzMxMzkxLCJqdGkiOiIwYzE1MDJhZS05YmI5LTQ4YzQtYmQyZC0yOGFhNWUxYjZkMTkiLCJleHAiOjE2ODU3MzIyOTF9.mAkGeVgWOb7Mrzka7DSj32vSM8RaFpYse_2E7jCQ4DuH8i32wq9FxXGgfwdBQDHzgku3RYIjLM1xlVrGjNM3MsnZgR7ymQ6S4bdTTOmSK0dKbk91SrN7ZAC9k2a6JpCC2ZYgXpZ5BzpDTdy9BYu6msHKmkL79_aabFAhrH36Nk26pLvoI0-KiGImEex-aRR4iiaXhOebXBeqiQTRPKoKizREq4-8zBQv_j6yy4AiEYvBatQ8L_sjHsLj9jjITreX8WRvEW-G4TPpPLMaHACHTDMpJSOZAnegAkzTV2frVRmk6DyVXnemm4L0RQD1XZDaH7JPsKk24Hd2WZQyIgHOqQ'


def vonage_jwt_mock(self, claims):
    return test_jwt


def test_generate_application_jwt(client):
    with patch('vonage.client.JwtClient.generate_application_jwt', vonage_jwt_mock):
        jwt = client._generate_application_jwt()
    assert jwt == test_jwt


def test_create_jwt_auth_string(client):
    headers = client.headers
    with patch('vonage.client.JwtClient.generate_application_jwt', vonage_jwt_mock):
        headers['Authorization'] = client._create_jwt_auth_string()
    assert headers['Accept'] == 'application/json'
    assert headers['Authorization'] == b'Bearer ' + test_jwt


def test_create_jwt_error_no_application_id_or_private_key():
    empty_client = Client()

    with raises(ClientError) as err:
        empty_client._generate_application_jwt()
    assert (
        str(err.value)
        == 'JWT generation failed. Check that you passed in valid values for "application_id" and "private_key".'
    )

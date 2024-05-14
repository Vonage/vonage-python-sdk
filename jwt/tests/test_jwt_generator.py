from vonage_jwt.jwt import JwtClient, VonageJwtError

import os
from pytest import raises
from jwt import decode
from jwt.exceptions import ImmatureSignatureError
from time import time

# Ensure the client isn't being configured with real values
os.environ.clear()


def read_file(path):
    with open(os.path.join(os.path.dirname(__file__), path)) as input_file:
        return input_file.read()


application_id = 'asdf1234'
private_key_string = read_file('data/private_key.txt')
private_key_file_path = './tests/data/private_key.txt'
jwt_client = JwtClient(application_id, private_key_file_path)

public_key = read_file('data/public_key.txt')


def test_create_jwt_client_key_string():
    jwt_client = JwtClient(application_id, private_key_string)
    assert jwt_client._application_id == application_id
    assert jwt_client._private_key == private_key_string


def test_create_jwt_client_key_file():
    jwt_client = JwtClient(application_id, private_key_file_path)
    assert jwt_client._application_id == application_id
    assert jwt_client._private_key == bytes(private_key_string, 'utf-8')


def test_create_jwt_client_error_incomplete():
    with raises(VonageJwtError) as err:
        JwtClient(application_id, None)
    assert str(err.value) == 'Both of "application_id" and "private_key" are required.'


def test_create_jwt_client_error_invalid_key():
    with raises(VonageJwtError) as err:
        JwtClient(application_id, 'invalid-private-key-string')
    assert (
        str(err.value)
        == 'If passing the private key directly as a string, it must be formatted correctly with newlines.'
    )


def test_generate_application_jwt_basic():
    jwt = jwt_client.generate_application_jwt()
    decoded_jwt = decode(jwt, key=public_key, algorithms='RS256')
    assert decoded_jwt['application_id'] == 'asdf1234'
    assert decoded_jwt['exp'] - decoded_jwt['iat'] == 15 * 60


def test_generate_application_jwt_custom_claims():
    now = int(time())
    claims = {'jti': 'qwerasdfzxcv1234', 'nbf': now + 100}
    jwt = jwt_client.generate_application_jwt(claims)
    with raises(ImmatureSignatureError) as err:
        decode(jwt, key=public_key, algorithms='RS256')
    assert str(err.value) == 'The token is not yet valid (nbf)'

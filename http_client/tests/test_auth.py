from os.path import dirname, join
from unittest.mock import patch
import hashlib


from pydantic import ValidationError
from pytest import raises
from vonage_http_client.auth import Auth
from vonage_http_client.errors import InvalidAuthError, JWTGenerationError
from vonage_jwt.jwt import JwtClient


def read_file(path):
    with open(join(dirname(__file__), path)) as input_file:
        return input_file.read()


api_key = 'qwerasdf'
api_secret = '1234qwerasdfzxcv'
application_id = 'asdfzxcv'
private_key = read_file('data/dummy_private_key.txt')
signature_secret = 'signature_secret'
signature_method = 'sha256'


def test_create_auth_class_and_get_objects():
    auth = Auth(
        api_key=api_key,
        api_secret=api_secret,
        application_id=application_id,
        private_key=private_key,
        signature_secret=signature_secret,
        signature_method=signature_method,
    )

    assert auth.api_key == api_key
    assert auth.api_secret == api_secret
    assert type(auth._jwt_client) == JwtClient


def test_create_new_auth_invalid_type():
    with raises(ValidationError):
        Auth(api_key=1234)


def test_auth_init_missing_combinations():
    with raises(InvalidAuthError):
        Auth(api_key=api_key)
    with raises(InvalidAuthError):
        Auth(api_secret=api_secret)
    with raises(InvalidAuthError):
        Auth(application_id=application_id)
    with raises(InvalidAuthError):
        Auth(private_key=private_key)


def test_auth_init_with_invalid_combinations():
    with raises(InvalidAuthError):
        Auth(api_key=api_key, application_id=application_id)
    with raises(InvalidAuthError):
        Auth(api_key=api_key, private_key=private_key)
    with raises(InvalidAuthError):
        Auth(api_secret=api_secret, application_id=application_id)
    with raises(InvalidAuthError):
        Auth(api_secret=api_secret, private_key=private_key)


def test_auth_init_with_valid_api_key_and_api_secret():
    auth = Auth(api_key=api_key, api_secret=api_secret)
    assert auth._api_key == api_key
    assert auth._api_secret == api_secret


def test_auth_init_with_valid_application_id_and_private_key():
    auth = Auth(application_id=application_id, private_key=private_key)
    assert auth._api_key is None
    assert auth._api_secret is None
    assert isinstance(auth._jwt_client, JwtClient)


test_jwt = b'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBsaWNhdGlvbl9pZCI6ImFzZGYxMjM0IiwiaWF0IjoxNjg1NzMxMzkxLCJqdGkiOiIwYzE1MDJhZS05YmI5LTQ4YzQtYmQyZC0yOGFhNWUxYjZkMTkiLCJleHAiOjE2ODU3MzIyOTF9.mAkGeVgWOb7Mrzka7DSj32vSM8RaFpYse_2E7jCQ4DuH8i32wq9FxXGgfwdBQDHzgku3RYIjLM1xlVrGjNM3MsnZgR7ymQ6S4bdTTOmSK0dKbk91SrN7ZAC9k2a6JpCC2ZYgXpZ5BzpDTdy9BYu6msHKmkL79_aabFAhrH36Nk26pLvoI0-KiGImEex-aRR4iiaXhOebXBeqiQTRPKoKizREq4-8zBQv_j6yy4AiEYvBatQ8L_sjHsLj9jjITreX8WRvEW-G4TPpPLMaHACHTDMpJSOZAnegAkzTV2frVRmk6DyVXnemm4L0RQD1XZDaH7JPsKk24Hd2WZQyIgHOqQ'


def vonage_jwt_mock(self):
    return test_jwt


def test_generate_application_jwt():
    auth = Auth(application_id=application_id, private_key=private_key)
    with patch('vonage_http_client.auth.Auth.generate_application_jwt', vonage_jwt_mock):
        jwt = auth.generate_application_jwt()
    assert jwt == test_jwt


def test_create_jwt_auth_string():
    auth = Auth(application_id=application_id, private_key=private_key)
    with patch('vonage_http_client.auth.Auth.generate_application_jwt', vonage_jwt_mock):
        header_auth_string = auth.create_jwt_auth_string()
        assert header_auth_string == b'Bearer ' + test_jwt


def test_create_jwt_error_no_application_id_or_private_key():
    auth = Auth()
    with raises(JWTGenerationError):
        auth.generate_application_jwt()


def test_create_basic_auth_string():
    auth = Auth(api_key=api_key, api_secret=api_secret)
    assert auth.create_basic_auth_string() == 'Basic cXdlcmFzZGY6MTIzNHF3ZXJhc2Rmenhjdg=='


def test_auth_init_with_valid_combinations():
    api_key = 'qwerasdf'
    api_secret = '1234qwerasdfzxcv'
    application_id = 'asdfzxcv'
    private_key = 'dummy_private_key'
    signature_secret = 'signature_secret'
    signature_method = 'sha256'

    auth = Auth(
        api_key=api_key,
        api_secret=api_secret,
        application_id=application_id,
        private_key=private_key,
        signature_secret=signature_secret,
        signature_method=signature_method,
    )

    assert auth._api_key == api_key
    assert auth._api_secret == api_secret
    assert auth._jwt_client.application_id == application_id
    assert auth._jwt_client.private_key == private_key
    assert auth._signature_secret == signature_secret
    assert auth._signature_method == hashlib.sha256


def test_auth_init_with_invalid_combinations():
    api_key = 'qwerasdf'
    api_secret = '1234qwerasdfzxcv'
    application_id = 'asdfzxcv'
    private_key = 'dummy_private_key'
    signature_secret = 'signature_secret'
    signature_method = 'invalid_method'

    with patch('vonage_http_client.auth.hashlib') as mock_hashlib:
        mock_hashlib.sha256.side_effect = AttributeError

        auth = Auth(
            api_key=api_key,
            api_secret=api_secret,
            application_id=application_id,
            private_key=private_key,
            signature_secret=signature_secret,
            signature_method=signature_method,
        )

        assert auth._api_key == api_key
        assert auth._api_secret == api_secret
        assert auth._jwt_client is None
        assert auth._signature_secret == signature_secret
        assert auth._signature_method is None

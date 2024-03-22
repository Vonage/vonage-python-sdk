import hashlib
from os.path import dirname, join
from unittest.mock import patch

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
    assert auth._signature_secret == signature_secret
    assert auth._signature_method == hashlib.sha256


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
    with raises(InvalidAuthError):
        Auth(application_id=application_id, signature_secret=signature_secret)
    with raises(InvalidAuthError):
        Auth(private_key=private_key, signature_secret=signature_secret)


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


def test_sign_params():
    auth = Auth(
        api_key=api_key,
        signature_secret=signature_secret,
        signature_method=signature_method,
    )

    params = {'param1': 'value1', 'param2': 'value2', 'timestamp': 1234567890}

    signed_params_hash = auth.sign_params(params)

    assert (
        signed_params_hash
        == '280c4320703dbc98bfa22db676655ed2acfbfe8792b062ff7622e67f1183c287'
    )


def test_sign_params_default_sig_method():
    auth = Auth(api_key=api_key, signature_secret=signature_secret)

    params = {'param1': 'value1', 'param2': 'value2', 'timestamp': 1234567890}

    signed_params_hash = auth.sign_params(params)

    assert signed_params_hash == '724c2bf6ca423c36e20631b11d1c5753'


def test_sign_params_with_special_characters():
    auth = Auth(api_key=api_key, signature_secret=signature_secret)

    params = {'param1': 'value&1', 'param2': 'value=2', 'timestamp': 1234567890}

    signed_params = auth.sign_params(params)

    assert signed_params == '2bbf0abafb2c55e5af6231513896a2ac'


@patch('vonage_http_client.auth.time', return_value=12345)
def test_sign_params_with_dynamic_timestamp(mock_time):
    auth = Auth(api_key=api_key, signature_secret=signature_secret)

    params = {'param1': 'value1', 'param2': 'value2'}

    signed_params = auth.sign_params(params)

    assert signed_params == 'bc7e95bb4e341090b3a202a2885903a5'


def test_check_signature_valid_signature():
    auth = Auth(api_key=api_key, signature_secret=signature_secret)
    params = {
        'param': 'value',
        'timestamp': 1234567890,
        'sig': '655a4d0b7f064dff438defc52b012cf5',
    }
    assert auth.check_signature(params) == True


def test_check_signature_invalid_signature():
    auth = Auth(api_key=api_key, signature_secret=signature_secret)
    params = {
        'param': 'value',
        'timestamp': 1234567890,
        'sig': 'invalid_signature',
    }
    assert auth.check_signature(params) == False

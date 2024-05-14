from vonage_jwt.verify_jwt import verify_signature, VonageVerifyJwtError
import pytest

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE2OTc2MzQ2ODAsImV4cCI6MzMyNTQ1NDA4MjgsImF1ZCI6IiIsInN1YiI6IiJ9.88vJc3I2HhuqEDixHXVhc9R30tA6U_HQHZTC29y6CGM'
valid_signature = "qwertyuiopasdfghjklzxcvbnm123456"
invalid_signature = 'asdf'


def test_verify_signature_valid():
    assert verify_signature(token, valid_signature) is True


def test_verify_signature_invalid():
    assert verify_signature(token, invalid_signature) is False


def test_verify_signature_error():
    with pytest.raises(VonageVerifyJwtError) as e:
        verify_signature('asdf', valid_signature)
    assert 'DecodeError' in str(e.value)

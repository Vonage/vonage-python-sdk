from vonage import Client, InvalidPhoneNumberError
from vonage._internal import *

from pytest import raises


def test_set_auth_type(client):
    # The client in conftest.py has a valid application id and key
    assert set_auth_type(client) == 'jwt'

    client_no_jwt = Client(key='asdfqwer', secret='1234qwerasdfzxcv')
    assert set_auth_type(client_no_jwt) == 'header'


def test_validate_phone_number():
    assert validate_phone_number('12345678901') == True

    with raises(InvalidPhoneNumberError) as err:
        validate_phone_number('0111')
    assert (
        str(err.value)
        == 'Invalid phone number provided. You provided: "0111".\nUse the E.164 format. Don\'t use a leading + or 00 when entering a phone number, start with the country code, e.g. 447700900000.'
    )
    with raises(InvalidPhoneNumberError) as err:
        validate_phone_number(12345678901)
    assert (
        str(err.value)
        == 'Invalid phone number provided. You must pass in a string in the E.164 format.'
    )

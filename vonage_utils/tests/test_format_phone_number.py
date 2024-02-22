from pytest import raises
from vonage_utils.errors import InvalidPhoneNumberError, InvalidPhoneNumberTypeError
from vonage_utils.utils import format_phone_number


def test_format_phone_numbers():
    number = '1234567890'
    assert format_phone_number('1234567890') == number
    assert format_phone_number(1234567890) == number
    assert format_phone_number('+1234567890') == number
    assert format_phone_number('+ 1 234 567 890') == number
    assert format_phone_number('00 1 234 567 890') == number
    assert format_phone_number('00 1234567890') == number
    assert format_phone_number('447700900000') == '447700900000'
    assert format_phone_number('1234567') == '1234567'
    assert format_phone_number('123456789012345') == '123456789012345'


def test_format_phone_number_invalid_type():
    number = ['1234567890']
    with raises(InvalidPhoneNumberTypeError) as e:
        format_phone_number(number)
    assert '"<class \'list\'>"' in str(e.value)


def test_format_phone_number_invalid_format():
    number = 'not a phone number'
    with raises(InvalidPhoneNumberError) as e:
        format_phone_number(number)
    assert '"not a phone number"' in str(e.value)

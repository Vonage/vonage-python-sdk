from re import search
from typing import Union

from errors import InvalidPhoneNumberError, InvalidPhoneNumberTypeError


def format_phone_number(number: Union[str, int]) -> str:
    """Formats a phone number by removing all non-numeric characters and leading zeros.

    Args:
        number (str, int): The phone number to format.

    Returns:
        str: The formatted phone number.

    Raises:
        InvalidPhoneNumberError: If the phone number is invalid.
        InvalidPhoneNumberTypeError: If the phone number is not a string or an integer.
    """
    if type(number) is not str:
        if type(number) is int:
            number = str(number)
        else:
            raise InvalidPhoneNumberTypeError(
                f'The phone number provided has an invalid type. You provided: "{type(number)}". Must be a string or an integer.'
            )

    # Remove all non-numeric characters and leading zeros
    formatted_number = ''.join(filter(str.isdigit, number)).lstrip('0')

    if search(r'^[1-9]\d{6,14}$', formatted_number):
        return formatted_number
    raise InvalidPhoneNumberError(
        f'Invalid phone number provided. You provided: "{number}".\n'
        'Use the E.164 format and start with the country code, e.g. "447700900000".'
    )

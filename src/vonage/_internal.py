from __future__ import annotations
from typing import TYPE_CHECKING

from .errors import InvalidPhoneNumberError

if TYPE_CHECKING:
    from vonage import Client


def _format_date_param(params, key, format="%Y-%m-%d %H:%M:%S"):
    """
    Utility function to convert datetime values to strings.

    If the value is already a str, or is not in the dict, no change is made.

    :param params: A `dict` of params that may contain a `datetime` value.
    :param key: The datetime value to be converted to a `str`
    :param format: The `strftime` format to be used to format the date. The default value is '%Y-%m-%d %H:%M:%S'
    """
    if key in params:
        param = params[key]
        if hasattr(param, "strftime"):
            params[key] = param.strftime(format)


def set_auth_type(client: Client) -> str:
    """Sets the authentication type used. If a JWT Client has been created,
    it will create a JWT and use JWT authentication."""

    if hasattr(client, '_jwt_client'):
        return 'jwt'
    else:
        return 'header'


def validate_phone_number(number: str) -> None:
    """Validates that a given phone number is a valid E.164 format string."""
    if type(number) is not str:
        raise InvalidPhoneNumberError(
            'Invalid phone number provided. You must pass in a string in the E.164 format.'
        )

    from re import search

    if search(r'^[1-9]\d{6,14}$', number):
        return True
    raise InvalidPhoneNumberError(
        f'Invalid phone number provided. You provided: "{number}".\n'
        "Use the E.164 format. Don't use a leading + or 00 when entering a phone number, start with the country code, e.g. 447700900000."
    )

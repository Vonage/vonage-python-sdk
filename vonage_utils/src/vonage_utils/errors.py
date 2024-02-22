class VonageError(Exception):
    """Base Error Class for all Vonage SDK errors."""


class InvalidPhoneNumberError(VonageError):
    """An invalid phone number was provided."""


class InvalidPhoneNumberTypeError(VonageError):
    """An invalid phone number type was provided.

    Should be a string or an integer.
    """

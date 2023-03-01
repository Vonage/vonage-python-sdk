class ClientError(Exception):
    pass


class ServerError(Exception):
    pass


class AuthenticationError(ClientError):
    pass


class CallbackRequiredError(Exception):
    """Indicates a callback is required but was not present."""


class MessagesError(Exception):
    """
    Indicates an error related to the Messages class which calls the Vonage Messages API.
    """


class SmsError(Exception):
    """
    Indicates an error related to the Sms class which calls the Vonage SMS API.
    """


class PartialFailureError(Exception):
    """
    Indicates that one or more parts of the message was not sent successfully.
    """


class PricingTypeError(Exception):
    """A pricing type was specified that is not allowed."""


class RedactError(Exception):

    """Error related to the Redact class or Redact API."""


class InvalidAuthenticationTypeError(Exception):
    """An authentication method was specified that is not allowed."""


class InvalidRoleError(Exception):
    """The specified role was invalid."""


class TokenExpiryError(Exception):
    """The specified token expiry time was invalid."""


class InvalidOptionsError(Exception):
    """The option(s) that were specified are invalid."""

    """An authentication method was specified that is not allowed."""


class VerifyError(Exception):
    """Error related to the Verify API."""


class BlockedNumberError(Exception):
    """The number you are trying to verify is blocked for verification."""


class NumberInsightError(Exception):
    """Error related to the Number Insight API."""


class SipError(Exception):
    """Error related to usage of SIP calls."""


class InvalidInputError(Exception):
    """The input that was provided was invalid."""

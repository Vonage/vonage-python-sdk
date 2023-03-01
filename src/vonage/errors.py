class ClientError(Exception):
    pass


class ServerError(Exception):
    pass


class AuthenticationError(ClientError):
    pass


class CallbackRequiredError(ClientError):
    """Indicates a callback is required but was not present."""


class MessagesError(ClientError):
    """
    Indicates an error related to the Messages class which calls the Vonage Messages API.
    """


class SmsError(ClientError):
    """
    Indicates an error related to the Sms class which calls the Vonage SMS API.
    """


class PartialFailureError(ClientError):
    """
    Indicates that one or more parts of the message was not sent successfully.
    """


class PricingTypeError(ClientError):
    """A pricing type was specified that is not allowed."""


class RedactError(ClientError):

    """Error related to the Redact class or Redact API."""


class InvalidAuthenticationTypeError(ClientError):
    """An authentication method was specified that is not allowed."""


class InvalidRoleError(ClientError):
    """The specified role was invalid."""


class TokenExpiryError(ClientError):
    """The specified token expiry time was invalid."""


class InvalidOptionsError(ClientError):
    """The option(s) that were specified are invalid."""

    """An authentication method was specified that is not allowed."""


class VerifyError(ClientError):
    """Error related to the Verify API."""


class BlockedNumberError(ClientError):
    """The number you are trying to verify is blocked for verification."""


class NumberInsightError(ClientError):
    """Error related to the Number Insight API."""


class SipError(ClientError):
    """Error related to usage of SIP calls."""


class InvalidInputError(ClientError):
    """The input that was provided was invalid."""

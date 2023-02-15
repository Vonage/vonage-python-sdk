class Error(Exception):
    pass


class ClientError(Error):
    pass


class ServerError(Error):
    pass


class AuthenticationError(ClientError):
    pass


class CallbackRequiredError(Error):
    """Indicates a callback is required but was not present."""


class MessagesError(Error):
    """
    Indicates an error related to the Messages class which calls the Vonage Messages API.
    """


class SmsError(Error):
    """
    Indicates an error related to the Sms class which calls the Vonage SMS API.
    """


class PartialFailureError(Error):
    """
    Indicates that one or more parts of the message was not sent successfully.
    """


class PricingTypeError(Error):
    """A pricing type was specified that is not allowed."""


class RedactError(Error):

    """Error related to the Redact class or Redact API."""


class InvalidAuthenticationTypeError(Error):
    """An authentication method was specified that is not allowed."""


class InvalidRoleError(Error):
    """The specified role was invalid."""


class TokenExpiryError(Error):
    """The specified token expiry time was invalid."""


class InvalidOptionsError(Error):
    """The option(s) that were specified are invalid."""

    """An authentication method was specified that is not allowed."""


class VerifyError(Error):
    """Error related to the Verify API."""


class BlockedNumberError(Error):
    """The number you are trying to verify is blocked for verification."""


class NumberInsightError(Error):
    """Error related to the Number Insight API."""


class SipError(Error):
    """Error related to usage of SIP calls."""


class InvalidInputError(Error):
    """The input that was provided was invalid."""

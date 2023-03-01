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


class PricingTypeError(Exception):
    """A pricing type was specified that is not allowed."""


class RedactError(Exception):
    """Error related to the Redact class or Redact API."""


class InvalidAuthenticationTypeError(Exception):
    """An authentication method was specified that is not allowed"""

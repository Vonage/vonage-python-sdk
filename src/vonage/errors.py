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


class PricingTypeError(Error):
    """A pricing type was specified that is not allowed."""


class RedactError(Error):
    """Error related to the Redact class or Redact API."""


class InvalidAuthenticationTypeError(Error):
    """An authentication method was specified that is not allowed."""


class Verify2Error(ClientError):
    """An error relating to the Verify (V2) API."""

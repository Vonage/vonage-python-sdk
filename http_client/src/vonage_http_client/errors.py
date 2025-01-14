from json import JSONDecodeError, dumps
from typing import Optional

from requests import Response
from vonage_utils.errors import VonageError


class JWTGenerationError(VonageError):
    """Indicates an error with generating a JWT."""


class InvalidAuthError(VonageError):
    """Indicates an error with the authentication credentials provided."""


class InvalidHttpClientOptionsError(VonageError):
    """The options passed to the HTTP Client were invalid."""


class HttpRequestError(VonageError):
    """Exception indicating an error in the response received from a Vonage SDK request.

    Args:
        response (requests.Response): The HTTP response object.

    Attributes:
        response (requests.Response): The HTTP response object.
        message (str): The returned error message.
    """

    def __init__(self, response: Response):
        self.response = response
        self.message = self._format_error_message()
        super().__init__(self.message)

    def _format_error_message(self) -> str:
        body = self._get_response_body()
        base_message = f'{self.response.status_code} response from {self.response.url}'

        if body:
            return f'{base_message}. Error response body: \n{body}'
        return base_message

    def _get_response_body(self) -> Optional[str]:
        if not self.response.content:
            return None
        try:
            return dumps(self.response.json(), indent=4)
        except JSONDecodeError:
            return self.response.text


class AuthenticationError(HttpRequestError):
    """Exception indicating authentication failure in a Vonage SDK request.

    This error is raised when the HTTP response status code is 401 (Unauthorized).

    Args:
        response (requests.Response): The HTTP response object.

    Attributes (inherited from HttpRequestError parent exception):
        response (requests.Response): The HTTP response object.
        message (str): The returned error message.
    """

    def __init__(self, response: Response):
        super().__init__(response)


class ForbiddenError(HttpRequestError):
    """Exception indicating a forbidden request in a Vonage SDK request.

    This error is raised when the HTTP response status code is 403 (Forbidden).

    Args:
        response (requests.Response): The HTTP response object.

    Attributes (inherited from HttpRequestError parent exception):
        response (requests.Response): The HTTP response object.
        message (str): The returned error message.
    """

    def __init__(self, response: Response):
        super().__init__(response)


class NotFoundError(HttpRequestError):
    """Exception indicating a resource was not found in a Vonage SDK request.

    This error is raised when the HTTP response status code is 404 (Not Found).

    Args:
        response (requests.Response): The HTTP response object.

    Attributes (inherited from HttpRequestError parent exception):
        response (requests.Response): The HTTP response object.
        message (str): The returned error message.
    """

    def __init__(self, response: Response):
        super().__init__(response)


class RateLimitedError(HttpRequestError):
    """Exception indicating a rate limit was hit when making too many requests to a Vonage
    endpoint.

    This error is raised when the HTTP response status code is 429 (Too Many Requests).

    Args:
        response (requests.Response): The HTTP response object.

    Attributes (inherited from HttpRequestError parent exception):
        response (requests.Response): The HTTP response object.
        message (str): The returned error message.
    """

    def __init__(self, response: Response):
        super().__init__(response)


class ServerError(HttpRequestError):
    """Exception indicating an error was returned by a Vonage server in response to a
    Vonage SDK request.

    This error is raised when the HTTP response status code is 500 (Internal Server Error).

    Args:
        response (requests.Response): The HTTP response object.

    Attributes (inherited from HttpRequestError parent exception):
        response (requests.Response): The HTTP response object.
        message (str): The returned error message.
    """

    def __init__(self, response: Response):
        super().__init__(response)


class FileStreamingError(VonageError):
    """Exception indicating an error occurred while streaming a file in a Vonage SDK
    request."""

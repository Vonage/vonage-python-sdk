from json import JSONDecodeError, dumps

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
        content_type (str): The response content type.

    Attributes:
        response (requests.Response): The HTTP response object.
        message (str): The returned error message.
    """

    def __init__(self, response: Response, content_type: str):
        self.response = response
        self.set_error_message(self.response, content_type)
        super().__init__(self.message)

    def set_error_message(self, response: Response, content_type: str):
        body = None
        if content_type == 'application/json':
            try:
                body = dumps(response.json(), indent=4)
            except JSONDecodeError:
                pass
        else:
            body = response.text

        if body:
            self.message = f'{response.status_code} response from {response.url}. Error response body: \n{body}'
        else:
            self.message = f'{response.status_code} response from {response.url}.'


class AuthenticationError(HttpRequestError):
    """Exception indicating authentication failure in a Vonage SDK request.

    This error is raised when the HTTP response status code is 401 (Unauthorized).

    Args:
        response (requests.Response): The HTTP response object.
        content_type (str): The response content type.

    Attributes (inherited from HttpRequestError parent exception):
        response (requests.Response): The HTTP response object.
        message (str): The returned error message.
    """

    def __init__(self, response: Response, content_type: str):
        super().__init__(response, content_type)


class ForbiddenError(HttpRequestError):
    """Exception indicating a forbidden request in a Vonage SDK request.

    This error is raised when the HTTP response status code is 403 (Forbidden).

    Args:
        response (requests.Response): The HTTP response object.
        content_type (str): The response content type.

    Attributes (inherited from HttpRequestError parent exception):
        response (requests.Response): The HTTP response object.
        message (str): The returned error message.
    """

    def __init__(self, response: Response, content_type: str):
        super().__init__(response, content_type)


class NotFoundError(HttpRequestError):
    """Exception indicating a resource was not found in a Vonage SDK request.

    This error is raised when the HTTP response status code is 404 (Not Found).

    Args:
        response (requests.Response): The HTTP response object.
        content_type (str): The response content type.

    Attributes (inherited from HttpRequestError parent exception):
        response (requests.Response): The HTTP response object.
        message (str): The returned error message.
    """

    def __init__(self, response: Response, content_type: str):
        super().__init__(response, content_type)


class RateLimitedError(HttpRequestError):
    """Exception indicating a rate limit was hit when making too many requests to a Vonage endpoint.

    This error is raised when the HTTP response status code is 429 (Too Many Requests).

    Args:
        response (requests.Response): The HTTP response object.
        content_type (str): The response content type.

    Attributes (inherited from HttpRequestError parent exception):
        response (requests.Response): The HTTP response object.
        message (str): The returned error message.
    """

    def __init__(self, response: Response, content_type: str):
        super().__init__(response, content_type)


class ServerError(HttpRequestError):
    """Exception indicating an error was returned by a Vonage server in response to a Vonage SDK
    request.

    This error is raised when the HTTP response status code is 500 (Internal Server Error).

    Args:
        response (requests.Response): The HTTP response object.
        content_type (str): The response content type.

    Attributes (inherited from HttpRequestError parent exception):
        response (requests.Response): The HTTP response object.
        message (str): The returned error message.
    """

    def __init__(self, response: Response, content_type: str):
        super().__init__(response, content_type)

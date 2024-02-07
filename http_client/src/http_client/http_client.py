from logging import getLogger
from platform import python_version
from typing import Literal, Optional

from http_client.auth import Auth
from http_client.errors import (
    AuthenticationError,
    HttpRequestError,
    InvalidHttpClientOptionsError,
    RateLimitedError,
    ServerError,
)
from pydantic import BaseModel, Field, ValidationError, validate_call
from requests import Response
from requests.adapters import HTTPAdapter
from requests.sessions import Session
from typing_extensions import Annotated

logger = getLogger('vonage-http-client-v2')


class HttpClientOptions(BaseModel):
    api_host: str = 'api.nexmo.com'
    rest_host: Optional[str] = 'rest.nexmo.com'
    timeout: Optional[Annotated[int, Field(ge=0)]] = None
    pool_connections: Optional[Annotated[int, Field(ge=1)]] = 10
    pool_maxsize: Optional[Annotated[int, Field(ge=1)]] = 10
    max_retries: Optional[Annotated[int, Field(ge=0)]] = 3


class HttpClient:
    """A synchronous HTTP client used to send authenticated requests to Vonage APIs.

    Args:
        auth (:class: Auth): An instance of the Auth class containing credentials to use when making HTTP requests.
        http_client_options (dict, optional): Customization options for the HTTP Client.

        The http_client_options dict can have any of the following fields:
            api_host (str, optional): The API host to use for HTTP requests. Defaults to 'api.nexmo.com'.
            rest_host (str, optional): The REST host to use for HTTP requests. Defaults to 'rest.nexmo.com'.
            timeout (int, optional): The timeout for HTTP requests in seconds. Defaults to None.
            pool_connections (int, optional): The number of pool connections. Must be > 0. Default is 10.
            pool_maxsize (int, optional): The maximum size of the connection pool. Must be > 0. Default is 10.
            max_retries (int, optional): The maximum number of retries for HTTP requests. Must be >= 0. Default is 3.
    """

    def __init__(self, auth: Auth, http_client_options: HttpClientOptions = None):
        self._auth = auth
        try:
            if http_client_options is not None:
                self._http_client_options = HttpClientOptions.model_validate(
                    http_client_options
                )
            else:
                self._http_client_options = HttpClientOptions()
        except ValidationError as err:
            raise InvalidHttpClientOptionsError(
                'Invalid options provided to the HTTP Client'
            ) from err

        self._api_host = self._http_client_options.api_host
        self._rest_host = self._http_client_options.rest_host

        self._timeout = self._http_client_options.timeout
        self._session = Session()
        self._adapter = HTTPAdapter(
            pool_connections=self._http_client_options.pool_connections,
            pool_maxsize=self._http_client_options.pool_maxsize,
            max_retries=self._http_client_options.max_retries,
        )
        self._session.mount('https://', self._adapter)

        self._user_agent = f'vonage-python-sdk python/{python_version()}'
        self._headers = {'User-Agent': self._user_agent, 'Accept': 'application/json'}

    @property
    def auth(self):
        return self._auth

    @property
    def http_client_options(self):
        return self._http_client_options

    @property
    def api_host(self):
        return self._api_host

    @property
    def rest_host(self):
        return self._rest_host

    def post(self, host: str, request_path: str = '', params: dict = None):
        return self.make_request('POST', host, request_path, params)

    def get(self, host: str, request_path: str = '', params: dict = None):
        return self.make_request('GET', host, request_path, params)

    @validate_call
    def make_request(
        self,
        request_type: Literal['GET', 'POST'],
        host: str,
        request_path: str = '',
        params: Optional[dict] = None,
    ):
        url = f'https://{host}{request_path}'
        logger.debug(
            f'{request_type} request to {url}, with data: {params}; headers: {self._headers}'
        )
        with self._session.request(
            request_type,
            url,
            json=params,
            headers=self._headers,
            timeout=self._timeout,
        ) as response:
            return self._parse_response(response)

    def _parse_response(self, response: Response):
        logger.debug(
            f'Response received from {response.url} with status code: {response.status_code}; headers: {response.headers}'
        )
        content_type = response.headers['Content-Type'].split(';', 1)[0]
        if 200 <= response.status_code < 300:
            if response.status_code == 204:
                return None
            return response.json()
        if response.status_code >= 400:
            logger.warning(
                f'Http Response Error! Status code: {response.status_code}; content: {repr(response.text)}; from url: {response.url}'
            )
            if response.status_code == 401 or response.status_code == 403:
                raise AuthenticationError(response, content_type)
            elif response.status_code == 429:
                raise RateLimitedError(response, content_type)
            elif response.status_code == 500:
                raise ServerError(response, content_type)
        raise HttpRequestError(response, content_type)

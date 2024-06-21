from json import JSONDecodeError
from logging import getLogger
from platform import python_version
from typing import Literal, Optional, Union

from pydantic import BaseModel, Field, ValidationError, validate_call
from requests import PreparedRequest, Response
from requests.adapters import HTTPAdapter
from requests.sessions import Session
from typing_extensions import Annotated
from vonage_http_client.auth import Auth
from vonage_http_client.errors import (
    AuthenticationError,
    ForbiddenError,
    HttpRequestError,
    InvalidHttpClientOptionsError,
    NotFoundError,
    RateLimitedError,
    ServerError,
)

logger = getLogger('vonage')


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
        auth (Auth): An instance of the Auth class containing credentials to use when making HTTP requests.
        http_client_options (dict, optional): Customization options for the HTTP Client.
        sdk_version (str, optional): The SDK version used.

        The http_client_options dict can have any of the following fields:
            api_host (str, optional): The API host to use for HTTP requests. Defaults to 'api.nexmo.com'.
            rest_host (str, optional): The REST host to use for HTTP requests. Defaults to 'rest.nexmo.com'.
            timeout (int, optional): The timeout for HTTP requests in seconds. Defaults to None.
            pool_connections (int, optional): The number of pool connections. Must be > 0. Default is 10.
            pool_maxsize (int, optional): The maximum size of the connection pool. Must be > 0. Default is 10.
            max_retries (int, optional): The maximum number of retries for HTTP requests. Must be >= 0. Default is 3.
    """

    def __init__(
        self,
        auth: Auth,
        http_client_options: HttpClientOptions = None,
        sdk_version: str = None,
    ):
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

        self._user_agent = f'vonage-python-sdk/{sdk_version} python/{python_version()}'
        self._headers = {'User-Agent': self._user_agent, 'Accept': 'application/json'}

        self._last_request = None
        self._last_response = None

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

    @property
    def user_agent(self):
        return self._user_agent

    @property
    def last_request(self) -> Optional[PreparedRequest]:
        """The last request sent to the server.

        Returns:
            Optional[PreparedRequest]: The exact bytes of the request sent to the server,
                or None if no request has been sent.
        """
        return self._last_response.request

    @property
    def last_response(self) -> Optional[Response]:
        """The last response received from the server.

        Returns:
            Optional[Response]: The response object received from the server,
                or None if no response has been received.
        """
        return self._last_response

    def post(
        self,
        host: str,
        request_path: str = '',
        params: dict = None,
        auth_type: Literal['jwt', 'basic', 'body', 'signature', 'oauth2'] = 'jwt',
        sent_data_type: Literal['json', 'form', 'query-params'] = 'json',
        token: Optional[str] = None,
    ) -> Union[dict, None]:
        return self.make_request(
            'POST', host, request_path, params, auth_type, sent_data_type, token
        )

    def get(
        self,
        host: str,
        request_path: str = '',
        params: dict = None,
        auth_type: Literal['jwt', 'basic', 'body', 'signature'] = 'jwt',
        sent_data_type: Literal['json', 'form', 'query_params'] = 'query_params',
    ) -> Union[dict, None]:
        return self.make_request(
            'GET', host, request_path, params, auth_type, sent_data_type
        )

    def patch(
        self,
        host: str,
        request_path: str = '',
        params: dict = None,
        auth_type: Literal['jwt', 'basic', 'body', 'signature'] = 'jwt',
        sent_data_type: Literal['json', 'form', 'query_params'] = 'json',
    ) -> Union[dict, None]:
        return self.make_request(
            'PATCH', host, request_path, params, auth_type, sent_data_type
        )

    def put(
        self,
        host: str,
        request_path: str = '',
        params: dict = None,
        auth_type: Literal['jwt', 'basic', 'body', 'signature'] = 'jwt',
        sent_data_type: Literal['json', 'form', 'query_params'] = 'json',
    ) -> Union[dict, None]:
        return self.make_request(
            'PUT', host, request_path, params, auth_type, sent_data_type
        )

    def delete(
        self,
        host: str,
        request_path: str = '',
        params: dict = None,
        auth_type: Literal['jwt', 'basic', 'body', 'signature'] = 'jwt',
        sent_data_type: Literal['json', 'form', 'query_params'] = 'json',
    ) -> Union[dict, None]:
        return self.make_request(
            'DELETE', host, request_path, params, auth_type, sent_data_type
        )

    @validate_call
    def make_request(
        self,
        request_type: Literal['GET', 'POST', 'PATCH', 'PUT', 'DELETE'],
        host: str,
        request_path: str = '',
        params: Optional[dict] = None,
        auth_type: Literal['jwt', 'basic', 'body', 'signature', 'oauth2'] = 'jwt',
        sent_data_type: Literal['json', 'form', 'query_params'] = 'json',
        token: Optional[str] = None,
    ):
        url = f'https://{host}{request_path}'
        logger.debug(
            f'{request_type} request to {url}, with data: {params}; headers: {self._headers}'
        )
        if auth_type == 'jwt':
            self._headers['Authorization'] = self._auth.create_jwt_auth_string()
        elif auth_type == 'basic':
            self._headers['Authorization'] = self._auth.create_basic_auth_string()
        elif auth_type == 'body':
            params['api_key'] = self._auth.api_key
            params['api_secret'] = self._auth.api_secret
        elif auth_type == 'oauth2':
            self._headers['Authorization'] = f'Bearer {token}'
        elif auth_type == 'signature':
            params['api_key'] = self._auth.api_key
            params['sig'] = self._auth.sign_params(params)

        request_params = {
            'method': request_type,
            'url': url,
            'headers': self._headers,
            'timeout': self._timeout,
        }

        if sent_data_type == 'json':
            self._headers['Content-Type'] = 'application/json'
            request_params['json'] = params
        elif sent_data_type == 'query_params':
            request_params['params'] = params
        elif sent_data_type == 'form':
            request_params['data'] = params

        with self._session.request(**request_params) as response:
            return self._parse_response(response)

    def append_to_user_agent(self, string: str):
        self._user_agent += f' {string}'

    def _parse_response(self, response: Response) -> Union[dict, None]:
        logger.debug(
            f'Response received from {response.url} with status code: {response.status_code}; headers: {response.headers}'
        )
        self._last_response = response
        if 200 <= response.status_code < 300:
            try:
                return response.json()
            except JSONDecodeError:
                return None
        if response.status_code >= 400:
            content_type = response.headers['Content-Type'].split(';', 1)[0]
            logger.warning(
                f'Http Response Error! Status code: {response.status_code}; content: {repr(response.text)}; from url: {response.url}'
            )
            if response.status_code == 401:
                raise AuthenticationError(response, content_type)
            if response.status_code == 403:
                raise ForbiddenError(response, content_type)
            elif response.status_code == 404:
                raise NotFoundError(response, content_type)
            elif response.status_code == 429:
                raise RateLimitedError(response, content_type)
            elif response.status_code == 500:
                raise ServerError(response, content_type)
        raise HttpRequestError(response, content_type)

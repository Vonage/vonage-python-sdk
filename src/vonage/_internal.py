import logging

from requests.sessions import Session

from .errors import AuthenticationError, ClientError, ServerError

try:
    from json import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

logger = logging.getLogger("nexmo")


class BasicAuthenticatedServer(object):
    def __init__(self, host, user_agent, api_key, api_secret, timeout=None):
        self._host = host
        self._session = session = Session()
        self.timeout = None
        session.auth = (api_key, api_secret)  # Basic authentication.
        session.headers.update({"User-Agent": user_agent})

    def _uri(self, path):
        return "{host}{path}".format(host=self._host, path=path)

    def get(self, path, params=None, headers=None):
        return self._parse(
            self._session.get(self._uri(path), params=params, headers=headers, timeout=self.timeout)
        )

    def post(self, path, body=None, headers=None):
        return self._parse(
            self._session.post(self._uri(path), json=body, headers=headers, timeout=self.timeout)
        )

    def put(self, path, body=None, headers=None):
        return self._parse(
            self._session.put(self._uri(path), json=body, headers=headers, timeout=self.timeout)
        )

    def delete(self, path, body=None, headers=None):
        return self._parse(
            self._session.delete(self._uri(path), json=body, headers=headers, timeout=self.timeout)
        )

    def _parse(self, response):
        logger.debug("Response headers %r", response.headers)
        if response.status_code == 401:
            raise AuthenticationError()
        elif response.status_code == 204:
            return None
        elif 200 <= response.status_code < 300:
            return response.json()
        elif 400 <= response.status_code < 500:
            logger.warning(
                "Client error: %s %r", response.status_code, response.content
            )
            message = "{code} response".format(code=response.status_code)
            # Test for standard error format:
            try:
                error_data = response.json()
                if (
                    "type" in error_data
                    and "title" in error_data
                    and "detail" in error_data
                ):
                    message = "{title}: {detail} ({type})".format(
                        title=error_data["title"],
                        detail=error_data["detail"],
                        type=error_data["type"],
                    )
            except JSONDecodeError:
                pass
            raise ClientError(message)
        elif 500 <= response.status_code < 600:
            logger.warning(
                "Server error: %s %r", response.status_code, response.content
            )
            message = "{code} response".format(code=response.status_code)
            raise ServerError(message)


class ApplicationV2(object):
    """
    Provides Application API v2 functionality.

    Don't instantiate this class yourself, access it via :py:attr:`vonage.Client.application_v2`
    """

    def __init__(self, api_server):
        self._api_server = api_server

    def create_application(self, application_data):
        """
        Create an application using the provided `application_data`.

        :param dict application_data: A JSON-style dict describing the application to be created.

        >>> client.application_v2.create_application({ 'name': 'My Cool App!' })

        Details of the `application_data` dict are described at https://developer.nexmo.com/api/application.v2#createApplication
        """
        return self._api_server.post("/v2/applications", application_data)

    def get_application(self, application_id):
        """
        Get application details for the application with `application_id`.

        The format of the returned dict is described at https://developer.nexmo.com/api/application.v2#getApplication

        :param str application_id: The application ID.
        :rtype: dict
        """

        return self._api_server.get(
            "/v2/applications/{application_id}".format(application_id=application_id),
            headers={"content-type": "application/json"},
        )

    def update_application(self, application_id, params):
        """
        Update the application with `application_id` using the values provided in `params`.


        """
        return self._api_server.put(
            "/v2/applications/{application_id}".format(application_id=application_id),
            params,
        )

    def delete_application(self, application_id):
        """
        Delete the application with `application_id`.
        """

        self._api_server.delete(
            "/v2/applications/{application_id}".format(application_id=application_id),
            headers={"content-type": "application/json"},
        )

    def list_applications(self, page_size=None, page=None):
        """
        List all applications for your account.

        Results are paged, so each page will need to be requested to see all applications.

        :param int page_size: The number of items in the page to be returned
        :param int page: The page number of the page to be returned.
        """
        params = _filter_none_values({"page_size": page_size, "page": page})

        return self._api_server.get(
            "/v2/applications",
            params=params,
            headers={"content-type": "application/json"},
        )


def _filter_none_values(d):
    return {k: v for k, v in d.items() if v is not None}


def _format_date_param(params, key, format="%Y-%m-%d %H:%M:%S"):
    """
    Utility function to convert datetime values to strings.

    If the value is already a str, or is not in the dict, no change is made.

    :param params: A `dict` of params that may contain a `datetime` value.
    :param key: The datetime value to be converted to a `str`
    :param format: The `strftime` format to be used to format the date. The default value is '%Y-%m-%d %H:%M:%S'
    """
    if key in params:
        param = params[key]
        if hasattr(param, "strftime"):
            params[key] = param.strftime(format)

import logging

from requests.sessions import Session

from .errors import AuthenticationError, ClientError, ServerError

try:
    from json import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

logger = logging.getLogger("nexmo")


class Server(object):
    def __init__(self, host, user_agent, api_key, api_secret):
        self._host = host
        self._session = session = Session()
        session.auth = (api_key, api_secret)  # Basic authentication.
        session.headers.update({"User-Agent": user_agent})

    def _uri(self, path):
        return "{host}{path}".format(host=self._host, path=path)

    def get(self, path, params=None, headers=None):
        return self._parse(
            self._session.get(self._uri(path), params=params, headers=headers)
        )

    def post(self, path, body=None, headers=None):
        return self._parse(
            self._session.post(self._uri(path), json=body, headers=headers)
        )

    def put(self, path, body=None, headers=None):
        return self._parse(
            self._session.put(self._uri(path), json=body, headers=headers)
        )

    def delete(self, path, body=None, headers=None):
        return self._parse(
            self._session.delete(self._uri(path), json=body, headers=headers)
        )

    def _parse(self, response):
        logger.debug("Response headers %r", response.headers)
        if response.status_code == 401:
            raise AuthenticationError()
        elif response.status_code == 204:
            return None
        elif 200 <= response.status_code < 300:
            # Strip off any encoding from the content-type header:
            content_mime = response.headers.get("content-type").split(";", 1)[0]
            if content_mime == "application/json":
                return response.json()
            else:
                return response.content
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
    def __init__(self, api_server):
        self._api_server = api_server

    def create_application(self, params=None):
        return self._api_server.post("/v2/applications", params)

    def update_application(self, application_id, params):
        return self._api_server.put(
            "/v2/applications/{application_id}".format(application_id=application_id),
            params or kwargs,
        )

    def delete_application(self, application_id):
        return self._api_server.delete(
            "/v2/applications/{application_id}".format(application_id=application_id),
            headers={"content-type": "application/json"},
        )

    def list_applications(self):
        # TODO: Report that this doesn't work without the meaningless content-type header:
        return self._api_server.get(
            "/v2/applications", headers={"content-type": "application/json"}
        )

    def get_application(self, application_id):
        return self._api_server.get(
            "/v2/applications/{application_id}".format(application_id=application_id),
            headers={"content-type": "application/json"},
        )

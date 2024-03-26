from typing import Optional
from pydantic import validate_call
from vonage_http_client.http_client import HttpClient

from .errors import UsersError
from .requests import ListUsersRequest
from .responses import ListUsersResponse


class Users:
    """Class containing methods for user management.

    When using APIs that require a Vonage Application to be created,
    you can create users to associate with that application.
    """

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client
        self._auth_type = 'jwt'

    @validate_call
    def list_users(self, params: Optional[ListUsersRequest] = None) -> ListUsersResponse:
        """List all users."""
        response = self._http_client.get(
            self._http_client.api_host,
            '/v1/users',
            params.model_dump() if params is not None else None,
            self._auth_type,
        )
        return ListUsersResponse(**response)

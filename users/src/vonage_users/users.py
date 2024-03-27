from typing import Generator, Literal, Optional

from pydantic import BaseModel, validate_call
from vonage_http_client.http_client import HttpClient

from .common import User
from .requests import ListUsersRequest
from .responses import CreateUserResponse, ListUsersResponse


class Filters(BaseModel):
    order: Optional[Literal['asc', 'desc', 'ASC', 'DESC']] = None


import urllib.parse


def parse_cursor_from_url(url: str) -> Optional[str]:
    """Extract the cursor from the "next" URL."""
    query_string = urllib.parse.urlparse(url).query
    params = urllib.parse.parse_qs(query_string)
    return params.get('cursor', [None])[0]


class Users:
    """Class containing methods for user management.

    When using APIs that require a Vonage Application to be created, you can create users to
    associate with that application.
    """

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client
        self._auth_type = 'jwt'

    @validate_call
    def list_users(
        self,
        order: Literal['asc', 'desc', 'ASC', 'DESC'] = None,
        name: str = None,
    ) -> Generator:
        """List all users with pagination handled by a generator."""
        cursor = None
        while True:
            params = ListUsersRequest(order=order, cursor=cursor, name=name)
            response = self._http_client.get(
                self._http_client.api_host,
                '/v1/users',
                # need to send the right stuff to the api
                params.model_dump() if params is not None else None,
                self._auth_type,
            )
            users = ListUsersResponse(**response)
            for user in users.embedded.users:
                yield user
            if not users.links.next:
                break
            cursor = parse_cursor_from_url(users.links.next.href)

    @validate_call
    def create_user(self, params: Optional[User]):
        """Create a user."""
        response = self._http_client.post(
            self._http_client.api_host,
            '/v1/users',
            params.model_dump() if params is not None else None,
            self._auth_type,
        )
        return CreateUserResponse(**response)

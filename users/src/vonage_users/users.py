from typing import Optional
from urllib.parse import parse_qs, urlparse

from pydantic import validate_call
from vonage_http_client.http_client import HttpClient

from .common import User
from .requests import ListUsersFilter
from .responses import ListUsersResponse, UserSummary


class Users:
    """Class containing methods for user management.

    When using APIs that require a Vonage Application to be created, you can create users
    to associate with that application.
    """

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client
        self._auth_type = 'jwt'

    @property
    def http_client(self) -> HttpClient:
        """The HTTP client used to make requests to the Users API.

        Returns:
            HttpClient: The HTTP client used to make requests to the Users API.
        """
        return self._http_client

    @validate_call
    def list_users(
        self, filter: ListUsersFilter = ListUsersFilter()
    ) -> tuple[list[UserSummary], Optional[str]]:
        """List all users.

        Retrieves a list of all users. Gets 100 users by default.
        If you want to see more information about a specific user, you can use the
            `Users.get_user` method.

        Args:
            params (ListUsersFilter, optional): An instance of the `ListUsersFilter`
                class that allows you to specify additional parameters for the user listing.

        Returns:
            tuple[list[UserSummary], Optional[str]]: A tuple containing a list of `UserSummary`
                objects representing the users and a string representing the next cursor for
                pagination, if there are more results than the specified `page_size`.
        """
        response = self._http_client.get(
            self._http_client.api_host,
            '/v1/users',
            filter.model_dump(exclude_none=True),
            self._auth_type,
        )

        users_response = ListUsersResponse(**response)
        if users_response.links.next is None:
            return users_response.embedded.users, None

        parsed_url = urlparse(users_response.links.next.href)
        query_params = parse_qs(parsed_url.query)
        next_cursor = query_params.get('cursor', [None])[0]
        return users_response.embedded.users, next_cursor

    @validate_call
    def create_user(self, params: Optional[User] = None) -> User:
        """Create a new user.

        Args:
            params (Optional[User]): An optional `User` object containing the parameters for creating a new user.

        Returns:
            User: A `User` object representing the newly created user.
        """
        response = self._http_client.post(
            self._http_client.api_host,
            '/v1/users',
            params.model_dump(exclude_none=True) if params is not None else None,
            self._auth_type,
        )
        return User(**response)

    @validate_call
    def get_user(self, id: str) -> User:
        """Get a user by ID.

        Args:
            id (str): The ID of the user to retrieve.

        Returns:
            User: The user object.
        """
        response = self._http_client.get(
            self._http_client.api_host, f'/v1/users/{id}', None, self._auth_type
        )
        return User(**response)

    @validate_call
    def update_user(self, id: str, params: User) -> User:
        """Update a user.

        Args:
            id (str): The ID of the user to update.
            params (User): The updated user object.

        Returns:
            User: The updated user object.
        """
        response = self._http_client.patch(
            self._http_client.api_host,
            f'/v1/users/{id}',
            params.model_dump(exclude_none=True),
            self._auth_type,
        )
        return User(**response)

    @validate_call
    def delete_user(self, id: str) -> None:
        """Delete a user.

        Args:
            id (str): The ID of the user to delete.
        """
        self._http_client.delete(
            self._http_client.api_host, f'/v1/users/{id}', None, self._auth_type
        )

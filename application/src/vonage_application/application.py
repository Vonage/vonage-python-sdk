from typing import List, Optional, Tuple

from pydantic import validate_call
from vonage_http_client.http_client import HttpClient

from .requests import ApplicationOptions, ListApplicationsFilter
from .responses import ApplicationData


class Application:
    """Class containing methods for Vonage Application management."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client
        self._auth_type = 'basic'

    @property
    def http_client(self) -> HttpClient:
        """The HTTP client used to make requests to the Users API.

        Returns:
            HttpClient: The HTTP client used to make requests to the Users API.
        """
        return self._http_client

    @validate_call
    def list_applications(
        self, filter: ListApplicationsFilter = ListApplicationsFilter()
    ) -> Tuple[List[ApplicationData], Optional[str]]:
        """"""
        response = self._http_client.get(
            self._http_client.api_host,
            '/v2/applications',
            filter.model_dump(exclude_none=True),
            self._auth_type,
        )

    #     applications_response = ListApplicationsResponse(**response)
    #     if applications_response.links.next is None:
    #         return applications_response.embedded.users, None

    #     parsed_url = urlparse(users_response.links.next.href)
    #     query_params = parse_qs(parsed_url.query)
    #     next_cursor = query_params.get('cursor', [None])[0]
    #     return users_response.embedded.users, next_cursor

    @validate_call
    def create_application(
        self, params: Optional[ApplicationOptions] = None
    ) -> ApplicationData:
        """Create a new application.

        Args:
            params (Optional[ApplicationOptions]): The application options.

        Returns:
            ApplicationData: The created application object.
        """
        response = self._http_client.post(
            self._http_client.api_host,
            '/v2/applications',
            params.model_dump(exclude_none=True) if params is not None else None,
            self._auth_type,
        )
        return ApplicationData(**response)

    @validate_call
    def get_application(self, id: str) -> ApplicationData:
        """Get application info by ID.

        Args:
            id (str): The ID of the application to retrieve.

        Returns:
            ApplicationData: The created application object.
        """
        response = self._http_client.get(
            self._http_client.api_host, f'/v1/users/{id}', None, self._auth_type
        )
        return ApplicationData(**response)

    # @validate_call
    # def update_application(self, id: str, params: User) -> User:
    #     """Update a user.

    #     Args:
    #         id (str): The ID of the user to update.
    #         params (User): The updated user object.

    #     Returns:
    #         User: The updated user object.
    #     """
    #     response = self._http_client.patch(
    #         self._http_client.api_host,
    #         f'/v1/users/{id}',
    #         params.model_dump(exclude_none=True),
    #         self._auth_type,
    #     )
    #     return User(**response)

    # @validate_call
    # def delete_application(self, id: str) -> None:
    #     """Delete an application.

    #     Args:
    #         id (str): The ID of the application to delete.

    #     Returns:
    #         None
    #     """
    #     self._http_client.delete(
    #         self._http_client.api_host, f'/v2/applications/{id}', None, self._auth_type
    #     )

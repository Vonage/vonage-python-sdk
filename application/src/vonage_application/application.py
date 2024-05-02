from typing import List, Optional, Tuple

from pydantic import validate_call
from vonage_http_client.http_client import HttpClient

from .requests import ApplicationConfig, ListApplicationsFilter
from .responses import ApplicationData, ListApplicationsResponse


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
        """List applications.

        By default, returns the first 100 applications and the page index of
            the next page of results, if there are more than 100 applications.

        Args:
            filter (ListApplicationsFilter): The filter object.

        Returns:
            Tuple[List[ApplicationData], Optional[str]]: A tuple containing a
                list of applications and the next page index.
        """
        response = self._http_client.get(
            self._http_client.api_host,
            '/v2/applications',
            filter.model_dump(exclude_none=True),
            self._auth_type,
        )

        applications_response = ListApplicationsResponse(**response)

        if applications_response.page == applications_response.total_pages:
            return applications_response.embedded.applications, None

        next_page = applications_response.page + 1
        return applications_response.embedded.applications, next_page

    @validate_call
    def create_application(
        self, params: Optional[ApplicationConfig] = None
    ) -> ApplicationData:
        """Create a new application.

        Args:
            params (Optional[ApplicationConfig]): Parameters describing the
                application options to set.

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
            self._http_client.api_host, f'/v2/applications/{id}', None, self._auth_type
        )
        return ApplicationData(**response)

    @validate_call
    def update_application(self, id: str, params: ApplicationConfig) -> ApplicationData:
        """Update an application.

        Args:
            id (str): The ID of the application to update.
            params (ApplicationConfig): Parameters describing the
                application options to update.

        Returns:
            ApplicationData: The updated application object.
        """
        response = self._http_client.put(
            self._http_client.api_host,
            f'/v2/applications/{id}',
            params.model_dump(exclude_none=True),
            self._auth_type,
        )
        return ApplicationData(**response)

    @validate_call
    def delete_application(self, id: str) -> None:
        """Delete an application.

        Args:
            id (str): The ID of the application to delete.

        Returns:
            None
        """
        self._http_client.delete(
            self._http_client.api_host, f'/v2/applications/{id}', None, self._auth_type
        )

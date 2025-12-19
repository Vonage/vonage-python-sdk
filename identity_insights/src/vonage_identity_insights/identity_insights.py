from logging import getLogger

from pydantic import validate_call
from vonage_http_client.http_client import HttpClient

from .errors import IdentityInsightsError
from .requests import IdentityInsightsRequest
from .responses import IdentityInsightsResponse

logger = getLogger("vonage_identity_insights")


class IdentityInsights:
    """Calls Vonage's Identity Insights API."""

    def __init__(self, http_client: HttpClient) -> None:
        """Initialize the IdentityInsights client.

        Args:
            http_client (HttpClient): Configured HTTP client used to make
                authenticated requests to the Vonage API.
        """
        self._http_client = http_client
        self._auth_type = "jwt"

    @property
    def http_client(self) -> HttpClient:
        """The HTTP client used to make requests to the Vonage Indentity Insights API.

        Returns:
            HttpClient: The HTTP client used to make requests to the Identity Insights API.
        """
        return self._http_client

    @validate_call
    def get_insights(
        self, insights_request: IdentityInsightsRequest
    ) -> IdentityInsightsResponse:
        """Retrieve identity insights for a phone number.

        Sends an aggregated request to the Identity Insights API and returns
        the results for each requested insight.

        Args:
            insights_request (IdentityInsightsRequest): The request object
                containing the phone number and the set of identity insights
                to retrieve.

        Returns:
            IdentityInsightsResponse: The response object containing the results
                and status of each requested insight.

        Raises:
            IdentityInsightsError: If the API returns an error response in
                `application/problem+json` format.
        """
        payload = insights_request.model_dump(exclude_none=True)

        response = self._http_client.post(
            self._http_client.api_host,
            "/v0.1/identity-insights",
            payload,
            auth_type=self._auth_type,
        )
        self._check_for_error(response)

        return IdentityInsightsResponse(**response)

    def _check_for_error(self, response: dict) -> None:
        """Check whether the API response represents an error.

        The Identity Insights API returns errors using the
        `application/problem+json` format. If such an error is detected, this
        method raises an IdentityInsightsError.

        Args:
            response (dict): Raw response returned by the HTTP client.

        Raises:
            IdentityInsightsError: If the response contains an error payload.
        """
        if "title" in response and "detail" in response:
            error_message = f"Error with the following details: {response}"
            raise IdentityInsightsError(error_message)

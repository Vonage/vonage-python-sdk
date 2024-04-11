from pydantic import validate_call
from vonage_http_client.http_client import HttpClient

from .models.requests import Call
from .models.responses import CreateCallResponse


class Voice:
    """Calls Vonage's Voice API."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    @validate_call
    def create_call(self, params: Call) -> CreateCallResponse:
        """Creates a new call using the Vonage Voice API.

        Args:
            params (Call): The parameters for the call.

        Returns:
            CreateCallResponse: The response object containing information about the created call.
        """
        response = self._http_client.post(
            self._http_client.api_host,
            '/v1/calls',
            params.model_dump(by_alias=True, exclude_none=True),
        )

        return CreateCallResponse(**response)

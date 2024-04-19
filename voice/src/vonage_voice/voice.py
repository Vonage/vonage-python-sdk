from typing import List, Optional, Tuple

from pydantic import validate_call
from vonage_http_client.http_client import HttpClient

from .models.requests import CreateCallRequest, ListCallsFilter
from .models.responses import CallInfo, CallList, CreateCallResponse


class Voice:
    """Calls Vonage's Voice API."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    @validate_call
    def create_call(self, params: CreateCallRequest) -> CreateCallResponse:
        """Creates a new call using the Vonage Voice API.

        Args:
            params (CreateCallRequest): The parameters for the call.

        Returns:
            CreateCallResponse: The response object containing information about the created call.
        """
        response = self._http_client.post(
            self._http_client.api_host,
            '/v1/calls',
            params.model_dump(by_alias=True, exclude_none=True),
        )

        return CreateCallResponse(**response)

    @validate_call
    def list_calls(
        self, filter: ListCallsFilter = ListCallsFilter()
    ) -> Tuple[List[CallInfo], Optional[int]]:
        """Lists calls made with the Vonage Voice API.

        Args:
            filter (ListCallsFilter): The parameters to filter the list of calls.

        Returns:
            Tuple[List[CallInfo], Optional[int]] A tuple containing a list of `CallInfo` objects and the
                value of the `record_index` attribute to get the next page of results, if there
                are more results than the specified `page_size`.
        """
        response = self._http_client.get(
            self._http_client.api_host,
            '/v1/calls',
            filter.model_dump(by_alias=True, exclude_none=True),
        )

        list_response = CallList(**response)
        if list_response.links.next is None:
            return list_response.embedded.calls, None
        next_page_index = list_response.record_index + 1
        return list_response.embedded.calls, next_page_index

    @validate_call
    def get_call(self, call_id: str) -> CallInfo:
        """Gets a call by ID.

        Args:
            call_id (str): The ID of the call to retrieve.

        Returns:
            CallInfo: Object with information about the call.
        """
        response = self._http_client.get(
            self._http_client.api_host, f'/v1/calls/{call_id}'
        )

        return CallInfo(**response)

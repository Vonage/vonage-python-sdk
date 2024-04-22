from typing import List, Optional, Tuple

from pydantic import validate_call
from vonage_http_client.http_client import HttpClient
from vonage_voice.models.ncco import NccoAction

from .models.requests import CreateCallRequest, ListCallsFilter
from .models.responses import CallInfo, CallList, CallMessage, CreateCallResponse


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

    @validate_call
    def transfer_call_ncco(self, uuid: str, ncco: List[NccoAction]) -> None:
        """Transfers a call to a new NCCO.

        Args:
            uuid (str): The UUID of the call to transfer.
            ncco (List[NccoAction]): The new NCCO to transfer the call to.
        """
        serializable_ncco = [
            action.model_dump(by_alias=True, exclude_none=True) for action in ncco
        ]
        self._http_client.put(
            self._http_client.api_host,
            f'/v1/calls/{uuid}',
            {
                'action': 'transfer',
                'destination': {'type': 'ncco', 'ncco': serializable_ncco},
            },
        )

    @validate_call
    def transfer_call_answer_url(self, uuid: str, answer_url: str) -> None:
        """Transfers a call to a new answer URL.

        Args:
            uuid (str): The UUID of the call to transfer.
            answer_url (str): The new answer URL to transfer the call to.
        """
        self._http_client.put(
            self._http_client.api_host,
            f'/v1/calls/{uuid}',
            {'action': 'transfer', 'destination': {'type': 'ncco', 'url': [answer_url]}},
        )

    def hangup(self, uuid: str) -> None:
        """Ends the call for the specified UUID, removing them from it.

        Args:
            uuid (str): The UUID to end the call for.
        """
        self._http_client.put(
            self._http_client.api_host, f'/v1/calls/{uuid}', {'action': 'hangup'}
        )

    def mute(self, uuid: str) -> None:
        """Mutes a call for the specified UUID.

        Args:
            uuid (str): The UUID to mute the call for.
        """
        self._http_client.put(
            self._http_client.api_host, f'/v1/calls/{uuid}', {'action': 'mute'}
        )

    def unmute(self, uuid: str) -> None:
        """Unmutes a call for the specified UUID.

        Args:
            uuid (str): The UUID to unmute the call for.
        """
        self._http_client.put(
            self._http_client.api_host, f'/v1/calls/{uuid}', {'action': 'unmute'}
        )

    def earmuff(self, uuid: str) -> None:
        """Earmuffs a call for the specified UUID (prevents them from hearing audio).

        Args:
            uuid (str): The UUID you want to prevent from hearing audio.
        """
        self._http_client.put(
            self._http_client.api_host, f'/v1/calls/{uuid}', {'action': 'earmuff'}
        )

    def unearmuff(self, uuid: str) -> None:
        """Allows the specified UUID to hear audio.

        Args:
            uuid (str): The UUID you want to to allow to hear audio.
        """
        self._http_client.put(
            self._http_client.api_host, f'/v1/calls/{uuid}', {'action': 'unearmuff'}
        )

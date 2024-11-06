from typing import Optional

from pydantic import validate_call
from vonage_http_client.http_client import HttpClient
from vonage_numbers.errors import NumbersError

from .requests import (
    ListOwnedNumbersFilter,
    NumberParams,
    SearchAvailableNumbersFilter,
    UpdateNumberParams,
)
from .responses import AvailableNumber, NumbersStatus, OwnedNumber


class Numbers:
    """Class containing methods for Vonage Application management."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client
        self._auth_type = 'basic'
        self._sent_data_type = 'form'

    @property
    def http_client(self) -> HttpClient:
        """The HTTP client used to make requests to the Numbers API.

        Returns:
            HttpClient: The HTTP client used to make requests to the Numbers API.
        """
        return self._http_client

    @validate_call
    def list_owned_numbers(
        self, filter: ListOwnedNumbersFilter = ListOwnedNumbersFilter()
    ) -> tuple[list[OwnedNumber], int, Optional[int]]:
        """List numbers you own.

        By default, returns the first 100 numbers and the page index of
            the next page of results, if there are more than 100 numbers.

        Args:
            filter (ListOwnedNumbersFilter): The filter object.

        Returns:
            tuple[list[OwnedNumber], int, Optional[int]]: A tuple containing a
                list of owned numbers, the total count of owned phone numbers
                and the next page index, if applicable.
                i.e.
                number_list: list[OwnedNumber], count: int, next_page_index: Optional[int])
        """
        response = self._http_client.get(
            self._http_client.rest_host,
            '/account/numbers',
            filter.model_dump(exclude_none=True),
            self._auth_type,
        )

        index = filter.index or 1
        page_size = filter.size

        numbers = []
        try:
            for number in response['numbers']:
                numbers.append(OwnedNumber(**number))
        except KeyError:
            return [], 0, None

        count = response['count']
        if count > page_size * index:
            return numbers, count, index + 1
        return numbers, count, None

    @validate_call
    def search_available_numbers(
        self, filter: SearchAvailableNumbersFilter
    ) -> tuple[list[AvailableNumber], int, Optional[int]]:
        """Search for available numbers to buy.

        By default, returns the first 100 numbers and the page index of
            the next page of results, if there are more than 100 numbers.

        Args:
            filter (SearchAvailableNumbersFilter): The filter object.

        Returns:
            tuple[list[AvailableNumber], int, Optional[int]]: A tuple containing a
                list of available numbers, the total count of available phone numbers
                and the next page index, if applicable.
                i.e.
                number_list: list[AvailableNumber], count: int, next_page_index: Optional[int])
        """
        response = self._http_client.get(
            self._http_client.rest_host,
            '/number/search',
            filter.model_dump(exclude_none=True),
            self._auth_type,
        )

        index = filter.index or 1
        page_size = filter.size

        numbers = []
        try:
            for number in response['numbers']:
                numbers.append(AvailableNumber(**number))
        except KeyError:
            return [], 0, None

        count = response['count']
        if count > page_size * index:
            return numbers, count, index + 1
        return numbers, count, None

    @validate_call
    def buy_number(self, params: NumberParams) -> NumbersStatus:
        """Buy a number.

        Args:
            params (NumberParams): The number parameters.

        Returns:
            NumbersStatus: The status of the number purchase.
        """
        response = self._http_client.post(
            self._http_client.rest_host,
            '/number/buy',
            params.model_dump(exclude_none=True),
            self._auth_type,
            self._sent_data_type,
        )

        self._check_for_error(response)
        return NumbersStatus(**response)

    @validate_call
    def cancel_number(self, params: NumberParams) -> NumbersStatus:
        """Cancel a number.

        Args:
            params (NumberParams): The number parameters.

        Returns:
            NumbersStatus: The status of the number cancellation.
        """
        response = self._http_client.post(
            self._http_client.rest_host,
            '/number/cancel',
            params.model_dump(exclude_none=True),
            self._auth_type,
            self._sent_data_type,
        )

        self._check_for_error(response)
        return NumbersStatus(**response)

    @validate_call
    def update_number(self, params: UpdateNumberParams) -> NumbersStatus:
        """Update a number.

        Args:
            params (UpdateNumberParams): The number parameters.

        Returns:
            NumbersStatus: The status of the number update.
        """
        response = self._http_client.post(
            self._http_client.rest_host,
            '/number/update',
            params.model_dump(exclude_none=True),
            self._auth_type,
            self._sent_data_type,
        )

        self._check_for_error(response)
        return NumbersStatus(**response)

    def _check_for_error(self, response_data):
        if response_data['error-code'] != '200':
            raise NumbersError(
                f'Numbers API operation failed: {response_data["error-code"]} {response_data["error-code-label"]}'
            )

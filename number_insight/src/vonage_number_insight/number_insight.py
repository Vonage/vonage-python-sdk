from logging import getLogger

from pydantic import validate_call
from vonage_http_client.http_client import HttpClient

from .errors import NumberInsightError
from .requests import (
    AdvancedAsyncInsightRequest,
    AdvancedSyncInsightRequest,
    BasicInsightRequest,
    StandardInsightRequest,
)
from .responses import (
    AdvancedAsyncInsightResponse,
    AdvancedSyncInsightResponse,
    BasicInsightResponse,
    StandardInsightResponse,
)

logger = getLogger('vonage_number_insight')


class NumberInsight:
    """Calls Vonage's Number Insight API."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client
        self._auth_type = 'body'

    @property
    def http_client(self) -> HttpClient:
        """The HTTP client used to make requests to the Vonage Number Insight API.

        Returns:
            HttpClient: The HTTP client used to make requests to the Number Insight API.
        """
        return self._http_client

    @validate_call
    def get_basic_info(self, options: BasicInsightRequest) -> BasicInsightResponse:
        """Get basic number insight information about a phone number.

        Args:
            Options (BasicInsightRequest): The options for the request. The `number` paramerter
                is required, and the `country_code` parameter is optional.

        Returns:
            BasicInsightResponse: The response object containing the basic number insight
                information about the phone number.
        """
        response = self._http_client.get(
            self._http_client.api_host,
            '/ni/basic/json',
            params=options.model_dump(exclude_none=True),
            auth_type=self._auth_type,
        )
        self._check_for_error(response)

        return BasicInsightResponse(**response)

    @validate_call
    def get_standard_info(
        self, options: StandardInsightRequest
    ) -> StandardInsightResponse:
        """Get standard number insight information about a phone number.

        Args:
            Options (StandardInsightRequest): The options for the request. The `number` paramerter
                is required, and the `country_code` and `cnam` parameters are optional.

        Returns:
            StandardInsightResponse: The response object containing the standard number insight
                information about the phone number.
        """
        response = self._http_client.get(
            self._http_client.api_host,
            '/ni/standard/json',
            params=options.model_dump(exclude_none=True),
            auth_type=self._auth_type,
        )
        self._check_for_error(response)

        return StandardInsightResponse(**response)

    @validate_call
    def get_advanced_info_async(
        self, options: AdvancedAsyncInsightRequest
    ) -> AdvancedAsyncInsightResponse:
        """Get advanced number insight information about a phone number asynchronously.

        Args:
            Options (AdvancedAsyncInsightRequest): The options for the request. You must provide values
                for the `callback` and `number` parameters. The `country_code` and `cnam` parameters
                are optional.

        Returns:
            AdvancedAsyncInsightResponse: The response object containing the advanced number insight
                information about the phone number.
        """
        response = self._http_client.get(
            self._http_client.api_host,
            '/ni/advanced/async/json',
            params=options.model_dump(exclude_none=True),
            auth_type=self._auth_type,
        )
        self._check_for_error(response)

        return AdvancedAsyncInsightResponse(**response)

    @validate_call
    def get_advanced_info_sync(
        self, options: AdvancedSyncInsightRequest
    ) -> AdvancedSyncInsightResponse:
        """Get advanced number insight information about a phone number synchronously.

        Args:
            Options (AdvancedSyncInsightRequest): The options for the request. The `number` parameter
                is required, and the `country_code` and `cnam` parameters are optional.

        Returns:
            AdvancedSyncInsightResponse: The response object containing the advanced number insight
                information about the phone number.
        """
        response = self._http_client.get(
            self._http_client.api_host,
            '/ni/advanced/json',
            params=options.model_dump(exclude_none=True),
            auth_type=self._auth_type,
        )
        self._check_for_error(response)

        return AdvancedSyncInsightResponse(**response)

    def _check_for_error(self, response: dict) -> None:
        """Check for an error in the response from the Number Insight API.

        Args:
            response (dict): The response from the Number Insight API.

        Raises:
            NumberInsightError: If the response contains an error.
        """
        if response['status'] != 0:
            if response['status'] in {43, 44, 45}:
                logger.warning(
                    'Live mobile lookup not returned. Not all parameters are available.'
                )
                return
            logger.warning(
                f'Error using the Number Insight API. Response received: {response}'
            )
            error_message = f'Error with the following details: {response}'
            raise NumberInsightError(error_message)

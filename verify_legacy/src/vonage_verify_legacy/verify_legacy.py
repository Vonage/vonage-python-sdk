from typing import Optional, Union

from pydantic import Field, validate_call
from vonage_http_client.http_client import HttpClient

from .errors import VerifyError
from .requests import BaseVerifyRequest, Psd2Request, VerifyRequest
from .responses import (
    CheckCodeResponse,
    NetworkUnblockStatus,
    StartVerificationResponse,
    VerifyControlStatus,
    VerifyStatus,
)


class VerifyLegacy:
    """Calls Vonage's Legacy Verify API. If you are just starting to use the Verify API,
    please use the `Verify` class instead.

    This class provides methods to interact with Vonage's Legacy Verify API for verifying
    users.

    Args:
        http_client (HttpClient): The HTTP client used to make requests to the Verify API.

    Raises:
        VerifyError: If an error is found in the response.
    """

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client
        self._sent_data_type = 'form'
        self._auth_type = 'body'

    @property
    def http_client(self) -> HttpClient:
        """The HTTP client used to make requests to the Verify API.

        Returns:
            HttpClient: The HTTP client used to make requests to the Verify API.
        """
        return self._http_client

    @validate_call
    def start_verification(
        self, verify_request: VerifyRequest
    ) -> StartVerificationResponse:
        """Start a verification process.

        Args:
            verify_request (VerifyRequest): The verification request object.

        Returns:
            StartVerificationResponse: The response object containing the verification result.
        """
        return self._make_verify_request(verify_request)

    @validate_call
    def start_psd2_verification(
        self, verify_request: Psd2Request
    ) -> StartVerificationResponse:
        """Start a PSD2 verification process.

        Args:
            verify_request (Psd2Request): The PSD2 verification request object.

        Returns:
            StartVerificationResponse: The response object containing the verification result.
        """
        return self._make_verify_request(verify_request)

    @validate_call
    def check_code(self, request_id: str, code: str) -> CheckCodeResponse:
        """Check a verification code.

        Args:
            request_id (str): The request ID.
            code (str): The verification code.

        Returns:
            CheckCodeResponse: The response object containing the verification result.
        """
        response = self._http_client.post(
            self._http_client.api_host,
            '/verify/check/json',
            {'request_id': request_id, 'code': code},
            self._auth_type,
            self._sent_data_type,
        )
        self._check_for_error(response)
        return CheckCodeResponse(**response)

    @validate_call
    def search(
        self, request: Union[str, list[str]]
    ) -> Union[VerifyStatus, list[VerifyStatus]]:
        """Search for past or current verification requests.

        Args:
            request (str | list[str]): The request ID, or a list of request IDs.

        Returns:
            Union[VerifyStatus, list[VerifyStatus]]: Either the response object
                containing the verification result, or a list of response objects.
        """
        params = {}
        if type(request) == str:
            params['request_id'] = request
        elif type(request) == list:
            params['request_ids'] = request

        response = self._http_client.get(
            self._http_client.api_host, '/verify/search/json', params, self._auth_type
        )

        if 'verification_requests' in response:
            parsed_response = []
            for verification_request in response['verification_requests']:
                parsed_response.append(VerifyStatus(**verification_request))
            return parsed_response
        elif 'error_text' in response:
            error_message = f'Error with the following details: {response}'
            raise VerifyError(error_message)
        else:
            parsed_response = VerifyStatus(**response)
            return parsed_response

    @validate_call
    def cancel_verification(self, request_id: str) -> VerifyControlStatus:
        """Cancel a verification request.

        Args:
            request_id (str): The request ID.

        Returns:
            VerifyControlStatus: The response object containing details of the submitted
                verification control.
        """
        response = self._http_client.post(
            self._http_client.api_host,
            '/verify/control/json',
            {'request_id': request_id, 'cmd': 'cancel'},
            self._auth_type,
            self._sent_data_type,
        )
        self._check_for_error(response)

        return VerifyControlStatus(**response)

    @validate_call
    def trigger_next_event(self, request_id: str) -> VerifyControlStatus:
        """Trigger the next event in the verification process.

        Args:
            request_id (str): The request ID.

        Returns:
            VerifyControlStatus: The response object containing details of the submitted
                verification control.
        """
        response = self._http_client.post(
            self._http_client.api_host,
            '/verify/control/json',
            {'request_id': request_id, 'cmd': 'trigger_next_event'},
            self._auth_type,
            self._sent_data_type,
        )
        self._check_for_error(response)

        return VerifyControlStatus(**response)

    @validate_call
    def request_network_unblock(
        self, network: str, unblock_duration: Optional[int] = Field(None, ge=0, le=86400)
    ) -> NetworkUnblockStatus:
        """Request to unblock a network that has been blocked due to potential fraud
        detection.

        Note: The network unblock feature is switched off by default.
            Please contact Sales to enable the Network Unblock API for your account.

        Args:
            network (str): The network code of the network to unblock.
            unblock_duration (int, optional): How long (in seconds) to unblock the network for.
        """
        response = self._http_client.post(
            self._http_client.api_host,
            '/verify/network-unblock',
            {'network': network, 'duration': unblock_duration},
            self._auth_type,
        )

        return NetworkUnblockStatus(**response)

    def _make_verify_request(
        self, verify_request: BaseVerifyRequest
    ) -> StartVerificationResponse:
        """Make a verify request.

        This method makes a verify request to the Vonage Verify API.

        Args:
            verify_request (BaseVerifyRequest): The verify request object.

        Returns:
            VerifyResponse: The response object containing the verification result.
        """
        if type(verify_request) == VerifyRequest:
            request_path = '/verify/json'
        elif type(verify_request) == Psd2Request:
            request_path = '/verify/psd2/json'

        response = self._http_client.post(
            self._http_client.api_host,
            request_path,
            verify_request.model_dump(by_alias=True, exclude_none=True),
            self._auth_type,
            self._sent_data_type,
        )
        self._check_for_error(response)

        return StartVerificationResponse(**response)

    def _check_for_error(self, response: dict) -> None:
        """Check for error in the response.

        This method checks if the response contains a non-zero status code
            and raises a VerifyError if this is found.

        Args:
            response (dict): The response object.

        Raises:
            VerifyError: If an error is found in the response.
        """
        if int(response['status']) != 0:
            error_message = f'Error with the following details: {response}'
            raise VerifyError(error_message)

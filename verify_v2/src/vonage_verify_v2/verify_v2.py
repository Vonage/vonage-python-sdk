from typing import List, Optional, Union

from pydantic import validate_call
from vonage_http_client.http_client import HttpClient

from .errors import VerifyError
from .requests import (
    VerifyRequest,
    SilentAuthWorkflow,
    SmsWorkflow,
    WhatsappWorkflow,
    VoiceWorkflow,
    EmailWorkflow,
)
from .responses import (
    CheckCodeResponse,
    StartVerificationResponse,
    VerifyControlStatus,
    VerifyStatus,
)


class Verify:
    """Calls Vonage's Verify V2 API."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    @validate_call
    def start_verification(
        self, verify_request: VerifyRequest
    ) -> StartVerificationResponse:
        """Start a verification process.

        Args:
            verify_request (VerifyRequest): The verification request object.

        Returns:
            StartVerificationResponse: The response object containing the `request_id`.
                If requesting Silent Authentication, it will also contain a `check_url` field.
        """
        response = self._http_client.post(
            self._http_client.api_host,
            '/v2/verify',
            verify_request.model_dump(by_alias=True, exclude_none=True),
        )

        return StartVerificationResponse(**response)

    ####################################################################################################

    ####################################################################################################

    ####################################################################################################

    ####################################################################################################

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
    def trigger_next_workflow(self, request_id: str) -> VerifyControlStatus:
        """Trigger the next workflow event in the verification process.

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

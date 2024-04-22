from pydantic import validate_call
from vonage_http_client.http_client import HttpClient

from .requests import VerifyRequest
from .responses import CheckCodeResponse, StartVerificationResponse


class VerifyV2:
    """Calls Vonage's Verify V2 API."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    @property
    def http_client(self) -> HttpClient:
        """The HTTP client used to make requests to the Verify V2 API.

        Returns:
            HttpClient: The HTTP client used to make requests to the Verify V2 API.
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
            StartVerificationResponse: The response object containing the `request_id`.
                If requesting Silent Authentication, it will also contain a `check_url` field.
        """
        response = self._http_client.post(
            self._http_client.api_host,
            '/v2/verify',
            verify_request.model_dump(by_alias=True, exclude_none=True),
        )

        return StartVerificationResponse(**response)

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
            self._http_client.api_host, f'/v2/verify/{request_id}', {'code': code}
        )
        return CheckCodeResponse(**response)

    @validate_call
    def cancel_verification(self, request_id: str) -> None:
        """Cancel a verification request.

        Args:
            request_id (str): The request ID.
        """
        self._http_client.delete(self._http_client.api_host, f'/v2/verify/{request_id}')

    @validate_call
    def trigger_next_workflow(self, request_id: str) -> None:
        """Trigger the next workflow event in the list of workflows passed in when making the
        request.

        Args:
            request_id (str): The request ID.
        """
        self._http_client.post(
            self._http_client.api_host,
            f'/v2/verify/{request_id}/next_workflow',
        )

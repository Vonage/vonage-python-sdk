from pydantic import validate_call
from vonage_http_client.http_client import HttpClient

from .requests import BaseVerifyRequest, Psd2Request, VerifyRequest
from .responses import VerifyResponse


class Verify:
    """Calls Vonage's Verify API."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client
        self._sent_post_data_type = 'form'
        self._sent_get_data_type = 'query_params'
        self._auth_type = 'body'

    @validate_call
    def start_verification(self, verify_request: VerifyRequest) -> VerifyResponse:
        """Start a verification process."""
        return self._make_verify_request(verify_request)

    @validate_call
    def start_psd2_verification(self, verify_request: Psd2Request) -> VerifyResponse:
        """Start a PSD2 verification process."""
        return self._make_verify_request(verify_request)

    def _make_verify_request(self, verify_request: BaseVerifyRequest) -> VerifyResponse:
        if type(verify_request) == VerifyRequest:
            request_path = '/verify/json'
        elif type(verify_request) == Psd2Request:
            request_path = '/verify/psd2/json'

        response = self._http_client.post(
            self._http_client.api_host,
            request_path,
            verify_request.model_dump(by_alias=True),
            self._auth_type,
            self._sent_post_data_type,
        )
        return VerifyResponse(**response)

    # @validate_call
    # def send(self, message: SmsMessage) -> SmsResponse:
    #     """Send an SMS message."""
    #     response = self._http_client.post(
    #         self._http_client.rest_host,
    #         '/sms/json',
    #         message.model_dump(by_alias=True),
    #         self._auth_type,
    #         self._sent_data_type,
    #     )

    #     if int(response['message-count']) > 1:
    #         self._check_for_partial_failure(response)
    #     else:
    #         self._check_for_error(response)
    #     return SmsResponse(**response)

    # def _check_for_partial_failure(self, response_data):
    #     successful_messages = 0
    #     total_messages = int(response_data['message-count'])

    #     for message in response_data['messages']:
    #         if message['status'] == '0':
    #             successful_messages += 1
    #     if successful_messages < total_messages:
    #         raise PartialFailureError(response_data)

    # def _check_for_error(self, response_data):
    #     message = response_data['messages'][0]
    #     if int(message['status']) != 0:
    #         raise SmsError(
    #             f'Sms.send_message method failed with error code {message["status"]}: {message["error-text"]}'
    #         )

    # @validate_call
    # def submit_sms_conversion(
    #     self, message_id: str, delivered: bool = True, timestamp: datetime = None
    # ):
    #     """
    #     Note: Not available without having this feature manually enabled on your account.

    #     Notifies Vonage that an SMS was successfully received.

    #     This method is used to submit conversion data about SMS messages that were successfully delivered.
    #     If you are using the Verify API for two-factor authentication (2FA), this information is sent to Vonage automatically,
    #     so you do not need to use this method for 2FA messages.

    #     Args:
    #         message_id (str): The `message-id` returned by the `Sms.send` call.
    #         delivered (bool, optional): Set to `True` if the user replied to the message you sent. Otherwise, set to `False`.
    #         timestamp (datetime, optional): A `datetime` object containing the time the SMS arrived.
    #     """
    #     params = {
    #         'message-id': message_id,
    #         'delivered': delivered,
    #         'timestamp': (timestamp or datetime.now(timezone.utc)).strftime(
    #             '%Y-%m-%d %H:%M:%S'
    #         ),
    #     }
    #     self._http_client.post(
    #         self._http_client.api_host,
    #         '/conversions/sms',
    #         params,
    #         self._auth_type,
    #         self._sent_data_type,
    #     )

from datetime import datetime, timezone

from pydantic import validate_call
from vonage_http_client.http_client import HttpClient

from .errors import PartialFailureError, SmsError
from .requests import SmsMessage
from .responses import SmsResponse


class Sms:
    """Calls Vonage's SMS API.

    Args:
        http_client (HttpClient): The HTTP client used to make requests to the SMS API.

    Raises:
        PartialFailureError: Raised when not all messages were sent successfully.
        SmsError: Raised when the SMS API returns an error.
    """

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client
        self._sent_data_type = 'form'
        if self._http_client.auth._signature_secret:
            self._auth_type = 'signature'
        else:
            self._auth_type = 'basic'

    @property
    def http_client(self) -> HttpClient:
        """The HTTP client used to make requests to the SMS API.

        Returns:
            HttpClient: The HTTP client used to make requests to the SMS API.
        """
        return self._http_client

    @validate_call
    def send(self, message: SmsMessage) -> SmsResponse:
        """Send an SMS message.

        Args:
            message (SmsMessage): The message to send.

        Returns:
            SmsResponse: The response from the API.

        Raises:
            PartialFailureError: Raised when not all messages were sent successfully.
            SmsError: Raised when the SMS API returns an error.

        Example:
            >>> sms = Sms(http_client)
            >>> message = SmsMessage(
            ...     to='1234567890',
            ...     from_='9876543210',
            ...     text='Hello, World!',
            ... )
            >>> response = sms.send(message)
        """
        response = self._http_client.post(
            self._http_client.rest_host,
            '/sms/json',
            message.model_dump(by_alias=True),
            self._auth_type,
            self._sent_data_type,
        )

        if int(response['message-count']) > 1:
            self._check_for_partial_failure(response)
        else:
            self._check_for_error(response)
        return SmsResponse(**response)

    def _check_for_partial_failure(self, response_data):
        successful_messages = 0
        total_messages = int(response_data['message-count'])

        for message in response_data['messages']:
            if message['status'] == '0':
                successful_messages += 1
        if successful_messages < total_messages:
            raise PartialFailureError(response_data)

    def _check_for_error(self, response_data):
        message = response_data['messages'][0]
        if int(message['status']) != 0:
            raise SmsError(
                f'Sms.send_message method failed with error code {message["status"]}: {message["error-text"]}'
            )

    @validate_call
    def submit_sms_conversion(
        self, message_id: str, delivered: bool = True, timestamp: datetime = None
    ) -> None:
        """
        Note: Not available without having this feature manually enabled on your account.

        Notifies Vonage that an SMS was successfully received.

        This method is used to submit conversion data about SMS messages that were successfully delivered.
        If you are using the Verify API for two-factor authentication (2FA), this information is sent to Vonage automatically,
        so you do not need to use this method for 2FA messages.

        Args:
            message_id (str): The `message-id` returned by the `Sms.send` call.
            delivered (bool, optional): Set to `True` if the user replied to the message you sent. Otherwise, set to `False`.
            timestamp (datetime, optional): A `datetime` object containing the time the SMS arrived.
        """
        params = {
            'message-id': message_id,
            'delivered': delivered,
            'timestamp': (timestamp or datetime.now(timezone.utc)).strftime(
                '%Y-%m-%d %H:%M:%S'
            ),
        }
        self._http_client.post(
            self._http_client.api_host,
            '/conversions/sms',
            params,
            self._auth_type,
            self._sent_data_type,
        )

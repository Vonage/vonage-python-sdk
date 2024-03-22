from copy import deepcopy

from pydantic import validate_call
from vonage_http_client.http_client import HttpClient

from .errors import PartialFailureError, SmsError
from .models import SmsMessage
from .responses import MessageResponse, SmsResponse


class Sms:
    """Calls Vonage's SMS API."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = deepcopy(http_client)
        self._body_type = 'data'
        if self._http_client._auth._signature_secret:
            self._auth_type = 'signature'
        else:
            self._auth_type = 'basic'

    @validate_call
    def send(self, message: SmsMessage) -> SmsResponse:
        """Send an SMS message."""
        response = self._http_client.post(
            self._http_client.rest_host,
            '/sms/json',
            message.model_dump(by_alias=True),
            self._auth_type,
            self._body_type,
        )

        if int(response['message-count']) > 1:
            self.check_for_partial_failure(response)
        else:
            self.check_for_error(response)

        messages = []
        for message in response['messages']:
            messages.append(MessageResponse(**message))

        return SmsResponse(message_count=response['message-count'], messages=messages)

    def check_for_partial_failure(self, response_data):
        successful_messages = 0
        total_messages = int(response_data['message-count'])

        for message in response_data['messages']:
            if message['status'] == '0':
                successful_messages += 1
        if successful_messages < total_messages:
            raise PartialFailureError(response_data)

    def check_for_error(self, response_data):
        message = response_data['messages'][0]
        if int(message['status']) != 0:
            raise SmsError(
                f'Sms.send_message method failed with error code {message["status"]}: {message["error-text"]}'
            )

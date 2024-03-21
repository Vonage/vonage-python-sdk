from copy import deepcopy
from dataclasses import dataclass
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator, validate_call
from vonage_http_client.http_client import HttpClient

from .errors import PartialFailureError, SmsError


class SmsMessage(BaseModel):
    to: str
    from_: str = Field(..., alias="from")
    text: str
    sig: Optional[str] = Field(None, min_length=16, max_length=60)
    client_ref: Optional[str] = Field(None, alias="client-ref", max_length=100)
    type: Optional[Literal['text', 'binary', 'unicode']] = None
    ttl: Optional[int] = Field(None, ge=20000, le=604800000)
    status_report_req: Optional[bool] = Field(None, alias='status-report-req')
    callback: Optional[str] = Field(None, max_length=100)
    message_class: Optional[int] = Field(None, alias='message-class', ge=0, le=3)
    body: Optional[str] = None
    udh: Optional[str] = None
    protocol_id: Optional[int] = Field(None, alias='protocol-id', ge=0, le=255)
    account_ref: Optional[str] = Field(None, alias='account-ref')
    entity_id: Optional[str] = Field(None, alias='entity-id')
    content_id: Optional[str] = Field(None, alias='content-id')

    @field_validator('body', 'udh')
    @classmethod
    def validate_body(cls, value, values):
        if 'type' not in values or not values['type'] == 'binary':
            raise ValueError(
                'This parameter can only be set when the "type" parameter is set to "binary".'
            )
        if values['type'] == 'binary' and not value:
            raise ValueError('This parameter is required for binary messages.')


@dataclass
class MessageResponse:
    to: str
    message_id: str
    status: str
    remaining_balance: str
    message_price: str
    network: str
    client_ref: Optional[str] = None
    account_ref: Optional[str] = None


@dataclass
class SmsResponse:
    message_count: str
    messages: List[MessageResponse]


class Sms:
    """Calls Vonage's SMS API."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = deepcopy(http_client)
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

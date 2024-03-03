from copy import deepcopy
from dataclasses import dataclass
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field, field_validator, validate_call
from vonage_http_client.http_client import HttpClient
from vonage_sms.errors import SmsError


class SmsMessage(BaseModel):
    to: str
    from_: str = Field(..., alias="from")
    text: str
    type: Optional[str] = None
    sig: Optional[str] = Field(None, min_length=16, max_length=60)
    status_report_req: Optional[int] = Field(
        None,
        alias="status-report-req",
        description="Set to 1 to receive a Delivery Receipt",
    )
    client_ref: Optional[str] = Field(
        None, alias="client-ref", description="Your own reference. Up to 40 characters."
    )
    network_code: Optional[str] = Field(
        None,
        alias="network-code",
        description="A 4-5 digit number that represents the mobile carrier network code",
    )


@dataclass
class SmsResponse:
    id: str


class Sms:
    """Calls Vonage's SMS API."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = deepcopy(http_client)
        self._auth_type = 'basic'

    @validate_call
    def send(self, message: SmsMessage) -> SmsResponse:
        """Send an SMS message."""
        response = self._http_client.post(
            self._http_client.api_host,
            '/v2/ni',
            message.model_dump(),
            self._auth_type,
        )

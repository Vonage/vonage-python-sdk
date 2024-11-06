from typing import Literal, Optional

from pydantic import BaseModel, Field, ValidationInfo, field_validator, model_validator


class SmsMessage(BaseModel):
    """Message object containing the data and options for an SMS message.

    Args:
        to (str): The recipient's phone number in E.164 format.
        from_ (str): The name or number the message should be sent from. If a number, it
            must be specified in E.164 format, without a leading `+` or `00`. If using
            an alphanumeric sender IDs, spaces will be ignored. Sender IDs are not
            supported in all countries.
        text (str): The message body. If your message contains characters that can be
            encoded according to the GSM Standard and Extended tables then you can set
            `type` to `text`. If your message contains characters outside this range,
            you will need to set `type` to `unicode`.
        sig (str, Optional): The hash of the request parameters in alphabetical order, a
            timestamp and the signature secret.
        client_ref (str, Optional): A client reference string you can optionally include.
        type (str, Optional): The format of the message body. Can be 'text', 'binary', or
            'unicode'.
        ttl (int, Optional): The duration in milliseconds the delivery of an SMS will be
            attempted.
        status_report_req (bool, Optional): Boolean indicating if you like to receive a
            delivery receipt.
        callback (str, Optional): The webhook endpoint the delivery receipt for this SMS
            is sent to. This parameter overrides the webhook endpoint you set in the
            Vonage Developer Dashboard.
        message_class (int, Optional): The Data Coding Scheme value of the message.
        body (str, Optional): Hex-encoded binary data. Depends on `type` having the value
            `binary`.
        udh (str, Optional): The hex-encoded user data header for binary messages.
        protocol_id (int, Optional): The protocol identifier for binary messages. Ensure
            that the value is aligned with `udh`.
        account_ref (str, Optional): An optional string used to identify separate
            accounts using the SMS endpoint for billing purposes. To use this feature,
            please email support.
        entity_id (str, Optional): A string parameter that satisfies regulatory
            requirements when sending an SMS to specific countries.
        content_id (str, Optional): A string parameter that satisfies regulatory
            requirements when sending an SMS to specific countries.
    """

    to: str
    from_: str = Field(..., serialization_alias='from')
    text: str
    sig: Optional[str] = Field(None, min_length=16, max_length=60)
    client_ref: Optional[str] = Field(
        None, serialization_alias='client-ref', max_length=100
    )
    type: Optional[Literal['text', 'binary', 'unicode']] = None
    ttl: Optional[int] = Field(None, ge=20000, le=604800000)
    status_report_req: Optional[bool] = Field(
        None, serialization_alias='status-report-req'
    )
    callback: Optional[str] = Field(None, max_length=100)
    message_class: Optional[int] = Field(
        None, serialization_alias='message-class', ge=0, le=3
    )
    body: Optional[str] = None
    udh: Optional[str] = None
    protocol_id: Optional[int] = Field(
        None, serialization_alias='protocol-id', ge=0, le=255
    )
    account_ref: Optional[str] = Field(None, serialization_alias='account-ref')
    entity_id: Optional[str] = Field(None, serialization_alias='entity-id')
    content_id: Optional[str] = Field(None, serialization_alias='content-id')

    @field_validator('body', 'udh')
    @classmethod
    def validate_body(cls, value, info: ValidationInfo):
        data = info.data
        if 'type' not in data or not data['type'] == 'binary':
            raise ValueError(
                'This parameter can only be set when the "type" parameter is set to "binary".'
            )
        return value

    @model_validator(mode='after')
    def validate_type(self) -> 'SmsMessage':
        if self.type == 'binary' and self.body is None and self.udh is None:
            raise ValueError('This parameter is required for binary messages.')
        return self

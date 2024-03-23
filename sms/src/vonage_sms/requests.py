from typing import Literal, Optional

from pydantic import BaseModel, Field, ValidationInfo, field_validator, model_validator


class SmsMessage(BaseModel):
    """Message object containing the data and options for an SMS message."""

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

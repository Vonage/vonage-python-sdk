from typing import List, Optional

from pydantic import BaseModel, Field


class OwnedNumber(BaseModel):
    country: Optional[str] = Field(None, min_length=2, max_length=2)
    msisdn: Optional[str] = None
    mo_http_url: Optional[str] = Field(None, validation_alias='moHttpUrl')
    type: Optional[str] = None
    features: Optional[List[str]] = None
    messages_callback_type: Optional[str] = Field(
        None, validation_alias='messagesCallbackType'
    )
    messages_callback_value: Optional[str] = Field(
        None, validation_alias='messagesCallbackValue'
    )
    voice_callback_type: Optional[str] = Field(None, validation_alias='voiceCallbackType')
    voice_callback_value: Optional[str] = Field(
        None, validation_alias='voiceCallbackValue'
    )
    app_id: Optional[str] = None


class AvailableNumber(BaseModel):
    country: Optional[str] = Field(None, min_length=2, max_length=2)
    msisdn: Optional[str] = None
    type: Optional[str] = None
    cost: Optional[str] = None
    features: Optional[List[str]] = None


class NumbersStatus(BaseModel):
    error_code: str = Field(None, validation_alias='error-code')
    error_code_label: str = Field(None, validation_alias='error-code-label')

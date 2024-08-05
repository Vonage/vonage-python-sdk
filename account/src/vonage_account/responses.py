from typing import Optional

from pydantic import BaseModel, Field


class TopUpResponse(BaseModel):
    error_code: Optional[str] = Field(None, validation_alias='error-code')
    error_code_label: Optional[str] = Field(None, validation_alias='error-code-label')


class SettingsResponse(BaseModel):
    mo_callback_url: Optional[str] = Field(None, validation_alias='mo-callback-url')
    dr_callback_url: Optional[str] = Field(None, validation_alias='dr-callback-url')
    max_outbound_request: Optional[int] = Field(
        None, validation_alias='max-outbound-request'
    )
    max_inbound_request: Optional[int] = Field(
        None, validation_alias='max-inbound-request'
    )
    max_calls_per_second: Optional[int] = Field(
        None, validation_alias='max-calls-per-second'
    )

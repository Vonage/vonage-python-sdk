from typing import Optional

from pydantic import BaseModel, Field


class Balance(BaseModel):
    """Model for the balance of a Vonage account.

    Args:
        value (float): The balance of the account in EUR.
        auto_reload (bool, Optional): Whether the account has auto-reload enabled.
    """

    value: float
    auto_reload: Optional[bool] = Field(None, validation_alias='autoReload')


class TopUpResponse(BaseModel):
    """Model for a response to a top-up request.

    Args:
        error_code (str, Optional): The error code.
        error_code_label (str, Optional): The error code label.
    """

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


class VonageApiSecret(BaseModel):
    id: str
    created_at: str

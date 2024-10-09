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
        error_code (str, Optional): Code describing the operation status.
        error_code_label (str, Optional): Description of the operation status.
    """

    error_code: Optional[str] = Field(None, validation_alias='error-code')
    error_code_label: Optional[str] = Field(None, validation_alias='error-code-label')


class SettingsResponse(BaseModel):
    """Model for a response to a settings update request.

    Args:
        mo_callback_url (str, Optional): The URL for the inbound SMS webhook.
        dr_callback_url (str, Optional): The URL for the delivery receipt webhook.
        max_outbound_request (int, Optional): The maximum number of outbound messages
            per second.
        max_inbound_request (int, Optional): The maximum number of inbound messages
            per second.
        max_calls_per_second (int, Optional): The maximum number of API calls per second.
    """

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
    """Model for a Vonage API secret.

    Args:
        id (str): The unique ID of the secret.
        created_at (str): The timestamp when the secret was created.
    """

    id: str
    created_at: str

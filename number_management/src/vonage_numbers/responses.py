from typing import Optional

from pydantic import BaseModel, Field


class OwnedNumber(BaseModel):
    """Model for an owned number.

    Args:
        country (str): The two-letter country code (in ISO 3166-1 alpha-2 format).
        msisdn (PhoneNumber): The phone number in E.164 format.
        mo_http_url (str, Optional): The URL of the webhook endpoint that handles inbound
            messages.
        type (str, Optional): The type of number.
        features (list[str], Optional): The capabilities of the number.
        messages_callback_type (str, Optional): The type of webhook for messages.
            This is always `app`.
        messages_callback_value (str, Optional): A Vonage application ID.
        voice_callback_type (str, Optional): The type of webhook for voice.
        voice_callback_value (str, Optional): A SIP URI, telephone number or Vonage
            application ID.
        app_id (str, Optional): ID of the Vonage application linked to this number.
    """

    country: Optional[str] = Field(None, min_length=2, max_length=2)
    msisdn: Optional[str] = None
    mo_http_url: Optional[str] = Field(None, validation_alias='moHttpUrl')
    type: Optional[str] = None
    features: Optional[list[str]] = None
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
    """Model for an available number.

    Args:
        country (str, Optional): The two-letter country code (in ISO 3166-1 alpha-2 format).
        msisdn (str, Optional): The phone number in E.164 format.
        type (str, Optional): The type of number.
        cost (str, Optional): The monthly rental cost for this number, in Euros.
        features (list[str], Optional): The capabilities of the number.
    """

    country: Optional[str] = Field(None, min_length=2, max_length=2)
    msisdn: Optional[str] = None
    type: Optional[str] = None
    cost: Optional[str] = None
    features: Optional[list[str]] = None


class NumbersStatus(BaseModel):
    """Model for the status of a number.

    Args:
        error_code (str, Optional): The status code of the response. 200 indicates a
            successful request.
        error_code_label (str, Optional): A human-readable description of the error code.
    """

    error_code: str = Field(None, validation_alias='error-code')
    error_code_label: str = Field(None, validation_alias='error-code-label')

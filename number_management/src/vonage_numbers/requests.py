from typing import Optional

from pydantic import BaseModel, Field, model_validator
from vonage_numbers.enums import NumberFeatures, NumberType, VoiceCallbackType
from vonage_utils.types import PhoneNumber

from .errors import NumbersError


class ListNumbersFilter(BaseModel):
    """Model with filters for listing numbers.

    Args:
        pattern (str, Optional): The number pattern you want to search for. Use in
            conjunction with `search_pattern`.
        search_pattern (int, Optional): The strategy to use when searching for numbers.
            - 0: Search for numbers that start with `pattern` (Note: all numbers are in
                E.164 format, so the starting pattern includes the country code, such
                as 1 for USA).
            - 1: Search for numbers that contain `pattern`.
            - 2: Search for numbers that end with `pattern`.
        size (int, Optional): The number of results to return per page.
        index (int, Optional): The page number to return.
    """

    pattern: Optional[str] = None
    search_pattern: Optional[int] = Field(None, ge=0, le=2)
    size: Optional[int] = Field(100, le=100)
    index: Optional[int] = Field(None, ge=1)

    @model_validator(mode='after')
    def check_search_pattern_if_pattern(self):
        if (self.pattern is None) != (self.search_pattern is None):
            raise NumbersError(
                '"search_pattern" is required when "pattern"" is provided and vice versa.'
            )
        return self


class ListOwnedNumbersFilter(ListNumbersFilter):
    """Model with filters for listing numbers you own.

    Args:
        country (str, Optional): The two-letter country code (in ISO 3166-1 alpha-2 format).
        application_id (str, Optional): The Vonage application ID.
        has_application (bool, Optional): Whether the number has an application associated
            with it. Set this optional field to `True` to restrict your results to numbers
            associated with an Application (any Application). Set to `false` to find all
            numbers not associated with any Application. Omit the field to avoid filtering
            on whether or not the number is assigned to an Application.
        pattern (str, Optional): The number pattern you want to search for. Use in
            conjunction with `search_pattern`.
        search_pattern (int, Optional): The strategy to use when searching for numbers.
            - 0: Search for numbers that start with `pattern` (Note: all numbers are in
                E.164 format, so the starting pattern includes the country code, such
                as 1 for USA).
            - 1: Search for numbers that contain `pattern`.
            - 2: Search for numbers that end with `pattern`.
        size (int, Optional): The number of results to return per page.
        index (int, Optional): The page number to return.
    """

    country: Optional[str] = Field(None, min_length=2, max_length=2)
    application_id: Optional[str] = None
    has_application: Optional[bool] = None


class SearchAvailableNumbersFilter(ListNumbersFilter):
    """Model with filters for searching available numbers.

    Args:
        country (str): The two-letter country code (in ISO 3166-1 alpha-2 format).
        type (NumberType, Optional): The type of number you are searching for.
        features (NumberFeatures, Optional): The features you want the number to have.
        pattern (str, Optional): The number pattern you want to search for. Use in
            conjunction with `search_pattern`.
        search_pattern (int, Optional): The strategy to use when searching for numbers.
            - 0: Search for numbers that start with `pattern` (Note: all numbers are in
                E.164 format, so the starting pattern includes the country code, such
                as 1 for USA).
            - 1: Search for numbers that contain `pattern`.
            - 2: Search for numbers that end with `pattern`.
        size (int, Optional): The number of results to return per page.
        index (int, Optional): The page number to return.
    """

    country: str = Field(..., min_length=2, max_length=2)
    type: Optional[NumberType] = None
    features: Optional[NumberFeatures] = None


class NumberParams(BaseModel):
    """Model for buying/cancelling a number.

    If you'd like to perform an action on a subaccount, provide the api_key of that
    account in the `target_api_key` field. If you'd like to perform an action on your own
    account, you do not need to provide this field.

    Args:
        country (str): The two-letter country code (in ISO 3166-1 alpha-2 format).
        msisdn (PhoneNumber): The phone number in E.164 format.
        target_api_key (str, Optional): The API key of the subaccount you want to
            perform the action on. If you want to perform the action on your own account,
            you do not need to provide this field.
    """

    country: str = Field(..., min_length=2, max_length=2)
    msisdn: PhoneNumber
    target_api_key: Optional[str] = None


class UpdateNumberParams(BaseModel):
    """Model for updating a number.

    Args:
        country (str): The two-letter country code (in ISO 3166-1 alpha-2 format).
        msisdn (PhoneNumber): The phone number in E.164 format.
        app_id (str, Optional): The Vonage application that will handle inbound traffic
            to this number.
        mo_http_url (str, Optional): The URL to which Vonage sends a webhook when a
            message is received. Set to an empty string to remove the webhook.
        mo_smpp_system_type (str, Optional): The associated system type for your SMPP
            client.
        voice_callback_type (VoiceCallbackType, Optional): Specify whether inbound voice
            calls on your number are forwarded to a SIP or a telephone number. This must
            be used with the `voice_callback_value parameter. If set, `sip` or `tel` are
            prioritised over the Voice capability set in your Application.
        voice_callback_value (str, Optional): A SIP URI or telephone number. Must be used
            with the `voice_callback_type` parameter.
        voice_status_callback (str, Optional): A webhook URI for Vonage sends a request
            to when a call ends.
    """

    country: str = Field(..., min_length=2, max_length=2)
    msisdn: str
    app_id: Optional[str] = None
    mo_http_url: Optional[str] = Field(None, serialization_alias='moHttpUrl')
    mo_smpp_sytem_type: Optional[str] = Field(None, serialization_alias='moSmppSysType')
    voice_callback_type: Optional[VoiceCallbackType] = Field(
        None, serialization_alias='voiceCallbackType'
    )
    voice_callback_value: Optional[str] = Field(
        None, serialization_alias='voiceCallbackValue'
    )
    voice_status_callback: Optional[str] = Field(
        None, serialization_alias='voiceStatusCallback'
    )

    @model_validator(mode='after')
    def check_voice_callbacks(self):
        if (self.voice_callback_type is None) != (self.voice_callback_value is None):
            raise NumbersError(
                '"voice_callback_value" is required when "voice_callback_type" is provided, and vice versa.'
            )
        return self

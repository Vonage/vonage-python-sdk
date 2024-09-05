from typing import Optional

from pydantic import BaseModel, Field, model_validator

from vonage_numbers.enums import NumberFeatures, NumberType, VoiceCallbackType

from .errors import NumbersError
from vonage_utils.types import PhoneNumber


class ListNumbersFilter(BaseModel):
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
    country: Optional[str] = Field(None, min_length=2, max_length=2)
    application_id: Optional[str] = None
    has_application: Optional[bool] = None


class SearchAvailableNumbersFilter(ListNumbersFilter):
    country: str = Field(..., min_length=2, max_length=2)
    type: Optional[NumberType] = None
    features: Optional[NumberFeatures] = None


class NumberParams(BaseModel):
    """Specify the two-letter country code and the number you are referring to.

    If you'd like to perform an action on a subaccount, provide the api_key of
    that account in the `target_api_key` field. If you'd like to perform an action
    on your own account, you do not need to provide this field.
    """

    country: str = Field(..., min_length=2, max_length=2)
    msisdn: PhoneNumber
    target_api_key: Optional[str] = None


class UpdateNumberParams(BaseModel):
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

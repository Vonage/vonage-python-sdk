from logging import getLogger
from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator
from vonage_utils.types.phone_number import PhoneNumber

from .language_codes import LanguageCode, Psd2LanguageCode

logger = getLogger('vonage_verify')


class BaseVerifyRequest(BaseModel):
    """Base request object containing the data and options for a verification request."""

    number: PhoneNumber
    country: Optional[str] = Field(None, max_length=2)
    code_length: Optional[Literal[4, 6]] = None
    pin_expiry: Optional[int] = Field(None, ge=60, le=3600)
    next_event_wait: Optional[int] = Field(None, ge=60, le=900)
    workflow_id: Optional[int] = Field(None, ge=1, le=7)

    @model_validator(mode='after')
    def check_expiry_and_next_event_timing(self):
        if self.pin_expiry is None or self.next_event_wait is None:
            return self
        if self.pin_expiry % self.next_event_wait != 0:
            logger.warning(
                f'The pin_expiry should be a multiple of next_event_wait.'
                f'\nThe current values are: pin_expiry={self.pin_expiry}, next_event_wait={self.next_event_wait}.'
                f'\nThe value of pin_expiry will be set to next_event_wait.'
            )
            self.pin_expiry = self.next_event_wait
        return self


class VerifyRequest(BaseVerifyRequest):
    """Request object for a verification request.

    You must set the `number` and `brand` fields.
    """

    brand: str = Field(..., max_length=18)
    sender_id: Optional[str] = Field(None, max_length=11)
    lg: Optional[LanguageCode] = None
    pin_code: Optional[str] = Field(None, min_length=4, max_length=10)


class Psd2Request(BaseVerifyRequest):
    """Request object for a PSD2 verification request.

    You must set the `number`, `payee` and `amount` fields.
    """

    payee: str = Field(..., max_length=18)
    amount: float
    lg: Optional[Psd2LanguageCode] = None

from logging import getLogger
from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator
from vonage_utils.types import PhoneNumber

from .language_codes import LanguageCode, Psd2LanguageCode

logger = getLogger('vonage_verify')


class BaseVerifyRequest(BaseModel):
    """Base request object containing the data and options for a verification request.

    Args:
        number (PhoneNumber): The phone number to verify. Unless you are setting country
            explicitly, this number must be in E.164 format.
        country (str, Optional): If you do not provide `number` in international format
            or you are not sure if `number` is correctly formatted, specify the
            two-character country code in country. Verify will then format the number for
            you.
        code_length (int, Optional): The length of the verification code to generate.
        pin_expiry (int, Optional): How long the generated verification code is valid
            for, in seconds. When you specify both `pin_expiry` and `next_event_wait`
            then `pin_expiry` must be an integer multiple of `next_event_wait` otherwise
            `pin_expiry` is defaulted to equal `next_event_wait`.
        next_event_wait (int, Optional): The wait time in seconds between attempts to
            deliver the verification code.
        workflow_id (int, Optional): Selects the predefined sequence of SMS and TTS (Text
            To Speech) actions to use in order to convey the PIN to your user.
    """

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

    Args:
        number (PhoneNumber): The phone number to verify. Unless you are setting country
            explicitly, this number must be in E.164 format.
        country (str, Optional): If you do not provide `number` in international format
            or you are not sure if `number` is correctly formatted, specify the
            two-character country code in country. Verify will then format the number for
            you.
        brand (str): The name of the company or service that is sending the verification
            request. This will appear in the body of the SMS or TTS message.
        code_length (int, Optional): The length of the verification code to generate.
        pin_expiry (int, Optional): How long the generated verification code is valid
            for, in seconds. When you specify both `pin_expiry` and `next_event_wait`
            then `pin_expiry` must be an integer multiple of `next_event_wait` otherwise
            `pin_expiry` is defaulted to equal `next_event_wait`.
        next_event_wait (int, Optional): The wait time in seconds between attempts to
            deliver the verification code.
        workflow_id (int, Optional): Selects the predefined sequence of SMS and TTS (Text
            To Speech) actions to use in order to convey the PIN to your user.
        sender_id (str, Optional): An 11-character alphanumeric string that represents the
            sender of the verification request. Depending on the location of the phone
            number, restrictions may apply.
        lg (LanguageCode, Optional): The language to use for the verification message.
        pin_code (str, Optional): The verification code to send to the user. If you do not
            provide this, Vonage will generate a code for you.
    """

    brand: str = Field(..., max_length=18)
    sender_id: Optional[str] = Field(None, max_length=11)
    lg: Optional[LanguageCode] = None
    pin_code: Optional[str] = Field(None, min_length=4, max_length=10)


class Psd2Request(BaseVerifyRequest):
    """Request object for a PSD2 verification request.

    You must set the `number`, `payee` and `amount` fields.

    Args:
        number (PhoneNumber): The phone number to verify. Unless you are setting country
            explicitly, this number must be in E.164 format.
        payee (str): An alphanumeric string to indicate to the user the name of the
            recipient that they are confirming a payment to.
        amount (float): The decimal amount of the payment to be confirmed, in Euros.
        country (str, Optional): If you do not provide `number` in international
            format or you are not sure if `number` is correctly formatted, specify the
            two-character country code in `country`. Verify will then format the number for
            you.
        lg (Psd2LanguageCode, Optional): The language to use for the verification message.
        code_length (int, Optional): The length of the verification code to generate.
        pin_expiry (int, Optional): How long the generated verification code is valid
            for, in seconds. When you specify both `pin_expiry` and `next_event_wait`
            then `pin_expiry` must be an integer multiple of `next_event_wait` otherwise
            `pin_expiry` is defaulted to equal `next_event_wait`.
        next_event_wait (int, Optional): The wait time in seconds between attempts to
            deliver the verification code.
        workflow_id (int, Optional): Selects the predefined sequence of SMS and TTS (Text
            To Speech) actions to use in order to convey the PIN to your user.
    """

    payee: str = Field(..., max_length=18)
    amount: float
    lg: Optional[Psd2LanguageCode] = None

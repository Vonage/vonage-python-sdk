from pydantic import BaseModel, Field


class NumberVerificationResponse(BaseModel):
    """Model for the response from the Number Verification API.

    Args:
        device_phone_number_verified (bool): Whether the phone number has been
            successfully verified.
    """

    device_phone_number_verified: bool = Field(
        ..., validation_alias='devicePhoneNumberVerified'
    )

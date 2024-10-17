from pydantic import BaseModel, Field, model_validator
from vonage_network_number_verification.errors import NetworkNumberVerificationError


class NumberVerificationRequest(BaseModel):
    """Model for the request to verify a phone number.

    Args:
        code (str): The code returned from the OIDC redirect.
        redirect_uri (str): The URI to redirect to after authentication.
        phone_number (str): The phone number to verify. Use the E.164 format with
            or without a leading +.
        hashed_phone_number (str): The hashed phone number to verify.
    """

    code: str
    redirect_uri: str
    phone_number: str = Field(None, serialization_alias='phoneNumber')
    hashed_phone_number: str = Field(None, serialization_alias='hashedPhoneNumber')

    @model_validator(mode='after')
    def check_only_one_phone_number(self):
        """Check that only one of `phone_number` and `hashed_phone_number` is set."""

        if self.phone_number is not None and self.hashed_phone_number is not None:
            raise NetworkNumberVerificationError(
                'Only one of `phone_number` and `hashed_phone_number` can be set.'
            )

        if self.phone_number is None and self.hashed_phone_number is None:
            raise NetworkNumberVerificationError(
                'One of `phone_number` and `hashed_phone_number` must be set.'
            )

        return self

from typing import Optional

from pydantic import BaseModel, Field


class CreateOidcUrl(BaseModel):
    """Model to craft a URL for OIDC authentication.

    Args:
        redirect_uri (str): The URI to redirect to after authentication.
        state (str, optional): A unique identifier for the request. Can be any string.
        login_hint (str, optional): The phone number to use for the request.
    """

    redirect_uri: str
    state: Optional[str] = None
    login_hint: Optional[str] = None
    scope: Optional[
        str
    ] = 'openid dpv:FraudPreventionAndDetection#number-verification-verify-read'


class NumberVerificationRequest(BaseModel):
    """Model for the request to verify a phone number.

    Args:
        phone_number (str): The phone number to verify. Use the E.164 format with
            or without a leading +.
        hashed_phone_number (str): The hashed phone number to verify.
    """

    phone_number: str = Field(..., alias='phoneNumber')
    hashed_phone_number: str = Field(..., alias='hashedPhoneNumber')

from typing import Optional

from pydantic import BaseModel, Field


class SimSwapCheckRequest(BaseModel):
    """Request model to check if a SIM has been swapped using the Vonage Sim Swap Network
    API.

    Args:
        phone_number (str): The phone number to check. Use the E.164 format with
            or without a leading +.
        max_age (int, optional): Period in hours to be checked for SIM swap.
    """

    phone_number: str = Field(..., serialization_alias='phoneNumber')
    max_age: Optional[int] = Field(None, serialization_alias='maxAge')

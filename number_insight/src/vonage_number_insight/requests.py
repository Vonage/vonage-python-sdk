from typing import Optional

from pydantic import BaseModel
from vonage_utils.types import PhoneNumber


class BasicInsightRequest(BaseModel):
    """Model for a basic number insight request.

    Args:
        number (PhoneNumber): The phone number to get insight information for.
        country (str, Optional): The country code for the phone number.
    """

    number: PhoneNumber
    country: Optional[str] = None


class StandardInsightRequest(BasicInsightRequest):
    """Model for a standard number insight request.

    Args:
        number (PhoneNumber): The phone number to get insight information for.
        country (str, Optional): The country code for the phone number.
        cnam (bool, Optional): Whether to include the Caller ID Name (CNAM) with the response.
    """

    cnam: Optional[bool] = None


class AdvancedAsyncInsightRequest(StandardInsightRequest):
    """Model for an advanced asynchronous number insight request.

    Args:
        number (PhoneNumber): The phone number to get insight information for.
        callback (str): The URL to send the asynchronous response to.
        country (str, Optional): The country code for the phone number.
        cnam (bool, Optional): Whether to include the Caller ID Name (CNAM) with the response.
    """

    callback: str


class AdvancedSyncInsightRequest(StandardInsightRequest):
    """Model for an advanced synchronous number insight request.

    Args:
        number (PhoneNumber): The phone number to get insight information for.
        country (str, Optional): The country code for the phone number.
        cnam (bool, Optional): Whether to include the Caller ID Name (CNAM) with the response.
    """

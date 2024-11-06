from typing import Optional

from pydantic import BaseModel, Field

from .enums import LanguageCode


class CaptionsOptions(BaseModel):
    """The Options to send captions.

    Args:
        session_id (str): The session ID.
        token (str): A valid token with moderation privileges.
        language_code (LanguageCode, Optional): The language code.
        max_duration (int, Optional): The maximum duration.
        partial_captions (bool, Optional): The partial captions.
        status_callback_url (str, Optional): The status callback URL.
    """

    session_id: str = Field(..., serialization_alias='sessionId')
    token: str
    language_code: Optional[LanguageCode] = Field(
        None, serialization_alias='languageCode'
    )
    max_duration: Optional[int] = Field(
        None, ge=300, le=14400, serialization_alias='maxDuration'
    )
    partial_captions: Optional[bool] = Field(None, serialization_alias='partialCaptions')
    status_callback_url: Optional[str] = Field(
        None, min_length=15, max_length=2048, serialization_alias='statusCallbackUrl'
    )


class CaptionsData(BaseModel):
    """Class containing captions ID.

    Args:
        captions_id (str): The captions ID.
    """

    captions_id: str = Field(..., serialization_alias='captionsId')

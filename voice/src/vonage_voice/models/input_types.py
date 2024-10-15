from typing import Optional

from pydantic import BaseModel, Field


class Dtmf(BaseModel):
    """Model for DTMF input options used as part of an NCCO.

    Args:
        timeOut (Optional[int]): The result of the callee's activity is sent to the
            `eventUrl` webhook endpoint `timeOut` seconds after the last action.
        submitOnHash (Optional[bool]): Set to `True` so the callee's activity is sent
            to your webhook endpoint at `eventUrl` after they press `#`. If `#` is not
                pressed the result is submitted after `timeOut` seconds.
        maxDigits (Optional[int]): The number of digits the user can press.
    """

    timeOut: Optional[int] = Field(None, ge=0, le=10)
    maxDigits: Optional[int] = Field(None, ge=1, le=20)
    submitOnHash: Optional[bool] = None


class Speech(BaseModel):
    """Model for speech input options used as part of an NCCO.

    Args:
        uuid (Optional[list[str]]): The UUID of the speech recognition session.
        endOnSilence (Optional[float]): The length of silence in seconds that indicates
            the end of the speech. Uses BCP-47 format.
        language (Optional[str]): The language used for speech recognition. The default
            is `en-US`.
        context (Optional[list[str]]):Array of hints (strings) to improve recognition
            quality if certain words are expected from the user.
        startTimeout (Optional[int]): Controls how long the system will wait for the user
            to start speaking.
        maxDuration (Optional[int]): Controls maximum speech duration (from the moment
            the user starts speaking).
        saveAudio (Optional[bool]): If the speech input recording is sent to your webhook
            endpoint at `eventUrl`.
        sensitivity (Optional[int]): Audio sensitivity used to differentiate noise from
            speech. An integer value where `10` represents low sensitivity and `100`
            maximum sensitivity.
    """

    uuid: Optional[list[str]] = None
    endOnSilence: Optional[float] = Field(None, ge=0.4, le=10.0)
    language: Optional[str] = None
    context: Optional[list[str]] = None
    startTimeout: Optional[int] = Field(None, ge=1, le=60)
    maxDuration: Optional[int] = Field(None, ge=1, le=60)
    saveAudio: Optional[bool] = False
    sensitivity: Optional[int] = Field(None, ge=0, le=100)

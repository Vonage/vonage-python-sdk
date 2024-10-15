from typing import Literal, Optional, Union

from pydantic import BaseModel, Field, model_validator
from vonage_utils.types import Dtmf

from ..errors import VoiceError
from .common import AdvancedMachineDetection, Phone, Sip, Vbc, Websocket
from .enums import CallState, TtsLanguageCode
from .ncco import Connect, Conversation, Input, Notify, Record, Stream, Talk


class ToPhone(Phone):
    """Model for the phone number to call.

    Args:
        number (PhoneNumber): The phone number.
        dtmf_answer (Optional[Dtmf]): The DTMF tones to send when the call is answered.
    """

    dtmf_answer: Optional[Dtmf] = Field(None, serialization_alias='dtmfAnswer')


class CreateCallRequest(BaseModel):
    """Request model for creating a call. You must supply either `ncco` or `answer_url`.

    Args:
        ncco (Optional[list[Union[Record, Conversation, Connect, Input, Talk, Stream, Notify]]]):
            The Nexmo Call Control Object (NCCO) to use for the call.
        answer_url (Optional[list[str]]): The URL to fetch the NCCO from.
        answer_method (Optional[Literal['POST', 'GET']]): The HTTP method used to send
            event information to `answer_url`.
        to (list[Union[ToPhone, Sip, Websocket, Vbc]]): The type of connection to call.
        from_ (Optional[Phone]): The phone number to use when calling. Mutually exclusive
            with the `random_from_number` property.
        random_from_number (Optional[bool]): Whether to use a random number as the caller's
            phone number. The number will be selected from the list of the numbers assigned
            to the current application. Mutually exclusive with the `from_` property.
        event_url (Optional[list[str]]): The webhook endpoint where call progress events
            are sent.
        event_method (Optional[Literal['POST', 'GET']]): The HTTP method used to send the call
            events to `event_url`.
        machine_detection (Optional[Literal['continue', 'hangup']]): Configure the behavior
            when Vonage detects that the call is answered by voicemail.
        advanced_machine_detection (Optional[AdvancedMachineDetection]): Configure the
            behavior of Vonage's advanced machine detection. Overrides `machine_detection`
            if both are set.
        length_timer (Optional[int]): Set the number of seconds that elapse before Vonage
            hangs up after the call state changes to "answered".
        ringing_timer (Optional[int]): Set the number of seconds that elapse before Vonage
            hangs up after the call state changes to `ringing`.

    Raises:
        VoiceError: If neither `ncco` nor `answer_url` is set.
        VoiceError: If both `ncco` and `answer_url` are set.
        VoiceError: If neither `from_` nor `random_from_number` is set.
        VoiceError: If both `from_` and `random_from_number` are set.
    """

    ncco: list[Union[Record, Conversation, Connect, Input, Talk, Stream, Notify]] = None
    answer_url: list[str] = None
    answer_method: Optional[Literal['POST', 'GET']] = None
    to: list[Union[ToPhone, Sip, Websocket, Vbc]]

    from_: Optional[Phone] = Field(None, serialization_alias='from')
    random_from_number: Optional[bool] = None
    event_url: Optional[list[str]] = None
    event_method: Optional[Literal['POST', 'GET']] = None
    machine_detection: Optional[Literal['continue', 'hangup']] = None
    advanced_machine_detection: Optional[AdvancedMachineDetection] = None
    length_timer: Optional[int] = Field(None, ge=1, le=7200)
    ringing_timer: Optional[int] = Field(None, ge=1, le=120)

    @model_validator(mode='after')
    def validate_ncco_and_answer_url(self):
        if self.ncco is None and self.answer_url is None:
            raise VoiceError('Either `ncco` or `answer_url` must be set')
        if self.ncco is not None and self.answer_url is not None:
            raise VoiceError('`ncco` and `answer_url` cannot be used together')
        return self

    @model_validator(mode='after')
    def validate_from_and_random_from_number(self):
        if self.random_from_number is None and self.from_ is None:
            raise VoiceError('Either `from_` or `random_from_number` must be set')
        if self.random_from_number == True and self.from_ is not None:
            raise VoiceError('`from_` and `random_from_number` cannot be used together')
        return self


class ListCallsFilter(BaseModel):
    """Filter model for listing calls.

    Args:
        status (Optional[CallState]): The state of the call.
        date_start (Optional[str]): Return the records available after this point in time.
        date_end (Optional[str]): Return the records that occurred before this point in
            time.
        page_size (Optional[int]): Return this amount of records in the response.
        record_index (Optional[int]): Return calls from this index in the response.
        order (Optional[Literal['asc', 'desc']]): The order in which to return the records.
        conversation_uuid (Optional[str]): Return all the records associated with a
            specific conversation.
    """

    status: Optional[CallState] = None
    date_start: Optional[str] = None
    date_end: Optional[str] = None
    page_size: Optional[int] = Field(100, ge=1, le=100)
    record_index: Optional[int] = None
    order: Optional[Literal['asc', 'desc']] = None
    conversation_uuid: Optional[str] = None


class AudioStreamOptions(BaseModel):
    """Options for streaming audio to a call.

    Args:
        stream_url (list[str]): The URL to stream audio from.
        loop (Optional[int]): The number of times to loop the audio. If set to 0, the audio
            will loop indefinitely.`
        level (Optional[float]): The volume level of the audio. The value must be between
            -1 and 1.
    """

    stream_url: list[str]
    loop: Optional[int] = Field(None, ge=0)
    level: Optional[float] = Field(None, ge=-1, le=1)


class TtsStreamOptions(BaseModel):
    """Options for streaming text-to-speech to a call.

    Args:
        text (str): The text to stream.
        language (Optional[TtsLanguageCode]): The language of the text.
        style (Optional[int]): The style of the voice (vocal range, tessitura, and timbre)
            to use.
        premium (Optional[bool]): Whether to use the premium version of the specified
            voice.
        loop (Optional[int]): The number of times to loop the audio. If set to 0, the audio
            will loop indefinitely.
        level (Optional[float]): The volume level of the audio. The value must be between
            -1 and 1.
    """

    text: str
    language: Optional[TtsLanguageCode] = None
    style: Optional[int] = None
    premium: Optional[bool] = None
    loop: Optional[int] = Field(None, ge=0)
    level: Optional[float] = Field(None, ge=-1, le=1)

from typing import Literal, Optional, Union

from pydantic import BaseModel, Field, model_validator
from vonage_utils.types import PhoneNumber
from vonage_voice.errors import NccoActionError
from vonage_voice.models.common import AdvancedMachineDetection

from .connect_endpoints import (
    AppEndpoint,
    PhoneEndpoint,
    SipEndpoint,
    VbcEndpoint,
    WebsocketEndpoint,
)
from .enums import NccoActionType
from .input_types import Dtmf, Speech


class NccoAction(BaseModel):
    """The base class for all NCCO actions.

    For more information on NCCO actions, see the Vonage API documentation.
    """


class Record(NccoAction):
    """Use the Record action to record a call or part of a call.

    Args:
        format (Optional[Literal['mp3', 'wav', 'ogg']]): The format of the recording.
        split (Optional[Literal['conversation']]): Record the sent and received audio
            in separate channels of a stereo recording. Set to `conversation` to enable
            this.
        channels (Optional[int]): The number of channels to record.  If the number of
            participants exceeds `channels` any additional participants will be added
            to the last channel in file. `split=conversation` must also be set.
        endOnSilence (Optional[int]): Stop recording after this many seconds of silence.
        endOnKey (Optional[str]): Stop recording when a digit is pressed on the keypad.
            Possible values are `[0-9*#]`.
        timeOut (Optional[int]): The maximum length of a recording in seconds. Once the
            recording is stopped the recording data is sent to `event_url`.
        beepStart (Optional[bool]): Play a beep when the recording starts.
        eventUrl (Optional[list[str]]): The URL to the webhook endpoint that is called
            asynchronously when a recording is finished. If the message recording is
            hosted by Vonage, this webhook contains the URL you need to download the
            recording and other metadata.
        eventMethod (Optional[str]): The HTTP method used to send the recording event to
            `eventUrl`.
    """

    format: Optional[Literal['mp3', 'wav', 'ogg']] = None
    split: Optional[Literal['conversation']] = None
    channels: Optional[int] = Field(None, ge=1, le=32)
    endOnSilence: Optional[int] = Field(None, ge=3, le=10)
    endOnKey: Optional[str] = Field(None, pattern=r'^[0-9#*]$')
    timeOut: Optional[int] = Field(None, ge=3, le=7200)
    beepStart: Optional[bool] = None
    eventUrl: Optional[list[str]] = None
    eventMethod: Optional[str] = None
    action: NccoActionType = NccoActionType.RECORD

    @model_validator(mode='after')
    def enable_split(self):
        if self.channels and not self.split:
            self.split = 'conversation'
        return self


class Conversation(NccoAction):
    """You can use the Conversation action to create standard or moderated conferences,
    while preserving the communication context.

    Using a conversation with the same name reuses the same persisted conversation.

    Args:
        name (str): The name of the conversation room.
        musicOnHoldUrl (Optional[list[str]]): The URL to the music that is played to
            participants when they are on hold.
        startOnEnter (Optional[bool]): The default value of `True` ensures that the
            conversation starts when this caller joins conversation `name`. Set to
            `False` for attendees in a moderated conversation.
        endOnExit (Optional[bool]): End the conversation when the moderator leaves.
        record (Optional[bool]): Record the conversation.
        canSpeak (Optional[list[str]]): A list of leg UUIDs that this participant can be
            heard by. If not provided, the participant can be heard by everyone. If an
            empty list is provided, the participant will not be heard by anyone.
        canHear (Optional[list[str]]): A list of leg UUIDs that this participant can
            hear. If not provided, the participant can hear everyone. If an empty list
            is provided, the participant will not hear any other participants.
        mute (Optional[bool]): Mute the participant.

    Raises:
        NccoActionError: If the `mute` option is used with the `canSpeak` option.
    """

    name: str
    musicOnHoldUrl: Optional[list[str]] = None
    startOnEnter: Optional[bool] = None
    endOnExit: Optional[bool] = None
    record: Optional[bool] = None
    canSpeak: Optional[list[str]] = None
    canHear: Optional[list[str]] = None
    mute: Optional[bool] = None
    action: NccoActionType = NccoActionType.CONVERSATION

    @model_validator(mode='after')
    def can_mute(self):
        if self.canSpeak and self.mute:
            raise NccoActionError(
                'Cannot use mute option if canSpeak option is specified.'
            )
        return self


class Connect(NccoAction):
    """You can use the Connect action to connect a call to endpoints such as phone numbers
    or a VBC extension.

    Args:
        endpoint (list[Union[PhoneEndpoint, AppEndpoint, WebsocketEndpoint, SipEndpoint, VbcEndpoint]]):
            The endpoint to connect to.
        from_ (Optional[PhoneNumber]): The phone number to use when calling. Mutually exclusive
            with the `randomFromNumber` property.
        randomFromNumber (Optional[bool]): Whether to use a random number as the caller's phone
            number. The number will be selected from the list of the numbers assigned to the
            current application. Mutually exclusive with the `from_` property.
        eventType (Optional[Literal['synchronous']]): The type of event that triggers the `eventUrl`
            webhook. The default is `synchronous`.
        timeout (Optional[int]): If the call is unanswered, set the number in seconds before
            Vonage stops ringing `endpoint`.
        limit (Optional[int]): The maximum duration of the call in seconds. The default is `7200`.
        machineDetection (Optional[Literal['continue', 'hangup']]): Configure the behavior when Vonage
            detects that the call is answered by voicemail.
        advancedMachineDetection (Optional[AdvancedMachineDetection]): Configure the behavior of Vonage's
            advanced machine detection. Overrides `machineDetection` if both are set.
        eventUrl (Optional[list[str]]): Set the webhook endpoint that Vonage calls asynchronously
            on each of the possible Call States. If `eventType` is set to `synchronous` the
            `eventUrl` can return an NCCO that overrides the current NCCO when a timeout occurs.
        eventMethod (Optional[str]): The HTTP method used to send the call events to `eventUrl`.
        ringbackTone (Optional[list[str]]):A URL value that points to a `ringbackTone` to be played
            back on repeat to the caller, so they don't hear silence. The `ringbackTone` will
            automatically stop playing when the call is fully connected. It's not recommended to
            use this parameter when connecting to a `phone` endpoint, as the carrier will supply
            their own `ringbackTone`.

    Raises:
        NccoActionError: If neither `from_` nor `randomFromNumber` is set.
        NccoActionError: If both `from_` and `randomFromNumber` are set.
    """

    endpoint: list[
        Union[PhoneEndpoint, AppEndpoint, WebsocketEndpoint, SipEndpoint, VbcEndpoint]
    ]
    from_: Optional[PhoneNumber] = Field(None, serialization_alias='from')
    randomFromNumber: Optional[bool] = None
    eventType: Optional[Literal['synchronous']] = None
    timeout: Optional[int] = None
    limit: Optional[int] = Field(None, le=7200)
    machineDetection: Optional[Literal['continue', 'hangup']] = None
    advancedMachineDetection: Optional[AdvancedMachineDetection] = None
    eventUrl: Optional[list[str]] = None
    eventMethod: Optional[str] = None
    ringbackTone: Optional[list[str]] = None
    action: NccoActionType = NccoActionType.CONNECT

    @model_validator(mode='after')
    def validate_from_and_random_from_number(self):
        if self.randomFromNumber is None and self.from_ is None:
            raise NccoActionError('Either `from_` or `random_from_number` must be set.')
        if self.randomFromNumber == True and self.from_ is not None:
            raise NccoActionError(
                '`from_` and `random_from_number` cannot be used together.'
            )
        return self


class Talk(NccoAction):
    """The Talk action sends synthesized speech to a Conversation.

    For valid languages, see the Vonage API documentation.
    https://developer.vonage.com/en/voice/voice-api/concepts/text-to-speech#supported-languages

    Args:
        text (str): The text to be spoken.
        bargeIn (Optional[bool]): Set to `True` to allow the user to interrupt the audio
            stream by speaking or DTMF input. The default is `False`.
        loop (Optional[int]): The number of times the audio file is played before the call
            is closed. The default is `1`, `0` loops indefinitely.
        level (Optional[float]): The volume the speech is played at. The default is `0`.
        language (Optional[str]): The language used for the message. The default is `en-US`.
        style (Optional[int]): The vocal style of the voice used.
        premium (Optional[bool]): Set to `True` to use the premium version of the text-to-speech
            voice. The default is `False`.
    """

    text: str = Field(..., max_length=1500)
    bargeIn: Optional[bool] = None
    loop: Optional[int] = Field(None, ge=0)
    level: Optional[float] = Field(None, ge=-1, le=1)
    language: Optional[str] = None
    style: Optional[int] = None
    premium: Optional[bool] = None
    action: NccoActionType = NccoActionType.TALK


class Stream(NccoAction):
    """The stream action allows you to send an audio stream to a Call or Conversation.

    Args:
        streamUrl (list[str]): An array containing a single URL to an mp3 or wav (16-bit)
            audio file to stream to the Call or Conversation.
        level (Optional[float]): The volume level of the audio. The value must be between
            -1 and 1.
        bargeIn (Optional[bool]): Set to `True` to allow the user to interrupt the audio
            stream by speaking or DTMF input. The default is `False`.
        loop (Optional[int]): The number of times the audio file is played before the call
            is closed. The default is `1`, `0` loops indefinitely.
    """

    streamUrl: list[str]
    level: Optional[float] = Field(None, ge=-1, le=1)
    bargeIn: Optional[bool] = None
    loop: Optional[int] = Field(None, ge=0)
    action: NccoActionType = NccoActionType.STREAM


class Input(NccoAction):
    """Collect digits or speech input by the person you are are calling.

    Args:
        type (list[Union[Literal['dtmf'], Literal['speech']]]): The type of input to collect.
        dtmf (Optional[Dtmf]): The DTMF options to use.
        speech (Optional[Speech]): The speech options to use.
        eventUrl (Optional[list[str]]): Vonage sends the digits pressed by the callee to
            this URL either 1) after `timeOut` pause in activity or when `#` is pressed for
            DTMF input or 2) after the user stops speaking or 30 seconds of speech for
            speech input.
        eventMethod (Optional[str]): The HTTP method to use when sending the result to
            `eventUrl`.
    """

    type: list[Union[Literal['dtmf'], Literal['speech']]]
    dtmf: Optional[Dtmf] = None
    speech: Optional[Speech] = None
    eventUrl: Optional[list[str]] = None
    eventMethod: Optional[str] = None
    action: NccoActionType = NccoActionType.INPUT


class Notify(NccoAction):
    """Use the notify action to send a custom payload to your event URL. Your webhook
    endpoint can return another NCCO that replaces the existing NCCO or return an empty
    payload meaning the existing NCCO will continue to execute.

    Args:
        payload (dict): The custom payload to send to your event URL.
        eventUrl (list[str]): The URL to send events to.  If you return an NCCO when you
            receive a notification, it will replace the current NCCO.
        eventMethod (Optional[str]): The HTTP method to use when sending the payload.
    """

    payload: dict
    eventUrl: list[str]
    eventMethod: Optional[str] = None
    action: NccoActionType = NccoActionType.NOTIFY

from re import search
from typing import Optional, Union

from pydantic import BaseModel, Field, field_validator, model_validator
from vonage_utils.types import PhoneNumber

from .enums import ChannelType, Locale
from .errors import VerifyError


class Channel(BaseModel):
    """Base model for a channel to use in a verification request.

    Args:
        to (PhoneNumber): The phone number to send the verification code to, in the
            E.164 format without a leading `+` or `00`.
    """

    to: PhoneNumber


class SilentAuthChannel(Channel):
    """Model for a Silent Authentication channel.

    Args:
        to (PhoneNumber): The phone number to send the verification code to, in the
            E.164 format without a leading `+` or `00`.
        redirect_url (str, Optional): Optional final redirect added at the end of the
            check_url request/response lifecycle. Will contain the `request_id` and
            `code` as a url fragment after the URL.
        sandbox (bool, Optional): Whether you are using the sandbox to test Silent
            Authentication integrations.
    """

    redirect_url: Optional[str] = None
    sandbox: Optional[bool] = None
    channel: ChannelType = ChannelType.SILENT_AUTH


class SmsChannel(Channel):
    """Model for an SMS channel.

    Args:
        to (PhoneNumber): The phone number to send the verification code to, in the
            E.164 format without a leading `+` or `00`.
        from_ (Union[PhoneNumber, str], Optional): The sender of the SMS. This can be
            a phone number in E.164 format without a leading `+` or `00`, or a string
            of 3-11 alphanumeric characters.
        app_hash (str, Optional): Optional Android Application Hash Key for automatic
            code detection on a user's device.
        entity_id (str, Optional): Optional PEID required for SMS delivery using Indian
            carriers.
        content_id (str, Optional): Optional PEID required for SMS delivery using Indian
            carriers.

    Raises:
        VerifyError: If the `from_` field is not a valid phone number.
    """

    from_: Optional[Union[PhoneNumber, str]] = Field(None, serialization_alias='from')
    app_hash: Optional[str] = Field(None, min_length=11, max_length=11)
    entity_id: Optional[str] = Field(None, pattern=r'^[0-9]{1,20}$')
    content_id: Optional[str] = Field(None, pattern=r'^[0-9]{1,20}$')
    channel: ChannelType = ChannelType.SMS

    @field_validator('from_')
    @classmethod
    def check_valid_from_field(cls, v):
        if (
            v is not None
            and type(v) is not PhoneNumber
            and not search(r'^[a-zA-Z0-9]{3,11}$', v)
        ):
            raise VerifyError(
                'You must specify a valid "from_" value if included. '
                'It must be a valid phone number without the leading +, or a string of 3-11 alphanumeric characters. '
                f'You set "from_": "{v}".'
            )
        return v


class WhatsappChannel(Channel):
    """Model for a WhatsApp channel.

    Args:
        to (PhoneNumber): The phone number to send the verification code to, in the
            E.164 format without a leading `+` or `00`.
        from_ (Union[PhoneNumber, str]): A WhatsApp Business Account (WABA)-connected
            sender number, in the E.164 format. Don't use a leading + or 00 when entering
            a phone number.

    Raises:
        VerifyError: If the `from_` field is not a valid phone number or string of 3-11
            alphanumeric characters.
    """

    from_: Union[PhoneNumber, str] = Field(..., serialization_alias='from')
    channel: ChannelType = ChannelType.WHATSAPP

    @field_validator('from_')
    @classmethod
    def check_valid_sender(cls, v):
        if type(v) is not PhoneNumber and not search(r'^[a-zA-Z0-9]{3,11}$', v):
            raise VerifyError(
                f'You must specify a valid "from_" value. '
                'It must be a valid phone number without the leading +, or a string of 3-11 alphanumeric characters. '
                f'You set "from_": "{v}".'
            )
        return v


class VoiceChannel(Channel):
    """Model for a Voice channel.

    Args:
        to (PhoneNumber): The phone number to send the verification code to, in the
            E.164 format without a leading `+` or `00`.
    """

    channel: ChannelType = ChannelType.VOICE


class EmailChannel(Channel):
    """Model for an Email channel.

    Args:
        to (str): The email address to send the verification code to.
        from_ (str, Optional): The email address of the sender.
    """

    to: str
    from_: Optional[str] = Field(None, serialization_alias='from')
    channel: ChannelType = ChannelType.EMAIL


class VerifyRequest(BaseModel):
    """Request object for a verification request.

    Args:
        brand (str): The name of the company or service that is sending the verification
            request. This will appear in the body of the SMS or TTS message.
        workflow (list[Union[SilentAuthChannel, SmsChannel, WhatsappChannel, VoiceChannel, EmailChannel]]):
            The list of channels to use in the verification workflow. They will be used
            in the order they are listed.
        locale (Locale, Optional): The locale to use for the verification message.
        channel_timeout (int, Optional): The time in seconds to wait between attempts to
            deliver the verification code.
        client_ref (str, Optional): A unique identifier for the verification request. If
            the client_ref is set when the request is sent, it will be included in the
            callbacks.
        code_length (int, Optional): The length of the verification code to generate.
        code (str, Optional): An optional alphanumeric custom code to use, if you don't
            want Vonage to generate the code.

    Raises:
        VerifyError: If the `workflow` list contains a Silent Authentication channel that
            is not the first channel in the list.
    """

    brand: str = Field(..., min_length=1, max_length=16)
    workflow: list[
        Union[
            SilentAuthChannel,
            SmsChannel,
            WhatsappChannel,
            VoiceChannel,
            EmailChannel,
        ]
    ]
    locale: Optional[Locale] = None
    channel_timeout: Optional[int] = Field(None, ge=15, le=900)
    client_ref: Optional[str] = Field(None, min_length=1, max_length=16)
    code_length: Optional[int] = Field(None, ge=4, le=10)
    code: Optional[str] = Field(None, pattern=r'^[a-zA-Z0-9]{4,10}$')

    @model_validator(mode='after')
    def check_silent_auth_first_if_present(self):
        if len(self.workflow) > 1:
            for i in range(1, len(self.workflow)):
                if isinstance(self.workflow[i], SilentAuthChannel):
                    raise VerifyError(
                        'If using Silent Authentication, it must be the first channel in the "workflow" list.'
                    )
        return self

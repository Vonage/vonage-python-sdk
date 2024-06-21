from re import search
from typing import List, Optional, Union

from pydantic import BaseModel, Field, field_validator, model_validator
from vonage_utils.types import PhoneNumber

from .enums import ChannelType, Locale
from .errors import VerifyError


class Channel(BaseModel):
    to: PhoneNumber


class SilentAuthChannel(Channel):
    redirect_url: Optional[str] = None
    sandbox: Optional[bool] = None
    channel: ChannelType = ChannelType.SILENT_AUTH


class SmsChannel(Channel):
    from_: Optional[Union[PhoneNumber, str]] = Field(None, serialization_alias='from')
    entity_id: Optional[str] = Field(None, pattern=r'^[0-9]{1,20}$')
    content_id: Optional[str] = Field(None, pattern=r'^[0-9]{1,20}$')
    app_hash: Optional[str] = Field(None, min_length=11, max_length=11)
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
    channel: ChannelType = ChannelType.VOICE


class EmailChannel(Channel):
    to: str
    from_: Optional[str] = Field(None, serialization_alias='from')
    channel: ChannelType = ChannelType.EMAIL


class VerifyRequest(BaseModel):
    brand: str = Field(..., min_length=1, max_length=16)
    workflow: List[
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

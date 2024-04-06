from typing import List, Optional, Union
from re import search

from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator,
)
from vonage_utils.types.phone_number import PhoneNumber

from .enums import VerifyChannel, VerifyLocale
from .errors import VerifyError


class Workflow(BaseModel):
    channel: VerifyChannel
    to: PhoneNumber


class SilentAuthWorkflow(Workflow):
    redirect_url: Optional[str] = None
    sandbox: Optional[bool] = None


class SmsWorkflow(Workflow):
    from_: Optional[Union[PhoneNumber, str]] = Field(None, serialization_alias='from')
    entity_id: Optional[str] = Field(None, pattern=r'^[0-9]{1,20}$')
    content_id: Optional[str] = Field(None, pattern=r'^[0-9]{1,20}$')
    app_hash: Optional[str] = Field(None, min_length=11, max_length=11)

    @field_validator('from_')
    @classmethod
    def check_valid_from_field(cls, v):
        if (
            v is not None
            and type(v) is not PhoneNumber
            and not search(r'^[a-zA-Z0-9]{1,15}$', v)
        ):
            raise VerifyError(f'You must specify a valid "from" value if included.')


class WhatsappWorkflow(Workflow):
    from_: Union[PhoneNumber, str] = Field(..., serialization_alias='from')

    @field_validator('from_')
    @classmethod
    def check_valid_sender(cls, v):
        if type(v) is not PhoneNumber and not search(r'^[a-zA-Z0-9]{1,15}$', v):
            raise VerifyError(f'You must specify a valid "from" value.')


class VoiceWorkflow(Workflow):
    @model_validator(mode='after')
    def remove_from_field_from_voice(self):
        self.from_ = None
        return self


class EmailWorkflow(Workflow):
    to: str
    from_: Optional[str] = Field(None, serialization_alias='from')


class VerifyRequest(BaseModel):
    brand: str = Field(..., min_length=1, max_length=16)
    workflow: List[Workflow]
    locale: Optional[VerifyLocale] = None
    channel_timeout: Optional[int] = Field(None, ge=60, le=900)
    client_ref: Optional[str] = Field(None, min_length=1, max_length=16)
    code_length: Optional[int] = Field(None, ge=4, le=10)
    code: Optional[str] = Field(None, pattern=r'^[a-zA-Z0-9]{4,10}$')

    @model_validator(mode='after')
    def remove_fields_if_only_silent_auth(self):
        if len(self.workflow) == 1 and isinstance(self.workflow[0], SilentAuthWorkflow):
            self.locale = None
            self.client_ref = None
            self.code_length = None
            self.code = None
        return self

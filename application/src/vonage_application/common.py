from typing import Literal, Optional, Union

from pydantic import BaseModel, Field, field_validator

from .enums import Region
from .errors import ApplicationError


class Url(BaseModel):
    address: str
    http_method: Optional[Literal['GET', 'POST']] = None


class VoiceUrl(Url):
    connection_timeout: Optional[int] = Field(None, ge=300, le=1000)
    socket_timeout: Optional[int] = Field(None, ge=1000, le=5000)


class VoiceWebhooks(BaseModel):
    answer_url: Optional[Url] = None
    fallback_answer_url: Optional[Url] = None
    event_url: Optional[Url] = None


class Voice(BaseModel):
    webhooks: Optional[VoiceWebhooks] = None
    signed_callbacks: Optional[bool] = None
    conversations_ttl: Optional[int] = Field(None, ge=1, le=9000)
    leg_persistence_time: Optional[int] = Field(None, ge=1, le=31)
    region: Optional[Region] = None


class RtcWebhooks(BaseModel):
    event_url: Optional[Url] = None


class Rtc(BaseModel):
    webhooks: Optional[RtcWebhooks] = None
    signed_callbacks: Optional[bool] = None


class MessagesWebhooks(BaseModel):
    inbound_url: Optional[Url] = None
    status_url: Optional[Url] = None


class Messages(BaseModel):
    version: Optional[str] = None
    webhooks: Optional[MessagesWebhooks] = None


class Vbc(BaseModel):
    pass


class VerifyWebhooks(BaseModel):
    status_url: Optional[Url] = None

    @field_validator('status_url')
    @classmethod
    def check_http_method(cls, v: Url):
        if v.http_method is not None and v.http_method != 'POST':
            raise ApplicationError('HTTP method must be POST')
        return v


class Verify(BaseModel):
    webhooks: Optional[VerifyWebhooks] = None
    version: Optional[str] = None


class Privacy(BaseModel):
    improve_ai: Optional[bool] = None


class ApplicationBase(BaseModel):
    name: str
    capabilities: Optional[Union[Voice, Rtc, Messages, Vbc, Verify]] = None
    privacy: Optional[Privacy] = None

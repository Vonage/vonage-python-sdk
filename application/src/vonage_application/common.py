from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .enums import Region
from .errors import ApplicationError


class ApplicationUrl(BaseModel):
    address: str
    http_method: Optional[Literal['GET', 'POST']] = None


class VoiceUrl(ApplicationUrl):
    connect_timeout: Optional[int] = Field(None, ge=300, le=1000)
    socket_timeout: Optional[int] = Field(None, ge=1000, le=10000)


class VoiceWebhooks(BaseModel):
    answer_url: Optional[VoiceUrl] = None
    fallback_answer_url: Optional[VoiceUrl] = None
    event_url: Optional[VoiceUrl] = None


class Voice(BaseModel):
    """Voice application capabilities."""

    webhooks: Optional[VoiceWebhooks] = None
    signed_callbacks: Optional[bool] = None
    conversations_ttl: Optional[int] = Field(None, ge=1, le=9000)
    leg_persistence_time: Optional[int] = Field(None, ge=1, le=31)
    region: Optional[Region] = None


class RtcWebhooks(BaseModel):
    event_url: Optional[ApplicationUrl] = None


class Rtc(BaseModel):
    """Real-Time Communications application capabilities."""

    webhooks: Optional[RtcWebhooks] = None
    signed_callbacks: Optional[bool] = None


class MessagesWebhooks(BaseModel):
    inbound_url: Optional[ApplicationUrl] = None
    status_url: Optional[ApplicationUrl] = None

    @field_validator('inbound_url', 'status_url')
    @classmethod
    def check_http_method(cls, v: ApplicationUrl):
        if v.http_method is not None and v.http_method != 'POST':
            raise ApplicationError('HTTP method must be POST')
        return v


class Messages(BaseModel):
    """Messages application capabilities."""

    webhooks: Optional[MessagesWebhooks] = None
    version: Optional[str] = None
    authenticate_inbound_media: Optional[bool] = None


class Vbc(BaseModel):
    """VBC capabilities.

    This object should be empty when creating or updating an application.
    """


class VerifyWebhooks(BaseModel):
    status_url: Optional[ApplicationUrl] = None

    @field_validator('status_url')
    @classmethod
    def check_http_method(cls, v: ApplicationUrl):
        if v.http_method is not None and v.http_method != 'POST':
            raise ApplicationError('HTTP method must be POST')
        return v


class Verify(BaseModel):
    """Verify application capabilities.

    Don't set the `version` field when creating or updating an application.
    """

    webhooks: Optional[VerifyWebhooks] = None
    version: Optional[str] = None


class Privacy(BaseModel):
    improve_ai: Optional[bool] = None


class Capabilities(BaseModel):
    voice: Optional[Voice] = None
    rtc: Optional[Rtc] = None
    messages: Optional[Messages] = None
    vbc: Optional[Vbc] = None
    verify: Optional[Verify] = None


class Keys(BaseModel):
    model_config = ConfigDict(extra='allow')

    public_key: Optional[str] = None


class ApplicationBase(BaseModel):
    """Base application object used in requests and responses when communicating with the Vonage
    Application API."""

    name: str
    capabilities: Optional[Capabilities] = None
    privacy: Optional[Privacy] = None
    keys: Optional[Keys] = None

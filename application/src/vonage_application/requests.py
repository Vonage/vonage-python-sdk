from typing import Optional

from pydantic import BaseModel


class ListApplicationsFilter(BaseModel):
    """Request object for listing users."""

    page_size: Optional[int] = 100
    page: int = None


class Webhook(BaseModel):
    address: str
    http_method: str
    connection_timeout: Optional[int] = None
    socket_timeout: Optional[int] = None


class Voice(BaseModel):
    webhooks: Webhook
    fallback_answer_url: Optional[Webhook] = None
    event_url: Optional[Webhook] = None
    signed_callbacks: bool
    conversations_ttl: int
    leg_persistence_time: int
    region: str


class Messages(BaseModel):
    version: str
    webhooks: Webhook


class RTC(BaseModel):
    webhooks: Webhook
    signed_callbacks: bool


class Meetings(BaseModel):
    webhooks: Webhook


class Verify(BaseModel):
    webhooks: Webhook


class Privacy(BaseModel):
    improve_ai: bool


class ApplicationBase(BaseModel):
    name: str
    capabilities: Optional[dict] = None
    voice: Optional[Voice] = None
    messages: Optional[Messages] = None
    rtc: Optional[RTC] = None
    meetings: Optional[Meetings] = None
    verify: Optional[Verify] = None
    privacy: Optional[Privacy] = None


class ApplicationOptions(ApplicationBase):
    keys: Optional[dict] = None

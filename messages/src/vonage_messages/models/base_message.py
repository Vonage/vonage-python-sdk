from typing import Optional

from pydantic import BaseModel, Field
from vonage_utils.types import PhoneNumber

from .enums import WebhookVersion


class BaseMessage(BaseModel):
    to: PhoneNumber
    client_ref: Optional[str] = Field(None, max_length=100)
    webhook_url: Optional[str] = None
    webhook_version: Optional[WebhookVersion] = None

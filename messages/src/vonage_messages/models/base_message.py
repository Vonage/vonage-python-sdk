from typing import Optional

from pydantic import BaseModel, Field
from vonage_utils.types import PhoneNumber

from .enums import WebhookVersion


class BaseMessage(BaseModel):
    """Model with base properties for a message.

    Args:
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    to: PhoneNumber
    client_ref: Optional[str] = Field(None, max_length=100)
    webhook_url: Optional[str] = None
    webhook_version: Optional[WebhookVersion] = None

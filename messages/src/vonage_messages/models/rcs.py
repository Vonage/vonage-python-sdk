from typing import Optional

from pydantic import BaseModel, Field
from vonage_utils.types import PhoneNumber

from .base_message import BaseMessage
from .enums import ChannelType, MessageType


class RcsResource(BaseModel):
    """Model for a resource in an RCS message.

    Args:
        url (str): The URL of the resource.
    """

    url: str


class BaseRcs(BaseMessage):
    """Model for a base RCS message.

    Args:
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (str): The sender's phone number in E.164 format. Don't use a leading plus sign.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    to: PhoneNumber
    from_: str = Field(..., serialization_alias='from', pattern='^[a-zA-Z0-9]+$')
    ttl: Optional[int] = Field(None, ge=300, le=259200)
    channel: ChannelType = ChannelType.RCS


class RcsText(BaseRcs):
    """Model for an RCS text message.

    Args:
        text (str): The text of the message.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (str): The sender's phone number in E.164 format. Don't use a leading plus sign.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    text: str = Field(..., min_length=1, max_length=3072)
    message_type: MessageType = MessageType.TEXT


class RcsImage(BaseRcs):
    """Model for an RCS image message.

    Args:
        image (RcsResource): The image resource.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (str): The sender's phone number in E.164 format. Don't use a leading plus sign.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    image: RcsResource
    message_type: MessageType = MessageType.IMAGE


class RcsVideo(BaseRcs):
    """Model for an RCS video message.

    Args:
        video (RcsResource): The video resource.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (str): The sender's phone number in E.164 format. Don't use a leading plus sign.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    video: RcsResource
    message_type: MessageType = MessageType.VIDEO


class RcsFile(BaseRcs):
    """Model for an RCS file message.

    Args:
        file (RcsResource): The file resource.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (str): The sender's phone number in E.164 format. Don't use a leading plus sign.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    file: RcsResource
    message_type: MessageType = MessageType.FILE


class RcsCustom(BaseRcs):
    """Model for an RCS custom message.

    Args:
        custom (dict): The custom message data.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (str): The sender's phone number in E.164 format. Don't use a leading plus sign.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    custom: dict
    message_type: MessageType = MessageType.CUSTOM

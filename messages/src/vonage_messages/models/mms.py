from typing import Optional, Union

from pydantic import BaseModel, Field
from vonage_utils.types import PhoneNumber

from .base_message import BaseMessage
from .enums import ChannelType, MessageType


class MmsResource(BaseModel):
    """Model for a resource in an MMS message.

    Args:
        url (str): The URL of the resource.
        caption (str, Optional): Additional text to accompany the resource.
    """

    url: str
    caption: Optional[str] = Field(None, min_length=1, max_length=2000)


class BaseMms(BaseMessage):
    """Model for a base MMS message.

    Args:
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (Union[PhoneNumber, str]): The sender's phone number in E.164 format. Don't use a leading plus sign.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    to: PhoneNumber
    from_: Union[PhoneNumber, str] = Field(..., serialization_alias='from')
    ttl: Optional[int] = Field(None, ge=300, le=259200)
    channel: ChannelType = ChannelType.MMS


class MmsImage(BaseMms):
    """Model for an MMS image message.

    Args:
        image (MmsResource): The image resource.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (Union[PhoneNumber, str]): The sender's phone number in E.164 format. Don't use a leading plus sign.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    image: MmsResource
    message_type: MessageType = MessageType.IMAGE


class MmsVcard(BaseMms):
    """Model for an MMS vCard message.

    Args:
        vcard (MmsResource): The vCard resource.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (Union[PhoneNumber, str]): The sender's phone number in E.164 format. Don't use a leading plus sign.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    vcard: MmsResource
    message_type: MessageType = MessageType.VCARD


class MmsAudio(BaseMms):
    """Model for an MMS audio message.

    Args:
        audio (MmsResource): The audio resource.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (Union[PhoneNumber, str]): The sender's phone number in E.164 format. Don't use a leading plus sign.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    audio: MmsResource
    message_type: MessageType = MessageType.AUDIO


class MmsVideo(BaseMms):
    """Model for an MMS video message.

    Args:
        video (MmsResource): The video resource.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (Union[PhoneNumber, str]): The sender's phone number in E.164 format. Don't use a leading plus sign.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    video: MmsResource
    message_type: MessageType = MessageType.VIDEO

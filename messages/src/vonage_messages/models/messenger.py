from typing import Literal, Optional

from pydantic import BaseModel, Field, model_validator

from .base_message import BaseMessage
from .enums import ChannelType, MessageType


class MessengerResource(BaseModel):
    """Model for a resource in a Messenger message.

    Args:
        url (str): The URL of the resource.
    """

    url: str


class MessengerOptions(BaseModel):
    """Model for Messenger options.

    Args:
        category (str, Optional): The category of the message. The use of different category tags enables the business to send messages for different use cases.
        tag (str, Optional): A tag describing the type and relevance of the 1:1 communication between your app and the end user.
    """

    category: Optional[Literal['response', 'update', 'message_tag']] = None
    tag: Optional[str] = None

    @model_validator(mode='after')
    def check_tag_if_category_message_tag(self):
        if self.category == 'message_tag' and not self.tag:
            raise ValueError('"tag" is required when "category" == "message_tag"')
        return self


class BaseMessenger(BaseMessage):
    """Model for a base Messenger message.

    Args:
        to (str): The ID of the message recipient.
        from_ (str): The ID of the message sender.
        messenger (MessengerOptions, Optional): Messenger options.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    to: str = Field(..., min_length=1, max_length=50)
    from_: str = Field(..., min_length=1, max_length=50, serialization_alias='from')
    messenger: Optional[MessengerOptions] = None
    channel: ChannelType = ChannelType.MESSENGER


class MessengerText(BaseMessenger):
    """Model for a Messenger text message.

    Args:
        text (str): The text of the message.
        to (str): The ID of the message recipient.
        from_ (str): The ID of the message sender.
        messenger (MessengerOptions, Optional): Messenger options.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    text: str = Field(..., max_length=640)
    message_type: MessageType = MessageType.TEXT


class MessengerImage(BaseMessenger):
    """Model for a Messenger image message.

    Args:
        image (MessengerResource): The image resource.
        to (str): The ID of the message recipient.
        from_ (str): The ID of the message sender.
        messenger (MessengerOptions, Optional): Messenger options.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    image: MessengerResource
    message_type: MessageType = MessageType.IMAGE


class MessengerAudio(BaseMessenger):
    """Model for a Messenger audio message.

    Args:
        audio (MessengerResource): The audio resource.
        to (str): The ID of the message recipient.
        from_ (str): The ID of the message sender.
        messenger (MessengerOptions, Optional): Messenger options.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    audio: MessengerResource
    message_type: MessageType = MessageType.AUDIO


class MessengerVideo(BaseMessenger):
    """Model for a Messenger video message.

    Args:
        video (MessengerResource): The video resource.
        to (str): The ID of the message recipient.
        from_ (str): The ID of the message sender.
        messenger (MessengerOptions, Optional): Messenger options.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    video: MessengerResource
    message_type: MessageType = MessageType.VIDEO


class MessengerFile(BaseMessenger):
    """Model for a Messenger file message.

    Args:
        file (MessengerResource): The file resource.
        to (str): The ID of the message recipient.
        from_ (str): The ID of the message sender.
        messenger (MessengerOptions, Optional): Messenger options.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    file: MessengerResource
    message_type: MessageType = MessageType.FILE

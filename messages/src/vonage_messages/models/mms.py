from typing import Optional, Union

from pydantic import BaseModel, Field
from vonage_utils.types import PhoneNumber

from .base_message import BaseMessage
from .enums import ChannelType, MessageType, MmsContentItemType


class MmsResource(BaseModel):
    """Model for a resource in an MMS message.

    Args:
        url (str): The URL of the resource.
        caption (str, Optional): Additional text to accompany the resource, with a maximum length of 3000 characters.
    """

    url: str
    caption: Optional[str] = Field(None, min_length=1, max_length=3000)


class BaseMms(BaseMessage):
    """Model for a base MMS message.

    Args:
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (Union[PhoneNumber, str]): The sender's phone number in E.164 format. Don't use a leading plus sign.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        trusted_recipient (bool, Optional): Whether the recipient is a trusted recipient. Setting this parameter to true overrides, on a per-message basis, any protections set up via Fraud Defender. Defaults to false.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    to: PhoneNumber
    from_: Union[PhoneNumber, str] = Field(..., serialization_alias='from')
    ttl: Optional[int] = Field(None, ge=300, le=259200)
    trusted_recipient: Optional[bool] = None
    channel: ChannelType = ChannelType.MMS


class MmsText(BaseMms):
    """Model for an MMS text message.

    Args:
        text (str): The text of the message.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (Union[PhoneNumber, str]): The sender's phone number in E.164 format. Don't use a leading plus sign.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        trusted_recipient (bool, Optional): Whether the recipient is a trusted recipient. Setting this parameter to true overrides, on a per-message basis, any protections set up via Fraud Defender. Defaults to false.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    text: str
    message_type: MessageType = MessageType.TEXT


class MmsImage(BaseMms):
    """Model for an MMS image message.

    Args:
        image (MmsResource): The image resource.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (Union[PhoneNumber, str]): The sender's phone number in E.164 format. Don't use a leading plus sign.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        trusted_recipient (bool, Optional): Whether the recipient is a trusted recipient. Setting this parameter to true overrides, on a per-message basis, any protections set up via Fraud Defender. Defaults to false.
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
        trusted_recipient (bool, Optional): Whether the recipient is a trusted recipient. Setting this parameter to true overrides, on a per-message basis, any protections set up via Fraud Defender. Defaults to false.
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
        trusted_recipient (bool, Optional): Whether the recipient is a trusted recipient. Setting this parameter to true overrides, on a per-message basis, any protections set up via Fraud Defender. Defaults to false.
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
        trusted_recipient (bool, Optional): Whether the recipient is a trusted recipient. Setting this parameter to true overrides, on a per-message basis, any protections set up via Fraud Defender. Defaults to false.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    video: MmsResource
    message_type: MessageType = MessageType.VIDEO


class MmsFile(BaseMms):
    """Model for an MMS file message.

    Args:
        file (MmsResource): The file resource.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (Union[PhoneNumber, str]): The sender's phone number in E.164 format. Don't use a leading plus sign.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        trusted_recipient (bool, Optional): Whether the recipient is a trusted recipient. Setting this parameter to true overrides, on a per-message basis, any protections set up via Fraud Defender. Defaults to false.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    file: MmsResource
    message_type: MessageType = MessageType.FILE


class MmsContentItemImage(MmsResource):
    """Model for an image content item in an MMS Content message.

    Args:
        url (str): The URL of the content item.
        caption (str, Optional): Additional text to accompany the content item, with a maximum length of 3000 characters.
    """

    type_: MmsContentItemType = Field(
        MmsContentItemType.IMAGE, serialization_alias='type'
    )


class MmsContentItemAudio(MmsResource):
    """Model for an audio content item in an MMS Content message.

    Args:
        url (str): The URL of the content item.
        caption (str, Optional): Additional text to accompany the content item, with a maximum length of 3000 characters.
    """

    type_: MmsContentItemType = Field(
        MmsContentItemType.AUDIO, serialization_alias='type'
    )


class MmsContentItemVideo(MmsResource):
    """Model for a video content item in an MMS Content message.

    Args:
        url (str): The URL of the content item.
        caption (str, Optional): Additional text to accompany the content item, with a maximum length of 3000 characters.
    """

    type_: MmsContentItemType = Field(
        MmsContentItemType.VIDEO, serialization_alias='type'
    )


class MmsContentItemFile(MmsResource):
    """Model for a file content item in an MMS Content message.

    Args:
        url (str): The URL of the content item.
        caption (str, Optional): Additional text to accompany the content item, with a maximum length of 3000 characters.
    """

    type_: MmsContentItemType = Field(MmsContentItemType.FILE, serialization_alias='type')


class MmsContentItemVcard(MmsResource):
    """Model for a vCard content item in an MMS Content message.

    Args:
        url (str): The URL of the content item.
        caption (str, Optional): Additional text to accompany the content item, with a maximum length of 3000 characters.
    """

    type_: MmsContentItemType = Field(
        MmsContentItemType.VCARD, serialization_alias='type'
    )


class MmsContent(BaseMms):
    """Model for an MMS message with content that can be of various types.

    Args:
        content (list[MmsContentItem]): A list of content items for the message (images, audio, video, files, or vCards).
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a leading plus sign.
        from_ (Union[PhoneNumber, str]): The sender's phone number in E.164 format. Don't use a leading plus sign.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        trusted_recipient (bool, Optional): Whether the recipient is a trusted recipient. Setting this parameter to true overrides, on a per-message basis, any protections set up via Fraud Defender. Defaults to false.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    content: list[
        Union[
            MmsContentItemImage,
            MmsContentItemAudio,
            MmsContentItemVideo,
            MmsContentItemFile,
            MmsContentItemVcard,
        ]
    ]
    message_type: MessageType = MessageType.CONTENT

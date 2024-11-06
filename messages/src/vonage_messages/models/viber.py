from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator

from .base_message import BaseMessage
from .enums import ChannelType, MessageType


class ViberAction(BaseModel):
    """Model for an action button in a Viber message.

    Args:
        url (str): A URL which is requested when the action button is clicked.
        text (str): Text which is rendered on the action button.
    """

    url: str
    text: str = Field(..., max_length=30)


class ViberOptions(BaseModel):
    """Model for Viber message options.

    Args:
        category (Literal['transaction', 'promotion'], Optional): The use of different
            category tags enables the business to send messages for different use cases.
            For Viber Business Messages the first message sent from a business to a user
            must be personal, informative and a targeted message - not promotional.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        type (Literal['string', 'template'], Optional): The type of the message. To use
            "template", please contact your Vonage Account Manager to setup your templates.
    """

    category: Literal['transaction', 'promotion'] = None
    ttl: Optional[int] = Field(None, ge=30, le=259200)
    type: Optional[Literal['string', 'template']] = None


class BaseViber(BaseMessage):
    """Model for a base Viber message.

    Args:
        to (str): The recipient's phone number in E.164 format. Don't use a leading
            plus sign.
        from_ (str): The sender's phone number in E.164 format. Don't use a leading
            plus sign.
        viber_service (ViberOptions, Optional): Viber message options.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be
            sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API
            will be used to send Status Webhook messages for this particular message.
    """

    from_: str = Field(..., min_length=1, max_length=50, serialization_alias='from')
    viber_service: Optional[ViberOptions] = None
    channel: ChannelType = ChannelType.VIBER


class ViberTextOptions(ViberOptions):
    """Model for Viber text message options.

    Args:
        action (ViberAction, Optional): An action button to include in the message.
        category (Literal['transaction', 'promotion'], Optional): The use of different
            category tags enables the business to send messages for different use cases.
            For Viber Business Messages the first message sent from a business to a user
            must be personal, informative and a targeted message - not promotional.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        type (Literal['string', 'template'], Optional): The type of the message. To use
            "template", please contact your Vonage Account Manager to setup your templates.
    """

    action: Optional[ViberAction] = None


class ViberText(BaseViber):
    """Model for a Viber text message.

    Args:
        text (str): The text of the message.
        to (str): The recipient's phone number in E.164 format. Don't use a leading
            plus sign.
        from_ (str): The sender's phone number in E.164 format. Don't use a leading
            plus sign.
        viber_service (ViberTextOptions, Optional): Viber text message options.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be
            sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API
            will be used to send Status Webhook messages for this particular message.
    """

    text: str = Field(..., max_length=1000)
    viber_service: Optional[ViberTextOptions] = None
    message_type: MessageType = MessageType.TEXT


class ViberImageResource(BaseModel):
    """Model for an image resource in a Viber message.

    Args:
        url (str): The URL of the image.
        caption (str, Optional): Additional text to accompany the image.
    """

    url: str
    caption: Optional[str] = None


class ViberImageOptions(ViberOptions):
    """Model for Viber image message options.

    Args:
        action (ViberAction, Optional): An action button to include in the message.
        category (Literal['transaction', 'promotion'], Optional): The use of different
            category tags enables the business to send messages for different use cases.
            For Viber Business Messages the first message sent from a business to a user
            must be personal, informative and a targeted message - not promotional.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        type (Literal['string', 'template'], Optional): The type of the message. To use
            "template", please contact your Vonage Account Manager to setup your templates.
    """

    action: Optional[ViberAction] = None


class ViberImage(BaseViber):
    """Model for a Viber image message.

    Args:
        image (ViberImageResource): The image resource.
        to (str): The recipient's phone number in E.164 format. Don't use a leading
            plus sign.
        from_ (str): The sender's phone number in E.164 format. Don't use a leading
            plus sign.
        viber_service (ViberImageOptions, Optional): Viber image message options.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be
            sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API
            will be used to send Status Webhook messages for this particular message.
    """

    image: ViberImageResource
    viber_service: Optional[ViberImageOptions] = None
    message_type: MessageType = MessageType.IMAGE


class ViberVideoResource(BaseModel):
    """Model for a video resource in a Viber message.

    Args:
        url (str): The URL of the video.
        thumb_url (str): The URL of a thumbnail image to display before the video is
            played.
        caption (str, Optional): Additional text to accompany the video.
    """

    url: str
    thumb_url: str = Field(..., max_length=1000)
    caption: Optional[str] = Field(None, max_length=1000)


class ViberVideoOptions(ViberOptions):
    """Model for Viber video message options.

    Args:
        duration (str): The duration of the video in seconds.
        file_size (str): The size of the video file in MB.
        action (ViberAction, Optional): An action button to include in the message.
        category (Literal['transaction', 'promotion'], Optional): The use of different
            category tags enables the business to send messages for different use cases.
            For Viber Business Messages the first message sent from a business to a user
            must be personal, informative and a targeted message - not promotional.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        type (Literal['string', 'template'], Optional): The type of the message. To use
            "template", please contact your Vonage Account Manager to setup your templates.
    """

    duration: str
    file_size: str

    @field_validator('duration')
    @classmethod
    def validate_duration(cls, value):
        value_int = int(value)
        if not 1 <= value_int <= 600:
            raise ValueError('"Duration" must be a number between 1 and 600.')
        return value

    @field_validator('file_size')
    @classmethod
    def validate_file_size(cls, value):
        value_int = int(value)
        if not 1 <= value_int <= 200:
            raise ValueError('"File size" must be a number between 1 and 200.')
        return value


class ViberVideo(BaseViber):
    """Model for a Viber video message.

    Args:
        video (ViberVideoResource): The video resource.
        to (str): The recipient's phone number in E.164 format. Don't use a leading
            plus sign.
        from_ (str): The sender's phone number in E.164 format. Don't use a leading
            plus sign.
        viber_service (ViberVideoOptions, Optional): Viber video message options.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be
            sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API
            will be used to send Status Webhook messages for this particular message.
    """

    video: ViberVideoResource
    viber_service: ViberVideoOptions
    message_type: MessageType = MessageType.VIDEO


class ViberFileResource(BaseModel):
    """Model for a file resource in a Viber message.

    Args:
        url (str): The URL for the file attachment or the path for the location of the
            file attachment. If name is included, can just be the path. If `name` is not
            included, must include the filename and extension.
        name (str, Optional): The name and extension of the file.
    """

    url: str
    name: Optional[str] = Field(None, max_length=25)


class ViberFileOptions(ViberOptions):
    """Model for Viber file message options.

    Args:
        category (Literal['transaction', 'promotion'], Optional): The use of different
            category tags enables the business to send messages for different use cases.
            For Viber Business Messages the first message sent from a business to a user
            must be personal, informative and a targeted message - not promotional.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        type (Literal['string', 'template'], Optional): The type of the message. To use
            "template", please contact your Vonage Account Manager to setup your templates.
    """


class ViberFile(BaseViber):
    """Model for a Viber file message.

    Args:
        file (ViberFileResource): The file resource.
        to (str): The recipient's phone number in E.164 format. Don't use a leading
            plus sign.
        from_ (str): The sender's phone number in E.164 format. Don't use a leading
            plus sign.
        viber_service (ViberFileOptions, Optional): Viber file message options.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be
            sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API
            will be used to send Status Webhook messages for this particular message.
    """

    file: ViberFileResource
    viber_service: Optional[ViberFileOptions] = None
    message_type: MessageType = MessageType.FILE

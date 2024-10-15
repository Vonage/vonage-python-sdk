from typing import Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field
from vonage_utils.types import PhoneNumber

from .base_message import BaseMessage
from .enums import ChannelType, MessageType


class WhatsappContext(BaseModel):
    """Model for the context of a WhatsApp message. This is used for quoting/replying.

    /reacting to a specific message in a conversation. When used for quoting or replying,
    the WhatsApp UI will display the new message along with a contextual bubble that
    displays the quoted/replied to message's content. When used for reacting, the WhatsApp
    UI will display the reaction emoji below the reacted to message.

    Args:
        message_uuid (str): The UUID of the message to quote/reply/react to.
    """

    message_uuid: str


class BaseWhatsapp(BaseMessage):
    """Model for a base WhatsApp message.

    Args:
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a
            leading plus sign.
        from_ (Union[PhoneNumber, str]): The sender's phone number in E.164 format.
            Don't use a leading plus sign.
        context (WhatsappContext, Optional): Used for quoting/replying/reacting to a
            specific message in a conversation. When used for quoting or replying,
            the WhatsApp UI will display the new message along with a contextual bubble
            that displays the quoted/replied to message's content. When used for
            reacting, the WhatsApp UI will display the reaction emoji below the reacted
            to message.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be
            sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API
            will be used to send Status Webhook messages for this particular message.
    """

    from_: Union[PhoneNumber, str] = Field(..., serialization_alias='from')
    context: Optional[WhatsappContext] = None
    channel: ChannelType = ChannelType.WHATSAPP


class WhatsappText(BaseWhatsapp):
    """Model for a WhatsApp text message.

    Args:
        text (str): The text of the message.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a
            leading plus sign.
        from_ (Union[PhoneNumber, str]): The sender's phone number in E.164 format.
            Don't use a leading plus sign.
        context (WhatsappContext, Optional): Used for quoting/replying/reacting to a
            specific message in a conversation. When used for quoting or replying,
            the WhatsApp UI will display the new message along with a contextual bubble
            that displays the quoted/replied to message's content. When used for
            reacting, the WhatsApp UI will display the reaction emoji below the reacted
            to message.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be
            sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API
            will be used to send Status Webhook messages for this particular message.
    """

    text: str = Field(..., max_length=4096)
    message_type: MessageType = MessageType.TEXT


class WhatsappImageResource(BaseModel):
    """Model for an image attachment in a WhatsApp message.

    Args:
        url (str): The publicly accessible URL of the image attachment.
        caption (Optional[str]): Additional text to accompany the image.
    """

    url: str
    caption: Optional[str] = Field(None, min_length=1, max_length=3000)


class WhatsappImage(BaseWhatsapp):
    """Model for a WhatsApp image message.

    Args:
        image (WhatsappImageResource): The image attachment.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a
            leading plus sign.
        from_ (Union[PhoneNumber, str]): The sender's phone number in E.164 format.
            Don't use a leading plus sign.
        context (WhatsappContext, Optional): Used for quoting/replying/reacting to a
            specific message in a conversation. When used for quoting or replying,
            the WhatsApp UI will display the new message along with a contextual bubble
            that displays the quoted/replied to message's content. When used for
            reacting, the WhatsApp UI will display the reaction emoji below the reacted
            to message.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be
            sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API
            will be used to send Status Webhook messages for this particular message.
    """

    image: WhatsappImageResource
    message_type: MessageType = MessageType.IMAGE


class WhatsappAudioResource(BaseModel):
    """Model for an audio attachment in a WhatsApp message.

    Args:
        url (str): The publicly accessible URL of the audio attachment.
    """

    url: str = Field(..., min_length=10, max_length=2000)


class WhatsappAudio(BaseWhatsapp):
    """Model for a WhatsApp audio message.

    Args:
        audio (WhatsappAudioResource): The audio attachment.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a
            leading plus sign.
        from_ (Union[PhoneNumber, str]): The sender's phone number in E.164 format.
            Don't use a leading plus sign.
        context (WhatsappContext, Optional): Used for quoting/replying/reacting to a
            specific message in a conversation. When used for quoting or replying,
            the WhatsApp UI will display the new message along with a contextual bubble
            that displays the quoted/replied to message's content. When used for
            reacting, the WhatsApp UI will display the reaction emoji below the reacted
            to message.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be
            sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API
            will be used to send Status Webhook messages for this particular message.
    """

    audio: WhatsappAudioResource
    message_type: MessageType = MessageType.AUDIO


class WhatsappVideoResource(BaseModel):
    """Model for a video attachment in a WhatsApp message.

    Args:
        url (str): The publicly accessible URL of the video attachment.
        caption (Optional[str]): Additional text to accompany the video.
    """

    url: str
    caption: Optional[str] = None


class WhatsappVideo(BaseWhatsapp):
    """Model for a WhatsApp video message.

    Args:
        video (WhatsappVideoResource): The video attachment.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a
            leading plus sign.
        from_ (Union[PhoneNumber, str]): The sender's phone number in E.164 format.
            Don't use a leading plus sign.
        context (WhatsappContext, Optional): Used for quoting/replying/reacting to a
            specific message in a conversation. When used for quoting or replying,
            the WhatsApp UI will display the new message along with a contextual bubble
            that displays the quoted/replied to message's content. When used for
            reacting, the WhatsApp UI will display the reaction emoji below the reacted
            to message.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be
            sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API
            will be used to send Status Webhook messages for this particular message.
    """

    video: WhatsappVideoResource
    message_type: MessageType = MessageType.VIDEO


class WhatsappFileResource(BaseModel):
    """Model for a file attachment in a WhatsApp message.

    Args:
        url (str): The publicly accessible URL of the file attachment.
        caption (Optional[str]): Additional text to accompany the file.
        name (Optional[str]): Optional parameter that specifies the name of the file
            being sent. If not included, the value for `caption` will be used as the
            file name. If neither `name` or `caption` are included, the file name will be
            parsed from the url.
    """

    url: str
    caption: Optional[str] = None
    name: Optional[str] = None


class WhatsappFile(BaseWhatsapp):
    """Model for a WhatsApp file message.

    Args:
        file (WhatsappFileResource): The file attachment.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a
            leading plus sign.
        from_ (Union[PhoneNumber, str]): The sender's phone number in E.164 format.
            Don't use a leading plus sign.
        context (WhatsappContext, Optional): Used for quoting/replying/reacting to a
            specific message in a conversation. When used for quoting or replying,
            the WhatsApp UI will display the new message along with a contextual bubble
            that displays the quoted/replied to message's content. When used for
            reacting, the WhatsApp UI will display the reaction emoji below the reacted
            to message.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be
            sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API
            will be used to send Status Webhook messages for this particular message.
    """

    file: WhatsappFileResource
    message_type: MessageType = MessageType.FILE


class WhatsappTemplateResource(BaseModel):
    """Model for a WhatsApp template message.

    Args:
        name (str): The name of the template. For WhatsApp use your WhatsApp namespace
            (available via Facebook Business Manager), followed by a colon : and the
            name of the template to use.
        parameters (Optional[list[str]]): The parameters to be used in the template.
            An array of strings, with the first string being used for 1 in the template,
            the second being 2, etc. Only required if the template specified by name
            contains parameters.
    """

    name: str
    parameters: Optional[list[str]] = None

    model_config = ConfigDict(extra='allow')


class WhatsappTemplateSettings(BaseModel):
    """Model for WhatsApp template settings.

    Args:
        locale (Optional[str]): The BCP 47 language of the template.
        policy (Optional[Literal['deterministic']]): Policy for resolving what language
            template to use. As of now, the only valid choice is deterministic.
    """

    locale: Optional[str] = 'en_US'
    policy: Optional[Literal['deterministic']] = None


class WhatsappTemplate(BaseWhatsapp):
    """Model for a WhatsApp template message.

    Args:
        template (WhatsappTemplateResource): The template to use.
        whatsapp (WhatsappTemplateSettings): WhatsApp template settings.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a
            leading plus sign.
        from_ (Union[PhoneNumber, str]): The sender's phone number in E.164 format.
            Don't use a leading plus sign.
        context (WhatsappContext, Optional): Used for quoting/replying/reacting to a
            specific message in a conversation. When used for quoting or replying,
            the WhatsApp UI will display the new message along with a contextual bubble
            that displays the quoted/replied to message's content. When used for
            reacting, the WhatsApp UI will display the reaction emoji below the reacted
            to message.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be
            sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API
            will be used to send Status Webhook messages for this particular message.
    """

    template: WhatsappTemplateResource
    whatsapp: WhatsappTemplateSettings = WhatsappTemplateSettings()
    message_type: MessageType = MessageType.TEMPLATE


class WhatsappStickerUrl(BaseModel):
    """Model for a sticker attachment in a WhatsApp message.

    Args:
        url (str): The publicly accessible URL of the sticker attachment.
    """

    url: str


class WhatsappStickerId(BaseModel):
    """Model for a sticker attachment in a WhatsApp message.

    Args:
        id (str): The id of the sticker in relation to a specific WhatsApp deployment.
    """

    id: str


class WhatsappSticker(BaseWhatsapp):
    """Model for a WhatsApp sticker message.

    Args:
        sticker (Union[WhatsappStickerUrl, WhatsappStickerId]): The sticker attachment.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a
            leading plus sign.
        from_ (Union[PhoneNumber, str]): The sender's phone number in E.164 format.
            Don't use a leading plus sign.
        context (WhatsappContext, Optional): Used for quoting/replying/reacting to a
            specific message in a conversation. When used for quoting or replying,
            the WhatsApp UI will display the new message along with a contextual bubble
            that displays the quoted/replied to message's content. When used for
            reacting, the WhatsApp UI will display the reaction emoji below the reacted
            to message.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be
            sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API
            will be used to send Status Webhook messages for this particular message.
    """

    sticker: Union[WhatsappStickerUrl, WhatsappStickerId]
    message_type: MessageType = MessageType.STICKER


class WhatsappCustom(BaseWhatsapp):
    """Model for a WhatsApp custom message.

    Args:
        custom (dict): A custom payload, which is passed directly to WhatsApp for certain
            features such as templates and interactive messages. The schema of a custom
            object can vary widely.
        to (PhoneNumber): The recipient's phone number in E.164 format. Don't use a
            leading plus sign.
        from_ (Union[PhoneNumber, str]): The sender's phone number in E.164 format.
            Don't use a leading plus sign.
        context (WhatsappContext, Optional): Used for quoting/replying/reacting to a
            specific message in a conversation. When used for quoting or replying,
            the WhatsApp UI will display the new message along with a contextual bubble
            that displays the quoted/replied to message's content. When used for
            reacting, the WhatsApp UI will display the reaction emoji below the reacted
            to message.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be
            sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API
            will be used to send Status Webhook messages for this particular message.
    """

    custom: Optional[dict] = None
    message_type: MessageType = MessageType.CUSTOM

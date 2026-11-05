from typing import Optional, Union

from pydantic import BaseModel, Field

from .base_message import BaseMessage
from .enums import (
    ChannelType,
    EmailContentItemType,
    EmailImportance,
    EmailPriority,
    EmailSensitivity,
    MessageType,
)


class EmailAdditionalRecipient(BaseModel):
    """Model for an additional recipient in an email message.

    Args:
        address (str): The email address of the additional recipient.
        name (str, Optional): The name of the additional recipient.
    """

    address: str
    name: Optional[str] = Field(None, min_length=1, max_length=100)


class EmailOptions(BaseModel):
    """Model for email options.

    Args:
        subject (str): The subject of the email.
        to_name (str, Optional): The display name of the recipient.
        from_name (str, Optional): The display name of the sender.
        importance (EmailImportance, Optional): The importance of the email.
        priority (EmailPriority, Optional): The priority of the email.
        sensitivity (EmailSensitivity, Optional): The sensitivity of the email.
        reply_to (str, Optional): The reply-to email address.
        cc (list[EmailAdditionalRecipient], Optional): A list of additional recipients to be CC'd.
        bcc (list[EmailAdditionalRecipient], Optional): A list of additional recipients to be BCC'd.
    """

    subject: str
    to_name: Optional[str] = Field(None, min_length=1, max_length=100)
    from_name: Optional[str] = Field(None, min_length=1, max_length=100)
    importance: Optional[EmailImportance] = None
    priority: Optional[EmailPriority] = None
    sensitivity: Optional[EmailSensitivity] = None
    reply_to: Optional[str] = None
    cc: Optional[list[EmailAdditionalRecipient]] = None
    bcc: Optional[list[EmailAdditionalRecipient]] = None


class BaseEmail(BaseMessage):
    """Model for a base email message.

    Args:
        to (str): The recipient's email address.
        from_ (str): The sender's email address.
        email (EmailOptions): The specific settings for this email message.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    to: str
    from_: str = Field(..., serialization_alias='from')
    channel: ChannelType = ChannelType.EMAIL
    email: EmailOptions


class EmailText(BaseEmail):
    """Model for an email text message.

    Args:
        text (str): The text of the message.
        to (str): The recipient's email address.
        from_ (str): The sender's email address.
        email (EmailOptions): The specific settings for this email message.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    text: str
    message_type: MessageType = MessageType.TEXT


class EmailHtmlContent(BaseModel):
    """Model for the HTML content of an email message.

    Args:
        body (str): The HTML content as a string.
    """

    body: str


class EmailHtml(BaseEmail):
    """Model for an email HTML message.

    Args:
        html (EmailHtmlContent): The HTML content of the message.
        to (str): The recipient's email address.
        from_ (str): The sender's email address.
        email (EmailOptions): The specific settings for this email message.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    html: EmailHtmlContent
    message_type: MessageType = MessageType.HTML


class EmailContentItemText(BaseModel):
    """Model for a text content item in an email content message.

    Args:
        text (str): The text of the content item.
    """

    type_: EmailContentItemType = Field(
        EmailContentItemType.TEXT, serialization_alias='type'
    )
    text: str


class EmailContentItemHtml(BaseModel):
    """Model for an HTML content item in an email content message.

    Args:
        body (str): The HTML content as a string.
    """

    type_: EmailContentItemType = Field(
        EmailContentItemType.HTML, serialization_alias='type'
    )
    body: str


class EmailContent(BaseEmail):
    """Model for an email message with content that can be of various types.

    Args:
        content (list[EmailContentItem]): A list of content items for the message (text or HTML).
        to (str): The recipient's email address.
        from_ (str): The sender's email address.
        email (EmailOptions): The specific settings for this email message.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    content: list[
        Union[
            EmailContentItemText,
            EmailContentItemHtml,
        ]
    ]
    message_type: MessageType = MessageType.CONTENT

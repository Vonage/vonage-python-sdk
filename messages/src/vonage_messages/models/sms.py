from typing import Optional, Union

from pydantic import BaseModel, Field
from vonage_utils.types import PhoneNumber

from .base_message import BaseMessage
from .enums import ChannelType, EncodingType, MessageType


class SmsOptions(BaseModel):
    """Model for SMS options.

    Args:
        encoding_type (EncodingType, Optional): The encoding type to use for the message.
            If set to either text or unicode the specified type will be used.
            If set to auto (the default), the Messages API will automatically set
            the type based on the content.
        content_id (str, Optional): A string parameter that satisfies regulatory
            requirements when sending an SMS to specific countries. Not needed unless
            sending SMS in a country that requires a specific content ID.
        entity_id (str, Optional):  A string parameter that satisfies regulatory
            requirements when sending an SMS to specific countries. Not needed unless
            sending SMS in a country that requires a specific entity ID.
        pool_id (str, Optional): The ID of the Number Pool to use as the sender of this message.
            If specified, a number from the pool will be used as the from number.
            The from number is still required even when specifying a pool_id and will be used as a fall-back if the number pool cannot be used.
            See the Number Pools documentation for more information: https://developer.vonage.com/numbers/number-pools-api/overview.
    """

    encoding_type: Optional[EncodingType] = None
    content_id: Optional[str] = None
    entity_id: Optional[str] = None
    pool_id: Optional[str] = None


class Sms(BaseMessage):
    """Model for an SMS message.

    Args:
        to (PhoneNumber): The recipient's phone number in E.164 format.
            Don't use a leading plus sign.
        from_ (Union[PhoneNumber, str]): The sender's phone number in E.164 format.
            Don't use a leading plus sign.
        text (str): The text of the message.
        ttl (int, Optional): The duration in seconds for which the message is valid.
        trusted_recipient (bool, Optional): Whether the recipient is a trusted recipient. Setting this parameter to true overrides, on a per-message basis, any protections set up via Fraud Defender. Defaults to false.
        sms (SmsOptions, Optional): SMS options.
        client_ref (str, Optional): An optional client reference.
        webhook_url (str, Optional): The URL to which Status Webhook messages will be sent for this particular message.
        webhook_version (WebhookVersion, Optional): Which version of the Messages API will be used to send Status Webhook messages for this particular message.
    """

    from_: Union[PhoneNumber, str] = Field(..., serialization_alias='from')
    text: str = Field(..., max_length=1000)
    ttl: Optional[int] = Field(None, ge=20, le=604800)
    trusted_recipient: Optional[bool] = None
    sms: Optional[SmsOptions] = None
    channel: ChannelType = ChannelType.SMS
    message_type: MessageType = MessageType.TEXT

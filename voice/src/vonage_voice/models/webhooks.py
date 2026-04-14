from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class AnswerWebhook(BaseModel):
    """Model for the Voice API Answer webhook payload.

    Args:
        to (str, Optional): The number or endpoint that answered the call.
        from_ (str, Optional): The number or endpoint that initiated the call.
        from_user (str, Optional): The Client SDK user that initiated the call.
        endpoint_type (str, Optional): The type of endpoint that answered the call.
        uuid (str, Optional): The unique identifier for this call.
        conversation_uuid (str, Optional): The unique identifier for this conversation.
        region_url (str, Optional): Regional API endpoint to control the call.
        custom_data (dict, Optional): Custom data object passed from the Client SDK.
        sipheader_user_to_user (str, Optional): Content of the SIP User-to-User header,
            received as the `SipHeader_User-to-User` parameter on the webhook.
    """

    model_config = ConfigDict(populate_by_name=True)

    to: Optional[str] = None
    from_: Optional[str] = Field(None, alias='from')
    from_user: Optional[str] = None
    endpoint_type: Optional[str] = None
    uuid: Optional[str] = None
    conversation_uuid: Optional[str] = None
    region_url: Optional[str] = None
    custom_data: Optional[dict] = None
    sipheader_user_to_user: Optional[str] = Field(
        None,
        validation_alias='SipHeader_User-to-User',
        serialization_alias='SipHeader_User-to-User',
    )

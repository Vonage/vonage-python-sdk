from typing import Optional

from pydantic import BaseModel, Field


class MessageResponse(BaseModel):
    """Individual message response model.

    Args:
        to (str): The recipient's phone number in E.164 format.
        message_id (str): The message ID.
        status (str): The status of the message.
        remaining_balance (str): The estimated remaining balance.
        message_price (str): The estimated message cost.
        network (str): The estimated ID of the network of the recipient
        client_ref (str, Optional): If a `client_ref` was included when sending the SMS,
            this field will be included and hold the value that was sent.
        account_ref (str, Optional): An optional string used to identify separate
            accounts using the SMS endpoint for billing purposes. To use this feature,
            please email support.
    """

    to: str
    message_id: str = Field(..., validation_alias='message-id')
    status: str
    remaining_balance: str = Field(..., validation_alias='remaining-balance')
    message_price: str = Field(..., validation_alias='message-price')
    network: str
    client_ref: Optional[str] = Field(None, validation_alias='client-ref')
    account_ref: Optional[str] = Field(None, validation_alias='account-ref')


class SmsResponse(BaseModel):
    """Response recieved after sending an SMS.

    Args:
        message_count (str): The number of messages sent.
        messages (list[MessageResponse]): A list of individual message responses. See
            `MessageResponse` for more information.
    """

    message_count: str = Field(..., validation_alias='message-count')
    messages: list[MessageResponse]

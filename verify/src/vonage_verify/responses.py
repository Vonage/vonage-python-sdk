from typing import Optional

from pydantic import BaseModel


class StartVerificationResponse(BaseModel):
    request_id: str
    status: str


class CheckCodeResponse(BaseModel):
    request_id: str
    status: str
    event_id: str
    price: str
    currency: str
    estimated_price_messages_sent: Optional[str] = None


# class MessageResponse(BaseModel):
#     to: str
#     message_id: str = Field(..., validation_alias='message-id')
#     status: str
#     remaining_balance: str = Field(..., validation_alias='remaining-balance')
#     message_price: str = Field(..., validation_alias='message-price')
#     network: str
#     client_ref: Optional[str] = Field(None, validation_alias='client-ref')
#     account_ref: Optional[str] = Field(None, validation_alias='account-ref')


# class SmsResponse(BaseModel):
#     message_count: str = Field(..., validation_alias='message-count')
#     messages: List[MessageResponse]

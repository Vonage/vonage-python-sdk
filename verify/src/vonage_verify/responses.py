from pydantic import BaseModel


class VerifyResponse(BaseModel):
    request_id: str
    status: str


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

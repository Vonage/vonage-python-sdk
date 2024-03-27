from typing import List, Optional

from pydantic import BaseModel, Field


class Link(BaseModel):
    href: str


class UserLinks(BaseModel):
    self: Link


class Links(BaseModel):
    self: Link
    first: Link
    next: Optional[Link] = None
    prev: Optional[Link] = None


class User(BaseModel):
    id: Optional[str]
    name: Optional[str]
    display_name: Optional[str]
    links: Optional[UserLinks] = Field(..., validation_alias='_links')


class Embedded(BaseModel):
    users: List[User] = []


class ListUsersResponse(BaseModel):
    page_size: int
    embedded: Embedded = Field(..., validation_alias='_embedded')
    links: Links = Field(..., validation_alias='_links')


class CreateUserResponse(BaseModel):
    id: str
    name: str
    display_name: str
    links: UserLinks = Field(..., validation_alias='_links')


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
#     messages: List[dict]

#     @field_validator('messages')
#     @classmethod
#     def create_message_response(cls, value):
#         messages = []
#         for message in value:
#             messages.append(MessageResponse(**message))
#         return messages

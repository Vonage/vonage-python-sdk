from typing import List, Optional
from pydantic import BaseModel, Field, model_validator


class CreateCallResponse(BaseModel):
    uuid: str
    status: str
    direction: str
    conversation_uuid: str


class CallStatus(BaseModel):
    message: str
    uuid: str


class Link(BaseModel):
    href: str


class Links(BaseModel):
    self: Link
    first: Optional[Link] = None
    next: Optional[Link] = None
    prev: Optional[Link] = None


class Endpoint(BaseModel):
    type: str
    number: str


class CallInfo(BaseModel):
    uuid: str
    conversation_uuid: str
    to: Endpoint
    from_: Endpoint = Field(..., alias='from')
    status: str
    direction: str
    rate: Optional[str] = None
    price: Optional[str] = None
    duration: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    network: Optional[str] = None
    links: Links = Field(..., validation_alias='_links', exclude=True)
    link: Optional[str] = None

    @model_validator(mode='after')
    @classmethod
    def get_link(self):
        self.link = self.links.self.href
        return self


class Embedded(BaseModel):
    calls: List[CallInfo]


class CallList(BaseModel):
    count: int
    page_size: int
    record_index: int
    embedded: Embedded = Field(..., validation_alias='_embedded')
    links: Links = Field(..., validation_alias='_links')

from typing import List, Optional, Union

from pydantic import BaseModel, Field, model_validator
from vonage_utils.models import HalLinks

from .common import Phone, Sip, Vbc, Websocket


class CreateCallResponse(BaseModel):
    uuid: str
    status: str
    direction: str
    conversation_uuid: str


class CallMessage(BaseModel):
    message: str
    uuid: str


class CallInfo(BaseModel):
    uuid: str
    conversation_uuid: str
    to: Phone
    from_: Union[Phone, Sip, Websocket, Vbc] = Field(..., validation_alias='from')
    status: str
    direction: str
    rate: Optional[str] = None
    price: Optional[str] = None
    duration: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    network: Optional[str] = None
    links: HalLinks = Field(..., validation_alias='_links', exclude=True)
    link: Optional[str] = None

    @model_validator(mode='after')
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
    links: HalLinks = Field(..., validation_alias='_links')

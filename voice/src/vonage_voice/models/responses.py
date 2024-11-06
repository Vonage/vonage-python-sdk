from typing import Optional, Union

from pydantic import BaseModel, Field, model_validator
from vonage_utils.models import HalLinks

from .common import Phone, Sip, Vbc, Websocket


class CreateCallResponse(BaseModel):
    """Response model for creating a call.

    Args:
        uuid (str): The unique identifier for the call.
        status (str): The status of the call.
        direction (str): The direction of the call.
        conversation_uuid (str): The unique identifier for the conversation this call
            leg is part of.
    """

    uuid: str
    status: str
    direction: str
    conversation_uuid: str


class CallMessage(BaseModel):
    """Model for a call message.

    Args:
        message (str): Description of the action taken.
        uuid (str): The unique identifier for this call leg.
    """

    message: str
    uuid: str


class CallInfo(BaseModel):
    """Model for information about a call.

    Args:
        uuid (str): The unique identifier for the call.
        conversation_uuid (str): The unique identifier for the conversation this call
            leg is part of.
        to (Union[Phone, Sip, Websocket, Vbc]): The endpoint that received the call.
        from_ (Union[Phone, Sip, Websocket, Vbc]): The phone number that made the call.
        status (str): The status of the call.
        direction (str): The direction of the call.
        rate (Optional[str]): The price per minute for this call. This is only sent
            if `status` is `completed`.
        price (Optional[str]): The total price charged for this call. This is only
            sent if `status` is `completed`.
        duration (Optional[str]): The time elapsed for the call to take place in seconds.
            This is only sent if `status` is `completed`.
        start_time (Optional[str]): The time the call started in the following format:
            YYYY-MM-DD HH:MM:SS.
        end_time (Optional[str]): The time the call ended in the following format:
            YYYY-MM-DD HH:MM:SS.
        network (Optional[str]): The Mobile Country Code Mobile Network Code (MCCMNC) for
            the carrier network used to make this call.
        link (Optional[str]): The URL to this resource.
    """

    uuid: str
    conversation_uuid: str
    to: Union[Phone, Sip, Websocket, Vbc]
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
    """Model for calls embedded in a response.

    Args:
        calls (list[CallInfo]): The calls in this response.
    """

    calls: list[CallInfo]


class CallList(BaseModel):
    """Model for a list of calls.

    Args:
        count (int): The total number of records.
        page_size (int): The number of records in this response.
        record_index (int): The index of the first record in this response.
        embedded (Embedded): The calls in this response.
        links (HalLinks): The links to navigate the list of calls.
    """

    count: int
    page_size: int
    record_index: int
    embedded: Embedded = Field(..., validation_alias='_embedded')
    links: HalLinks = Field(..., validation_alias='_links')

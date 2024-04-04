from typing import List, Optional

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


class Check(BaseModel):
    date_received: Optional[str] = None
    code: Optional[str] = None
    status: Optional[str] = None
    ip_address: Optional[str] = None


class Event(BaseModel):
    type: Optional[str] = None
    id: Optional[str] = None


class VerifyStatus(BaseModel):
    request_id: Optional[str] = None
    account_id: Optional[str] = None
    status: Optional[str] = None
    number: Optional[str] = None
    price: Optional[str] = None
    currency: Optional[str] = None
    sender_id: Optional[str] = None
    date_submitted: Optional[str] = None
    date_finalized: Optional[str] = None
    first_event_date: Optional[str] = None
    last_event_date: Optional[str] = None
    checks: Optional[List[Check]] = None
    events: Optional[List[Event]] = None
    estimated_price_messages_sent: Optional[str] = None


class VerifyControlStatus(BaseModel):
    status: str
    command: str


class NetworkUnblockStatus(BaseModel):
    network: str
    unblocked_until: str

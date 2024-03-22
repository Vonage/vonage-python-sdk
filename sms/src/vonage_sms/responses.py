from dataclasses import dataclass
from typing import List, Optional


@dataclass
class MessageResponse:
    to: str
    message_id: str
    status: str
    remaining_balance: str
    message_price: str
    network: str
    client_ref: Optional[str] = None
    account_ref: Optional[str] = None


@dataclass
class SmsResponse:
    message_count: str
    messages: List[MessageResponse]

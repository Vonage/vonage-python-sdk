from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class VonageAccount(BaseModel):
    api_key: str
    name: str
    primary_account_api_key: str
    use_primary_account_balance: bool
    created_at: datetime
    suspended: bool
    balance: Optional[float]
    credit_limit: Optional[float]


class PrimaryAccount(VonageAccount): ...


class Subaccount(VonageAccount): ...

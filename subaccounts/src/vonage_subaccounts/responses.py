from typing import List, Optional, Union

from pydantic import BaseModel, Field


class VonageAccount(BaseModel):
    api_key: str
    name: str
    created_at: str
    suspended: bool
    balance: Optional[float]
    credit_limit: Optional[Union[int, float]]


class PrimaryAccount(VonageAccount):
    ...


class Subaccount(VonageAccount):
    primary_account_api_key: str
    use_primary_account_balance: bool


class ListSubaccountsResponse(BaseModel):
    primary_account: PrimaryAccount
    subaccounts: List[Subaccount]
    total_balance: float
    total_credit_limit: Union[int, float]


class NewSubaccount(Subaccount):
    secret: str


class Transfer(BaseModel):
    id: str
    amount: float
    from_: str = Field(..., validation_alias='from')
    to: str
    created_at: str
    reference: Optional[str] = None


class TransferNumberResponse(BaseModel):
    number: str
    country: str
    from_: str = Field(..., validation_alias='from')
    to: str

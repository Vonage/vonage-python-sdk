import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator
from vonage_subaccounts.errors import InvalidSecretError


class SubaccountOptions(BaseModel):
    name: str = Field(..., min_length=1, max_length=80)
    secret: Optional[str] = None
    use_primary_account_balance: Optional[bool] = None

    @field_validator('secret')
    @classmethod
    def check_valid_secret(cls, v):
        if not _is_valid_secret(v):
            raise InvalidSecretError(
                'Secret must be 8-25 characters long and contain at least one uppercase '
                'letter, one lowercase letter, and one digit.'
            )
        return v


def _is_valid_secret(secret: str) -> bool:
    if len(secret) < 8 or len(secret) > 25:
        return False
    if not re.search(r'[a-z]', secret):
        return False
    if not re.search(r'[A-Z]', secret):
        return False
    if not re.search(r'\d', secret):
        return False
    return True


class ModifySubaccountOptions(BaseModel):
    suspended: Optional[bool] = None
    use_primary_account_balance: Optional[bool] = None
    name: Optional[str] = None


class ListTransfersFilter(BaseModel):
    start_date: str
    end_date: Optional[str] = None
    subaccount: Optional[str] = None


class TransferRequest(BaseModel):
    from_: str = Field(..., serialization_alias='from')
    to: str
    amount: float
    reference: Optional[str] = None


class TransferNumberRequest(BaseModel):
    from_: str = Field(..., serialization_alias='from')
    to: str
    number: str
    country: Optional[str] = None

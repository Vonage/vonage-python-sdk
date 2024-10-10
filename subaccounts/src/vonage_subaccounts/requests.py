import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator
from vonage_subaccounts.errors import InvalidSecretError


class SubaccountOptions(BaseModel):
    """Model for creating a subaccount.

    Args:
        name (str): The name of the subaccount.
        secret (str, Optional): The secret of the subaccount.
        use_primary_account_balance (bool, Optional): Whether the subaccount uses the
            primary account balance.

    Raises:
        InvalidSecretError: If the secret is invalid.
    """

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
    """Check if a secret is valid."""

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
    """Model for modifying a subaccount.

    Args:
        suspended (bool, Optional): Whether the subaccount is suspended.
        use_primary_account_balance (bool, Optional): Whether the subaccount uses the
            primary account balance.
        name (str, Optional): The name of the subaccount.
    """

    suspended: Optional[bool] = None
    use_primary_account_balance: Optional[bool] = None
    name: Optional[str] = None


class ListTransfersFilter(BaseModel):
    """Model with filters for listing transfers.

    Args:
        start_date (str): The start date of the retrieval period.
        end_date (str, Optional): The end date of the retrieval period. If not included,
            all transfers up to the present are returned.
        subaccount (str, Optional): The subaccount API key to filter on.
    """

    start_date: str
    end_date: Optional[str] = None
    subaccount: Optional[str] = None


class TransferRequest(BaseModel):
    """Model for transferring credit/balance between accounts.

    Args:
        from_ (str): The API key of the account the transfer is from.
        to (str): The API key of the account the transfer is to.
        amount (float): The amount of the transfer in EUR.
        reference (str, Optional): A reference for the transfer.
    """

    from_: str = Field(..., serialization_alias='from')
    to: str
    amount: float
    reference: Optional[str] = None


class TransferNumberRequest(BaseModel):
    """Model for transferring a number between accounts.

    Args:
        from_ (str): The API key of the account the number is from.
        to (str): The API key of the account the number is to.
        number (str): The number to transfer.
        country (str, Optional): The two-letter country code (in ISO 3166-1 alpha-2 format).
    """

    from_: str = Field(..., serialization_alias='from')
    to: str
    number: str
    country: Optional[str] = None

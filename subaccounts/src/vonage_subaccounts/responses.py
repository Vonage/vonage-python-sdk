from typing import Optional, Union

from pydantic import BaseModel, Field


class VonageAccount(BaseModel):
    """Model for a Vonage account/subaccount.

    Args:
        api_key (str): The API key of the account.
        name (str): The name of the account.
        created_at (str): The date and time the account was created.
        suspended (bool): Whether the account is suspended.
        balance (float): The balance of the account.
        credit_limit (float): The credit limit of the account.
    """

    api_key: str
    name: str
    created_at: str
    suspended: bool
    balance: Optional[float]
    credit_limit: Optional[Union[int, float]]


class PrimaryAccount(VonageAccount):
    """Model for a Vonage primary account.

    Args:
        api_key (str): The API key of the account.
        name (str): The name of the account.
        created_at (str): The date and time the account was created.
        suspended (bool): Whether the account is suspended.
        balance (float): The balance of the account.
        credit_limit (float): The credit limit of the account.
    """


class Subaccount(VonageAccount):
    """Model for a Vonage subaccount.

    Args:
        api_key (str): The API key of the account.
        name (str): The name of the account.
        primary_account_api_key (str): The API key of the primary account.
        use_primary_account_balance (bool): Whether the subaccount uses the primary
            account balance.
        created_at (str): The date and time the account was created.
        suspended (bool): Whether the account is suspended.
        balance (float): The balance of the account. Value is null if balance is shared
            with primary account.
        credit_limit (float): The credit limit of the account. Value is null if balance
            is shared with primary account.
    """

    primary_account_api_key: str
    use_primary_account_balance: bool


class ListSubaccountsResponse(BaseModel):
    """Model for a list of subaccounts.

    Args:
        primary_account (PrimaryAccount): The primary account. See `PrimaryAccount`.
        subaccounts (list[Subaccount]): The subaccounts. See `Subaccount`.
        total_balance (float): The total balance of all subaccounts.
        total_credit_limit (Union[int, float]): The total credit limit of all subaccounts.
    """

    primary_account: PrimaryAccount
    subaccounts: list[Subaccount]
    total_balance: float
    total_credit_limit: Union[int, float]


class NewSubaccount(Subaccount):
    """NewSubaccount: The new subaccount

    Args:
        secret (str): The API secret of the subaccount.
        api_key (str): The API key of the account.
        name (str): The name of the account.
        primary_account_api_key (str): The API key of the primary account.
        use_primary_account_balance (bool): Whether the subaccount uses the primary
            account balance.
        created_at (str): The date and time the account was created.
        suspended (bool): Whether the account is suspended.
        balance (float): The balance of the account. Value is null if balance is shared
            with primary account.
        credit_limit (float): The credit limit of the account. Value is null if balance
            is shared with primary account.
    """

    secret: str


class Transfer(BaseModel):
    """Model for a credit/balance transfer between accounts.

    Args:
        id (str): The Unique credit transfer ID.
        amount (float): The amount of the transfer.
        from_ (str): The API key of the account the transfer is from.
        to (str): The API key of the account the transfer is to.
        created_at (str): The date and time the transfer was created.
        reference (str, Optional): A reference for the transfer.
    """

    id: str
    amount: float
    from_: str = Field(..., validation_alias='from')
    to: str
    created_at: str
    reference: Optional[str] = None


class TransferNumberResponse(BaseModel):
    """Model for a number transfer between accounts.

    Args:
        number (str): The phone number in E.164 format.
        country (str): The two-letter country code (in ISO 3166-1 alpha-2 format).
        from_ (str): The API key of the account the number is being transferred from.
        to (str): The API key of the account the number is being transferred to.
    """

    number: str
    country: str
    from_: str = Field(..., validation_alias='from')
    to: str

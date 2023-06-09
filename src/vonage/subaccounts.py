from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Union

from .errors import SubaccountsError

if TYPE_CHECKING:
    from vonage import Client


class Subaccounts:
    """Class containing methods for working with the Vonage Subaccounts API."""

    def __init__(self, client: Client):
        self._client = client
        self._api_key = self._client.api_key
        self._api_host = self._client.api_host()
        self._auth_type = 'header'

    def list_subaccounts(self):
        return self._client.get(
            self._api_host,
            f'/accounts/{self._api_key}/subaccounts',
            auth_type=self._auth_type,
        )

    def create_subaccount(
        self,
        name: str,
        secret: Optional[str] = None,
        use_primary_account_balance: Optional[bool] = None,
    ):
        params = {'name': name}

        if secret is not None:
            params['secret'] = secret

        if use_primary_account_balance is not None:
            if type(use_primary_account_balance) == bool:
                params['use_primary_account_balance'] = use_primary_account_balance
            else:
                raise SubaccountsError(
                    '"use_primary_account_balance" must be a boolean, if supplied.'
                )

        return self._client.post(
            self._api_host,
            f'/accounts/{self._api_key}/subaccounts',
            params=params,
            auth_type=self._auth_type,
        )

    def get_subaccount(self, subaccount_key: str):
        return self._client.get(
            self._api_host,
            f'/accounts/{self._api_key}/subaccounts/{subaccount_key}',
            auth_type=self._auth_type,
        )

    def modify_subaccount(
        self,
        subaccount_key: str,
        suspended: Optional[bool] = None,
        use_primary_account_balance: Optional[bool] = None,
        name: Optional[str] = None,
    ):
        ...

    def list_credit_transfers(self, start_date: str = None, end_date: str = None, subaccount=[]):
        ...

    def transfer_credit(
        self, from_: str, to: str, amount: Union[float, int], reference: str = None
    ):
        ...

    def list_balance_transfers(self, start_date: str = None, end_date: str = None, subaccount=[]):
        ...

    def transfer_balance(
        self, from_: str, to: str, amount: Union[float, int], reference: str = None
    ):
        ...

    def transfer_number(self, from_: str, to: str, number: int, country: str):
        ...

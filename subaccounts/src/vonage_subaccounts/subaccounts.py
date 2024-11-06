from pydantic import validate_call
from vonage_http_client.http_client import HttpClient
from vonage_subaccounts.requests import (
    ListTransfersFilter,
    ModifySubaccountOptions,
    SubaccountOptions,
    TransferNumberRequest,
    TransferRequest,
)
from vonage_subaccounts.responses import (
    ListSubaccountsResponse,
    NewSubaccount,
    PrimaryAccount,
    Subaccount,
    Transfer,
    TransferNumberResponse,
)


class Subaccounts:
    """Class containing methods to manage Vonage subaccounts.

    Args:
        http_client (HttpClient): The HTTP client to make requests to the Subaccounts API.
    """

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client
        self._auth_type = 'basic'

    @property
    def http_client(self) -> HttpClient:
        """The HTTP client used to make requests to the Subaccounts API.

        Returns:
            HttpClient: The HTTP client used to make requests to the Subaccounts API.
        """
        return self._http_client

    def list_subaccounts(self) -> ListSubaccountsResponse:
        """List all subaccounts associated with the primary account.

        Returns:
            ListSubaccountsResponse: A response containing the primary account and all subaccounts.
            ListSubaccountsResponse contains the following attributes:
                - primary_account (PrimaryAccount): The primary account.
                - subaccounts (list[Subaccount]): A list of subaccounts.
                - total_balance (float): The total balance of the primary account and all subaccounts.
                - total_credit_limit (float): The total credit limit of the primary account and all subaccounts.
        """
        response = self._http_client.get(
            self._http_client.api_host,
            f'/accounts/{self._http_client.auth.api_key}/subaccounts',
            auth_type=self._auth_type,
        )

        response = {
            'primary_account': PrimaryAccount(**response['_embedded']['primary_account']),
            'subaccounts': response['_embedded']['subaccounts'],
            'total_balance': response['total_balance'],
            'total_credit_limit': response['total_credit_limit'],
        }

        return ListSubaccountsResponse(**response)

    @validate_call
    def create_subaccount(self, options: SubaccountOptions) -> NewSubaccount:
        """Create a subaccount.

        Args:
            SubaccountOptions: The options for the new subaccount. Contains the following attributes:
                - name (str): The name of the subaccount.
                - secret (str): The secret of the subaccount.
                - use_primary_account_balance (bool): Whether the subaccount uses the primary account balance

        Returns:
            NewSubaccount: The new subaccount. Contains the following attributes:
                - api_key (str): The API key of the subaccount.
                - name (str): The name of the subaccount.
                - created_at (str): The date and time the subaccount was created.
                - suspended (bool): Whether the subaccount is suspended.
                - primary_account_api_key (str): The API key of the primary account.
                - use_primary_account_balance (bool): Whether the subaccount uses the primary account balance
                - secret (str): The secret of the subaccount.
                - balance (float): The balance of the subaccount.
                - credit_limit (float): The credit limit of the subaccount.
        """
        response = self._http_client.post(
            self._http_client.api_host,
            f'/accounts/{self._http_client.auth.api_key}/subaccounts',
            options.model_dump(exclude_none=True),
            auth_type=self._auth_type,
        )

        return NewSubaccount(**response)

    @validate_call
    def get_subaccount(self, subaccount_api_key: str) -> Subaccount:
        """Get a subaccount by API key.

        Args:
            subaccount_api_key (str): The API key of the subaccount to get.

        Returns:
            Subaccount: The subaccount. Contains the following attributes:
                - api_key (str): The API key of the subaccount.
                - name (str): The name of the subaccount.
                - created_at (str): The date and time the subaccount was created.
                - suspended (bool): Whether the subaccount is suspended.
                - primary_account_api_key (str): The API key of the primary account.
                - use_primary_account_balance (bool): Whether the subaccount uses the primary account balance
                - balance (float): The balance of the subaccount.
                - credit_limit (float): The credit limit of the subaccount.
        """
        response = self._http_client.get(
            self._http_client.api_host,
            f'/accounts/{self._http_client.auth.api_key}/subaccounts/{subaccount_api_key}',
            auth_type=self._auth_type,
        )

        return Subaccount(**response)

    @validate_call
    def modify_subaccount(
        self, subaccount_api_key: str, options: ModifySubaccountOptions
    ) -> Subaccount:
        """Modify a subaccount.

        Args:
            subaccount_api_key (str): The API key of the subaccount to modify.
            ModifySubaccountOptions: The options for modifying the subaccount. Contains the following attributes:
                - suspended (bool): Whether the subaccount is suspended.
                - use_primary_account_balance (bool): Whether the subaccount uses the primary account balance.
                - name (str): The name of the subaccount.

        Returns:
            Subaccount: The modified subaccount. Contains the following attributes:
                - api_key (str): The API key of the subaccount.
                - name (str): The name of the subaccount.
                - created_at (str): The date and time the subaccount was created.
                - suspended (bool): Whether the subaccount is suspended.
                - primary_account_api_key (str): The API key of the primary account.
                - use_primary_account_balance (bool): Whether the subaccount uses the primary account balance.
                - balance (float): The balance of the subaccount.
                - credit_limit (float): The credit limit of the subaccount.
        """
        response = self._http_client.patch(
            self._http_client.api_host,
            f'/accounts/{self._http_client.auth.api_key}/subaccounts/{subaccount_api_key}',
            options.model_dump(exclude_none=True),
            auth_type=self._auth_type,
        )

        return Subaccount(**response)

    def list_balance_transfers(self, filter: ListTransfersFilter) -> list[Transfer]:
        """List all balance transfers.

        Args:
            filter (ListTransfersFilter): The filter for the balance transfers. Contains the following attributes:
                - start_date (str, required)
                - end_date (str)
                - subaccount (str): Show balance transfers relating to this subaccount.

        Returns:
            list[Transfer]: A list of balance transfers. Each balance transfer contains the following attributes:
                - id (str)
                - amount (float)
                - from_ (str)
                - to (str)
                - created_at (str)
                - reference (str)
        """
        response = self._http_client.get(
            self._http_client.api_host,
            f'/accounts/{self._http_client.auth.api_key}/balance-transfers',
            filter.model_dump(exclude_none=True),
            auth_type=self._auth_type,
        )

        return [
            Transfer(**transfer)
            for transfer in response['_embedded']['balance_transfers']
        ]

    def transfer_balance(self, params: TransferRequest) -> Transfer:
        """Transfer balance between subaccounts.

        Args:
            params (TransferRequest): The parameters for the balance transfer. Contains the following attributes:
                - from_ (str): The API key of the subaccount to transfer balance from.
                - to (str): The API key of the subaccount to transfer balance to.
                - amount (float): The amount to transfer.
                - reference (str): A reference for the transfer.

        Returns:
            Transfer: The balance transfer. Contains the following attributes:
                - id (str)
                - amount (float)
                - from_ (str)
                - to (str)
                - created_at (str)
                - reference (str)
        """
        response = self._http_client.post(
            self._http_client.api_host,
            f'/accounts/{self._http_client.auth.api_key}/balance-transfers',
            params.model_dump(by_alias=True, exclude_none=True),
            auth_type=self._auth_type,
        )

        return Transfer(**response)

    def list_credit_transfers(self, filter: ListTransfersFilter) -> list[Transfer]:
        """List all credit transfers.

        Args:
            filter (ListTransfersFilter): The filter for the credit transfers. Contains the following attributes:
                - start_date (str, required)
                - end_date (str)
                - subaccount (str): Show credit transfers relating to this subaccount.

        Returns:
            list[Transfer]: A list of credit transfers. Each credit transfer contains the following attributes:
                - id (str)
                - amount (float)
                - from_ (str)
                - to (str)
                - created_at (str)
                - reference (str)
        """
        response = self._http_client.get(
            self._http_client.api_host,
            f'/accounts/{self._http_client.auth.api_key}/credit-transfers',
            filter.model_dump(exclude_none=True),
            auth_type=self._auth_type,
        )

        return [
            Transfer(**transfer) for transfer in response['_embedded']['credit_transfers']
        ]

    @validate_call
    def transfer_credit(self, params: TransferRequest) -> Transfer:
        """Transfer credit between subaccounts.

        Args:
            params (TransferRequest): The parameters for the credit transfer. Contains the following attributes:
                - from_ (str): The API key of the subaccount to transfer credit from.
                - to (str): The API key of the subaccount to transfer credit to.
                - amount (float): The amount to transfer.
                - reference (str): A reference for the transfer.

        Returns:
            Transfer: The credit transfer. Contains the following attributes:
                - id (str)
                - amount (float)
                - from_ (str)
                - to (str)
                - created_at (str)
                - reference (str)
        """
        response = self._http_client.post(
            self._http_client.api_host,
            f'/accounts/{self._http_client.auth.api_key}/credit-transfers',
            params.model_dump(by_alias=True, exclude_none=True),
            auth_type=self._auth_type,
        )

        return Transfer(**response)

    @validate_call
    def transfer_number(self, params: TransferNumberRequest) -> TransferNumberResponse:
        """Transfer a number between subaccounts.

        Args:
            params (TransferNumberRequest): The parameters for the number transfer. Contains the following attributes:
                - from_ (str): The API key of the subaccount to transfer the number from.
                - to (str): The API key of the subaccount to transfer the number to.
                - number (str): The number to transfer.
                - country (str): The country code of the number.

        Returns:
            TransferNumberResponse: The number transfer. Contains the following attributes:
                - number (str)
                - country (str)
                - from_ (str)
                - to (str)
        """
        response = self._http_client.post(
            self._http_client.api_host,
            f'/accounts/{self._http_client.auth.api_key}/transfer-number',
            params.model_dump(by_alias=True, exclude_none=True),
            auth_type=self._auth_type,
        )

        return TransferNumberResponse(**response)

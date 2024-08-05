from pydantic import validate_call
from vonage_http_client.http_client import HttpClient

from .requests import Balance
from .responses import SettingsResponse, TopUpResponse


class Account:
    """Class containing methods for management of a Vonage account."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client
        self._auth_type = 'basic'

    @property
    def http_client(self) -> HttpClient:
        """The HTTP client used to make requests to the Users API.

        Returns:
            HttpClient: The HTTP client used to make requests to the Users API.
        """
        return self._http_client

    @validate_call
    def get_balance(self) -> Balance:
        """Get the balance of the account.

        Returns:
            Balance: Object containing the account balance and whether auto-reload is
                enabled for the account.
        """

        response = self._http_client.get(
            self._http_client.rest_host,
            '/account/get-balance',
            auth_type=self._auth_type,
        )
        return Balance(**response)

    @validate_call
    def top_up(self, trx: str) -> TopUpResponse:
        """Top-up the account balance.

        Args:
            trx (str): The transaction reference of the transaction when auto-reload
                was enabled on your account.

        Returns:
            TopUpResponse: Object containing the top-up response.
        """

        response = self._http_client.post(
            self._http_client.rest_host,
            '/account/top-up',
            params={'trx': trx},
            auth_type=self._auth_type,
            sent_data_type='form',
        )
        return TopUpResponse(**response)

    @validate_call
    def update_default_sms_webhook(
        self, mo_callback_url: str = None, dr_callback_url: str = None
    ) -> SettingsResponse:
        """Update the default SMS webhook URLs for the account.
            In order to unset any default value, pass an empty string as the value.

        Args:
            mo_callback_url (str, optional): The URL to which inbound SMS messages will be
                sent.
            dr_callback_url (str, optional): The URL to which delivery receipts will be sent.

        Returns:
            SettingsResponse: Object containing the response to the settings update.
        """

        params = {}
        if mo_callback_url is not None:
            params['moCallbackUrl'] = mo_callback_url
        if dr_callback_url is not None:
            params['drCallbackUrl'] = dr_callback_url

        response = self._http_client.post(
            self._http_client.rest_host,
            '/account/settings',
            params=params,
            auth_type=self._auth_type,
            sent_data_type='form',
        )
        return SettingsResponse(**response)

    def list_secrets(self) -> SecretList:
        """List all secrets associated with the account.

        Returns:
            SecretList: List of Secret objects.
        """
        pass

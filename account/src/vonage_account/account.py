import re

from pydantic import validate_call
from vonage_account.errors import InvalidSecretError
from vonage_account.requests import (
    GetCountryPricingRequest,
    GetPrefixPricingRequest,
    ServiceType,
)
from vonage_http_client.http_client import HttpClient

from .responses import (
    Balance,
    GetMultiplePricingResponse,
    GetPricingResponse,
    SettingsResponse,
    TopUpResponse,
    VonageApiSecret,
)


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
        """Update the default SMS webhook URLs for the account. In order to unset any
        default value, pass an empty string as the value.

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

    @validate_call
    def get_country_pricing(
        self, options: GetCountryPricingRequest
    ) -> GetPricingResponse:
        """Get the pricing for a specific country.

        Args:
            options (GetCountryPricingRequest): The options for the request.

        Returns:
            GetCountryPricingResponse: The response from the API.
        """
        response = self._http_client.get(
            self._http_client.rest_host,
            f'/account/get-pricing/outbound/{options.type.value}',
            params={'country': options.country_code},
            auth_type=self._auth_type,
        )

        return GetPricingResponse(**response)

    @validate_call
    def get_all_countries_pricing(
        self, service_type: ServiceType
    ) -> GetMultiplePricingResponse:
        """Get the pricing for all countries.

        Args:
            service_type (ServiceType): The type of service to retrieve pricing data about.

        Returns:
            GetMultiplePricingResponse: Model containing the pricing data for all countries.
        """
        response = self._http_client.get(
            self._http_client.rest_host,
            f'/account/get-full-pricing/outbound/{service_type.value}',
            auth_type=self._auth_type,
        )

        return GetMultiplePricingResponse(**response)

    @validate_call
    def get_prefix_pricing(
        self, options: GetPrefixPricingRequest
    ) -> GetMultiplePricingResponse:
        """Get the pricing for a specific prefix.

        Args:
            options (GetPrefixPricingRequest): The options for the request.

        Returns:
            GetMultiplePricingResponse: Model containing the pricing data for all
                countries using the dialling prefix.
        """
        response = self._http_client.get(
            self._http_client.rest_host,
            f'/account/get-prefix-pricing/outbound/{options.type.value}',
            params={'prefix': options.prefix},
            auth_type=self._auth_type,
        )

        return GetMultiplePricingResponse(**response)

    def list_secrets(self) -> list[VonageApiSecret]:
        """List all secrets associated with the account.

        Returns:
            list[VonageApiSecret]: List of VonageApiSecret objects.
        """
        response = self._http_client.get(
            self._http_client.api_host,
            f'/accounts/{self._http_client.auth.api_key}/secrets',
            auth_type=self._auth_type,
        )
        secrets = []
        for element in response['_embedded']['secrets']:
            secrets.append(VonageApiSecret(**element))

        return secrets

    @validate_call
    def create_secret(self, secret: str) -> VonageApiSecret:
        """Create an API secret for the account.

        Args:
            secret (VonageSecret): The secret to create. Must satisfy the following
                conditions:
                - 8-25 characters long
                - At least one uppercase letter
                - At least one lowercase letter
                - At least one digit

        Returns:
            VonageApiSecret: The created VonageApiSecret object.
        """
        if not self._is_valid_secret(secret):
            raise InvalidSecretError(
                'Secret must be 8-25 characters long and contain at least one uppercase '
                'letter, one lowercase letter, and one digit.'
            )

        response = self._http_client.post(
            self._http_client.api_host,
            f'/accounts/{self._http_client.auth.api_key}/secrets',
            params={'secret': secret},
            auth_type=self._auth_type,
        )
        return VonageApiSecret(**response)

    @validate_call
    def get_secret(self, secret_id: str) -> VonageApiSecret:
        """Get a specific secret associated with the account.

        Args:
            secret_id (str): The ID of the secret to retrieve.

        Returns:
            VonageApiSecret: The VonageApiSecret object.
        """
        response = self._http_client.get(
            self._http_client.api_host,
            f'/accounts/{self._http_client.auth.api_key}/secrets/{secret_id}',
            auth_type=self._auth_type,
        )
        return VonageApiSecret(**response)

    @validate_call
    def revoke_secret(self, secret_id: str) -> None:
        """Revoke a specific secret associated with the account.

        Args:
            secret_id (str): The ID of the secret to revoke.
        """
        self._http_client.delete(
            self._http_client.api_host,
            f'/accounts/{self._http_client.auth.api_key}/secrets/{secret_id}',
            auth_type=self._auth_type,
        )

    def _is_valid_secret(self, secret: str) -> bool:
        if len(secret) < 8 or len(secret) > 25:
            return False
        if not re.search(r'[a-z]', secret):
            return False
        if not re.search(r'[A-Z]', secret):
            return False
        if not re.search(r'\d', secret):
            return False
        return True

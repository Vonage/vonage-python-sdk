from typing import List, Union
from pydantic import validate_call
from vonage_http_client.http_client import HttpClient

# from .responses import Balance, SettingsResponse, TopUpResponse, VonageApiSecret


class Subaccounts:
    """Class containing methods to manage Vonage subaccounts."""

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

    def list_subaccounts(self) -> Tuple[PrimaryAccount, List[Subaccount]]:
        """List all subaccounts associated with the primary account.

        Returns:
            List[Union[PrimaryAccount, Subaccount]]: List of PrimaryAccount and Subaccount objects.
        """
        response = self._http_client.get(
            self._http_client.api_host,
            f'/accounts/{self._http_client.auth.api_key}/subaccounts',
            auth_type=self._auth_type,
        )
        accounts = []
        # accounts.append(PrimaryAccount(**response['_embedded']['account']))

        # for element in response['_embedded']['accounts']:
        #     if element['type'] == 'PRIMARY':
        #         accounts.append(PrimaryAccount(**element))
        #     else:
        #         accounts.append(Subaccount(**element))

        # return accounts

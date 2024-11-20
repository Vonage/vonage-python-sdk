from pydantic import validate_call
from vonage_http_client.http_client import HttpClient

from .models import BaseMessage
from .responses import SendMessageResponse


class Messages:
    """Calls Vonage's Messages API.

    This class provides methods to interact with Vonage's Messages API, allowing you to send messages.

    Args:
        http_client (HttpClient): An instance of the HttpClient class used to make HTTP requests.
    """

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client
        self._auth_type = 'jwt'

        if self._http_client.auth.application_id is None:
            self._auth_type = 'basic'

    @property
    def http_client(self) -> HttpClient:
        """The HTTP client used to make requests to the Messages API.

        Returns:
            HttpClient: The HTTP client used to make requests to the Messages API.
        """
        return self._http_client

    @validate_call
    def send(self, message: BaseMessage) -> SendMessageResponse:
        """Send a message using Vonage's Messages API.

        Args:
            message (BaseMessage): The message to be sent as a Pydantic model.
                Use the provided models (in `vonage_messages.models`) to create messages and pass them in to this method.

        Returns:
            SendMessageResponse: Response model containing the unique identifier of the sent message.
                Access the identifier with the `message_uuid` attribute.
        """
        response = self._http_client.post(
            self._http_client.api_host,
            '/v1/messages',
            message.model_dump(by_alias=True, exclude_none=True) or message,
            self._auth_type,
        )

        return SendMessageResponse(**response)

    @validate_call
    def mark_whatsapp_message_read(self, message_uuid: str) -> None:
        """Mark a WhatsApp message as read.

        Note: to use this method, update the `api_host` attribute of the
        `vonage_http_client.HttpClientOptions` object to the API endpoint
        corresponding to the region where the WhatsApp number is hosted.

        For example, to use the EU API endpoint, set the `api_host`
        attribute to 'api-eu.vonage.com'.

        Args:
            message_uuid (str): The unique identifier of the WhatsApp message to mark as read.
        """
        self._http_client.patch(
            self._http_client.api_host,
            f'/v1/messages/{message_uuid}',
            {'status': 'read'},
            self._auth_type,
        )

    @validate_call
    def revoke_rcs_message(self, message_uuid: str) -> None:
        """Revoke an RCS message.

        Note: to use this method, update the `api_host` attribute of the
        `vonage_http_client.HttpClientOptions` object to the API endpoint
        corresponding to the region where the RCS number is hosted.

        For example, to use the EU API endpoint, set the `api_host`
        attribute to 'api-eu.vonage.com'.

        Args:
            message_uuid (str): The unique identifier of the RCS message to revoke.
        """
        self._http_client.patch(
            self._http_client.api_host,
            f'/v1/messages/{message_uuid}',
            {'status': 'revoked'},
            self._auth_type,
        )

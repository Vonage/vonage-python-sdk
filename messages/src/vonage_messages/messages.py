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
        )
        return SendMessageResponse(**response)

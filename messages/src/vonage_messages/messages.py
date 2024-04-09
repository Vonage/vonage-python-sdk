from pydantic import validate_call
from vonage_http_client.http_client import HttpClient

from .models.sms import BaseMessage
from .responses import MessageUuid


class Messages:
    """Calls Vonage's Messages API.

    This class provides methods to interact with Vonage's Messages API, allowing you to send messages.

    Args:
        http_client (HttpClient): An instance of the HttpClient class used to make HTTP requests.
    """

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    @validate_call
    def send(self, message: BaseMessage) -> MessageUuid:
        """Send a message using Vonage's Messages API.

        Args:
            message (Message): The message to be sent.

        Returns:
            MessageUuid: The unique identifier of the sent message.
        """
        response = self._http_client.post(
            self._http_client.api_host,
            '/v1/messages',
            message.model_dump(by_alias=True, exclude_none=True),
        )

        return MessageUuid(**response)

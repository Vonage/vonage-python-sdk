from pydantic import BaseModel


class SendMessageResponse(BaseModel):
    """Response from Vonage's Messages API.

    Attributes:
        message_uuid (str): The UUID of the sent message.
    """

    message_uuid: str

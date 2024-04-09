from pydantic import BaseModel


class MessageUuid(BaseModel):
    """Response from Vonage's Messages API."""

    message_uuid: str

from typing import Optional

from pydantic import BaseModel


class SendMessageResponse(BaseModel):
    """Response from Vonage's Messages API.

    Attributes:
        message_uuid (str): The UUID of the sent message.
        workflow_id [str]: Workflow ID if the `failover` parameter was used in the request.
    """

    message_uuid: str
    workflow_id: Optional[str] = None

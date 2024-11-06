from pydantic import BaseModel, Field


class SignalData(BaseModel):
    """The data to send in a signal.

    Args:
        type (str): The type of data being sent to the client.
        data (str): Payload to send to the client.
    """

    type: str = Field(..., max_length=128)
    data: str = Field(..., max_length=8192)

from pydantic import BaseModel, Field


class SignalData(BaseModel):
    """The data to send in a signal."""

    type: str
    data: str = Field(None, max_length=8192)

from pydantic import BaseModel, Field


class SignalData(BaseModel):
    """The data to send in a signal."""

    type: str = Field(..., max_length=128)
    data: str = Field(..., max_length=8192)

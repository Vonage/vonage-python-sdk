from pydantic import BaseModel, Field


class SwapStatus(BaseModel):
    swapped: str


class LastSwapDate(BaseModel):
    last_swap_date: str = Field(..., validation_alias='latestSimChange')

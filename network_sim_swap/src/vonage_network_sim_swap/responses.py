from pydantic import BaseModel, Field


class SwapStatus(BaseModel):
    """Model for the status of a SIM swap.

    Args:
        swapped (str): Indicates whether the SIM card has been swapped during the period
            within the `max_age` provided in the request.
    """

    swapped: str


class LastSwapDate(BaseModel):
    """Model for the last SIM swap date information.

    Args:
        last_swap_date (str): The timestamp of the latest SIM swap performed.
    """

    last_swap_date: str = Field(..., validation_alias='latestSimChange')

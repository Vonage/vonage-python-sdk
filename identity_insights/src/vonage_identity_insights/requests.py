from typing import Optional

from pydantic import BaseModel, Field
from vonage_utils.types import PhoneNumber


class EmptyInsight(BaseModel):
    """Model for an insight request without parameters.

    This model represents insights that must be included as an empty JSON object (`{}`) to
    indicate that the insight is requested.
    """


class SimSwapInsight(BaseModel):
    """Model for a SIM swap insight request.

    This insight checks whether a SIM swap has occurred within a specified
    period of time.

    Args:
        period (int, Optional): Period in hours to be checked for SIM swap.
            Must be between 1 and 2400. Defaults to 240.
    """

    period: Optional[int] = Field(
        default=240,
        ge=1,
        le=2400,
        description="Period in hours to be checked for SIM swap",
    )


class InsightsRequest(BaseModel):
    """Model for a collection of identity insight requests.

    Each field represents an individual insight. Only the insights included
    in this object will be processed and returned in the response.

    Args:
        format (EmptyInsight, Optional): Request phone number format validation.
        sim_swap (SimSwapInsight, Optional): Request SIM swap information.
        original_carrier (EmptyInsight, Optional): Request original carrier
            information.
        current_carrier (EmptyInsight, Optional): Request current carrier
            information.
    """

    format: Optional[EmptyInsight] = None
    sim_swap: Optional[SimSwapInsight] = None
    original_carrier: Optional[EmptyInsight] = None
    current_carrier: Optional[EmptyInsight] = None

    def at_least_one_insight(cls, values):
        """Validate that at least one insight is provided."""
        if not any(v is not None for v in values.values()):
            raise ValueError("At least one insight must be provided")
        return values


class IdentityInsightsRequest(BaseModel):
    """Model for an Identity Insights API request.

    This model represents a single aggregated request for one or more identity
    insights related to a phone number.

    Args:
        phone_number (PhoneNumber): The phone number to retrieve identity
            insights for.
        purpose (str, Optional): Purpose of the request. Required for insights
            that rely on the Network Registry.
        insights (InsightsRequest): Collection of requested insights.
    """

    phone_number: PhoneNumber
    purpose: Optional[str] = Field(
        None, description="Purpose of the request (required for some insights)"
    )
    insights: InsightsRequest
